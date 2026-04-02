# Dairy Management System — Script Report: Animal Health Calendar

import frappe

def execute(filters=None):
    return get_columns(), get_data(filters)

def get_columns():
    return [
        {"label": "Animal", "fieldname": "animal", "fieldtype": "Link", "options": "Animal", "width": 140},
        {"label": "Event Type", "fieldname": "event_type", "fieldtype": "Data", "width": 120},
        {"label": "Last Date", "fieldname": "date", "fieldtype": "Date", "width": 110},
        {"label": "Next Due", "fieldname": "next_due_date", "fieldtype": "Date", "width": 110},
        {"label": "Medicine", "fieldname": "medicine", "fieldtype": "Data", "width": 130},
        {"label": "Vet", "fieldname": "vet_name", "fieldtype": "Data", "width": 130},
    ]

def get_data(filters):
    if not filters: filters = {}
    conditions = "docstatus = 1 AND next_due_date IS NOT NULL"
    values = {}

    if filters.get("animal"):
        conditions += " AND animal = %(animal)s"
        values["animal"] = filters["animal"]
    if filters.get("from_date"):
        conditions += " AND next_due_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND next_due_date <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    return frappe.db.sql(f"""
        SELECT animal, event_type, date, next_due_date, medicine, vet_name
        FROM `tabHealth Record`
        WHERE {conditions}
        ORDER BY next_due_date ASC
    """, values, as_dict=True)
