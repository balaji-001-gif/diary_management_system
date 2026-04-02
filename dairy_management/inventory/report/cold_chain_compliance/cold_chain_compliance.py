# Dairy Management System — Script Report: Cold Chain Compliance

import frappe

def execute(filters=None):
    return get_columns(), get_data(filters)

def get_columns():
    return [
        {"label": "Log", "fieldname": "name", "fieldtype": "Link", "options": "Cold Storage Log", "width": 150},
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 140},
        {"label": "Date", "fieldname": "log_date", "fieldtype": "Date", "width": 110},
        {"label": "Min Temp (°C)", "fieldname": "min_temp_recorded_c", "fieldtype": "Float", "width": 110},
        {"label": "Max Temp (°C)", "fieldname": "max_temp_recorded_c", "fieldtype": "Float", "width": 110},
        {"label": "Breach", "fieldname": "temperature_breach", "fieldtype": "Check", "width": 80},
        {"label": "Notified To", "fieldname": "breach_notified_to", "fieldtype": "Data", "width": 140},
    ]

def get_data(filters):
    if not filters: filters = {}
    conditions = "1=1"
    values = {}

    if filters.get("warehouse"):
        conditions += " AND warehouse = %(warehouse)s"
        values["warehouse"] = filters["warehouse"]
    if filters.get("from_date"):
        conditions += " AND log_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND log_date <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    return frappe.db.sql(f"""
        SELECT name, warehouse, log_date, min_temp_recorded_c,
               max_temp_recorded_c, temperature_breach, breach_notified_to
        FROM `tabCold Storage Log`
        WHERE {conditions}
        ORDER BY log_date DESC, warehouse
    """, values, as_dict=True)
