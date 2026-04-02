# Dairy Management System — Script Report: Dairy PL Summary

import frappe

def execute(filters=None):
    return get_columns(), get_data(filters)

def get_columns():
    return [
        {"label": "Product", "fieldname": "product", "fieldtype": "Link", "options": "Item", "width": 160},
        {"label": "Qty Produced", "fieldname": "qty_produced", "fieldtype": "Float", "width": 120},
        {"label": "Raw Milk (L)", "fieldname": "raw_milk_litres", "fieldtype": "Float", "width": 120},
        {"label": "Procurement Cost", "fieldname": "procurement_cost", "fieldtype": "Currency", "width": 140},
        {"label": "Yield %", "fieldname": "yield_pct", "fieldtype": "Percent", "width": 90},
    ]

def get_data(filters):
    if not filters: filters = {}
    conditions = "bp.docstatus = 1"
    values = {}

    if filters.get("from_date"):
        conditions += " AND bp.production_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND bp.production_date <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    return frappe.db.sql(f"""
        SELECT bp.product,
               SUM(bp.quantity_produced) AS qty_produced,
               SUM(bp.raw_milk_used_litres) AS raw_milk_litres,
               AVG(bp.yield_percentage) AS yield_pct,
               0 AS procurement_cost
        FROM `tabBatch Production` bp
        WHERE {conditions}
        GROUP BY bp.product
        ORDER BY qty_produced DESC
    """, values, as_dict=True)
