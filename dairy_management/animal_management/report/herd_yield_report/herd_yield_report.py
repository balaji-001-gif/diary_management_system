# Dairy Management System — Script Report: Herd Yield Report

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Animal", "fieldname": "animal", "fieldtype": "Link", "options": "Animal", "width": 140},
        {"label": "Breed", "fieldname": "breed", "fieldtype": "Link", "options": "Breed", "width": 120},
        {"label": "Farmer", "fieldname": "farmer", "fieldtype": "Link", "options": "Farmer", "width": 140},
        {"label": "Lactation No.", "fieldname": "lactation_number", "fieldtype": "Int", "width": 110},
        {"label": "Start Date", "fieldname": "start_date", "fieldtype": "Date", "width": 110},
        {"label": "Dry-off Date", "fieldname": "dry_off_date", "fieldtype": "Date", "width": 110},
        {"label": "Total Yield (L)", "fieldname": "total_yield_litres", "fieldtype": "Float", "width": 120},
        {"label": "Peak Yield (L)", "fieldname": "peak_yield_litres", "fieldtype": "Float", "width": 110},
        {"label": "Avg Daily (L)", "fieldname": "avg_daily_yield", "fieldtype": "Float", "width": 110},
    ]

def get_data(filters):
    conditions = "lc.docstatus = 1"
    values = {}

    if filters.get("animal"):
        conditions += " AND lc.animal = %(animal)s"
        values["animal"] = filters["animal"]
    if filters.get("from_date"):
        conditions += " AND lc.start_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND COALESCE(lc.dry_off_date, CURRENT_DATE) <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    return frappe.db.sql(f"""
        SELECT lc.animal, a.breed, a.farmer, lc.lactation_number,
               lc.start_date, lc.dry_off_date,
               lc.total_yield_litres, lc.peak_yield_litres, lc.avg_daily_yield
        FROM `tabLactation Cycle` lc
        LEFT JOIN `tabAnimal` a ON a.name = lc.animal
        WHERE {conditions}
        ORDER BY lc.animal, lc.lactation_number
    """, values, as_dict=True)
