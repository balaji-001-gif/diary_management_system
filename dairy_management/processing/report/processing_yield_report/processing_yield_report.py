# Dairy Management System — Script Report: Processing Yield Report

import frappe

def execute(filters=None):
    return get_columns(), get_data(filters)

def get_columns():
    return [
        {"label": "Batch", "fieldname": "name", "fieldtype": "Link", "options": "Batch Production", "width": 150},
        {"label": "Product", "fieldname": "product", "fieldtype": "Link", "options": "Item", "width": 140},
        {"label": "Date", "fieldname": "production_date", "fieldtype": "Date", "width": 110},
        {"label": "Qty Produced", "fieldname": "quantity_produced", "fieldtype": "Float", "width": 120},
        {"label": "Raw Milk (L)", "fieldname": "raw_milk_used_litres", "fieldtype": "Float", "width": 120},
        {"label": "Yield %", "fieldname": "yield_percentage", "fieldtype": "Percent", "width": 90},
        {"label": "Expiry Date", "fieldname": "expiry_date", "fieldtype": "Date", "width": 110},
    ]

def get_data(filters):
    if not filters: filters = {}
    conditions = "docstatus = 1"
    values = {}

    if filters.get("product"):
        conditions += " AND product = %(product)s"
        values["product"] = filters["product"]
    if filters.get("from_date"):
        conditions += " AND production_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND production_date <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    return frappe.db.sql(f"""
        SELECT name, product, production_date, quantity_produced,
               raw_milk_used_litres, yield_percentage, expiry_date
        FROM `tabBatch Production`
        WHERE {conditions}
        ORDER BY production_date DESC
    """, values, as_dict=True)
