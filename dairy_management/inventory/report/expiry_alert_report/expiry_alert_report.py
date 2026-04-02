# Dairy Management System — Script Report: Expiry Alert Report

import frappe
from frappe.utils import today, getdate, date_diff

def execute(filters=None):
    return get_columns(), get_data(filters)

def get_columns():
    return [
        {"label": "Item", "fieldname": "item", "fieldtype": "Link", "options": "Item", "width": 160},
        {"label": "Batch No", "fieldname": "batch_no", "fieldtype": "Link", "options": "Batch", "width": 130},
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 140},
        {"label": "Expiry Date", "fieldname": "expiry_date", "fieldtype": "Date", "width": 110},
        {"label": "Days to Expiry", "fieldname": "days_to_expiry", "fieldtype": "Int", "width": 120},
        {"label": "Qty Remaining", "fieldname": "quantity_remaining", "fieldtype": "Float", "width": 110},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]

def get_data(filters):
    if not filters: filters = {}
    threshold = filters.get("days_to_expiry", 30)

    return frappe.db.sql("""
        SELECT item, batch_no, warehouse, expiry_date, days_to_expiry,
               quantity_remaining, status
        FROM `tabExpiry Tracker`
        WHERE days_to_expiry <= %(threshold)s
        ORDER BY days_to_expiry ASC
    """, {"threshold": threshold}, as_dict=True)
