# Dairy Management System — Script Report: Milk Procurement Summary

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Farmer", "fieldname": "farmer", "fieldtype": "Link", "options": "Farmer", "width": 160},
        {"label": "Route", "fieldname": "route", "fieldtype": "Link", "options": "Milk Route", "width": 130},
        {"label": "Date", "fieldname": "collection_date", "fieldtype": "Date", "width": 110},
        {"label": "Shift", "fieldname": "shift", "fieldtype": "Data", "width": 90},
        {"label": "Qty (L)", "fieldname": "quantity_litres", "fieldtype": "Float", "width": 90},
        {"label": "Fat %", "fieldname": "fat_percentage", "fieldtype": "Float", "width": 80},
        {"label": "SNF %", "fieldname": "snf_percentage", "fieldtype": "Float", "width": 80},
        {"label": "Rate/L", "fieldname": "rate_per_litre", "fieldtype": "Currency", "width": 100},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
    ]

def get_data(filters):
    if not filters: filters = {}
    conditions = "docstatus = 1"
    values = {}

    if filters.get("farmer"):
        conditions += " AND farmer = %(farmer)s"
        values["farmer"] = filters["farmer"]
    if filters.get("route"):
        conditions += " AND route = %(route)s"
        values["route"] = filters["route"]
    if filters.get("from_date"):
        conditions += " AND collection_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND collection_date <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    return frappe.db.sql(f"""
        SELECT farmer, route, collection_date, shift, quantity_litres,
               fat_percentage, snf_percentage, rate_per_litre, amount
        FROM `tabMilk Collection Entry`
        WHERE {conditions}
        ORDER BY collection_date DESC, farmer
    """, values, as_dict=True)
