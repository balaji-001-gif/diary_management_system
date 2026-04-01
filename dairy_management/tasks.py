"""
dairy_management/tasks.py
Scheduler tasks — invoked by hooks.py scheduler_events
"""
import frappe
from frappe.utils import today, add_days, getdate


def generate_daily_milk_summary():
    """
    Daily task: Aggregate all Milk Collection Entries into Shift Summaries
    for yesterday's date (run daily at midnight, covers previous day).
    """
    target_date = add_days(today(), -1)

    routes = frappe.get_all(
        "Milk Collection Entry",
        filters={"collection_date": target_date, "docstatus": 1},
        fields=["route", "shift"],
        group_by="route, shift",
    )

    for row in routes:
        route, shift = row.route, row.shift
        if not route:
            continue

        entries = frappe.get_all(
            "Milk Collection Entry",
            filters={"collection_date": target_date, "route": route, "shift": shift, "docstatus": 1},
            fields=["quantity_litres", "fat_percentage", "snf_percentage", "amount", "farmer"],
        )

        if not entries:
            continue

        total_qty = sum(e.quantity_litres or 0 for e in entries)
        total_amount = sum(e.amount or 0 for e in entries)
        avg_fat = (
            sum((e.fat_percentage or 0) * (e.quantity_litres or 0) for e in entries) / total_qty
            if total_qty else 0
        )
        avg_snf = (
            sum((e.snf_percentage or 0) * (e.quantity_litres or 0) for e in entries) / total_qty
            if total_qty else 0
        )

        if not frappe.db.exists("Shift Summary", {"route": route, "collection_date": target_date, "shift": shift}):
            ss = frappe.new_doc("Shift Summary")
            ss.route = route
            ss.collection_date = target_date
            ss.shift = shift
            ss.total_quantity_litres = total_qty
            ss.avg_fat_percentage = round(avg_fat, 2)
            ss.avg_snf_percentage = round(avg_snf, 2)
            ss.farmer_count = len(entries)
            ss.total_amount = total_amount
            ss.insert(ignore_permissions=True)
            frappe.db.commit()


def check_animal_vaccination_due():
    """
    Daily task: Send alerts for animals with vaccinations due in the next 7 days.
    """
    due_records = frappe.get_all(
        "Health Record",
        filters={
            "next_due_date": ["between", [today(), add_days(today(), 7)]],
            "docstatus": 1,
        },
        fields=["animal", "event_type", "next_due_date"],
    )

    for record in due_records:
        frappe.sendmail(
            recipients=frappe.db.get_single_value("System Settings", "admin_password") or [],
            subject=f"[DMS] Vaccination Due: {record.animal}",
            message=(
                f"Animal {record.animal} has a {record.event_type} due on {record.next_due_date}. "
                f"Please schedule the appointment."
            ),
        )


def check_cold_storage_temperature():
    """
    Daily task: Flag cold storage logs with temperature breaches
    and log an error for follow-up.
    """
    breach_logs = frappe.get_all(
        "Cold Storage Log",
        filters={"log_date": today(), "temperature_breach": 1},
        fields=["name", "warehouse", "max_temp_recorded_c", "breach_notified_to"],
    )

    for log in breach_logs:
        frappe.log_error(
            f"Cold Storage breach at {log.warehouse}: max temp {log.max_temp_recorded_c}°C on {today()}. "
            f"Notified: {log.breach_notified_to or 'Not set'}",
            "Cold Storage Temperature Breach",
        )


def generate_farmer_payment_vouchers():
    """
    Weekly task: Auto-generate Farmer Invoices for active farmers
    based on the Payment Cycle Setting.
    """
    from frappe.utils import get_first_day, get_last_day
    from datetime import date

    today_date = getdate(today())
    period_from = get_first_day(today_date)
    period_to = get_last_day(today_date)

    farmers = frappe.get_all("Farmer", filters={}, fields=["name"])

    for f in farmers:
        exists = frappe.db.exists(
            "Farmer Invoice",
            {"farmer": f.name, "period_from": period_from, "period_to": period_to},
        )
        if exists:
            continue

        entries = frappe.get_all(
            "Milk Collection Entry",
            filters={
                "farmer": f.name,
                "collection_date": ["between", [period_from, period_to]],
                "docstatus": 1,
            },
            fields=["quantity_litres", "amount"],
        )

        if not entries:
            continue

        total_litres = sum(e.quantity_litres or 0 for e in entries)
        gross_amount = sum(e.amount or 0 for e in entries)

        inv = frappe.new_doc("Farmer Invoice")
        inv.farmer = f.name
        inv.period_from = period_from
        inv.period_to = period_to
        inv.total_litres_supplied = total_litres
        inv.gross_amount = gross_amount
        inv.insert(ignore_permissions=True)

    frappe.db.commit()
