# Dairy Management System — Script Report: Farmer Payment Register

import frappe

def execute(filters=None):
    return get_columns(), get_data(filters)

def get_columns():
    return [
        {"label": "Farmer Invoice", "fieldname": "name", "fieldtype": "Link", "options": "Farmer Invoice", "width": 160},
        {"label": "Farmer", "fieldname": "farmer", "fieldtype": "Link", "options": "Farmer", "width": 140},
        {"label": "Period From", "fieldname": "period_from", "fieldtype": "Date", "width": 110},
        {"label": "Period To", "fieldname": "period_to", "fieldtype": "Date", "width": 110},
        {"label": "Total Litres", "fieldname": "total_litres_supplied", "fieldtype": "Float", "width": 110},
        {"label": "Gross Amount", "fieldname": "gross_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Deductions", "fieldname": "total_deductions", "fieldtype": "Currency", "width": 110},
        {"label": "Net Payable", "fieldname": "net_payable", "fieldtype": "Currency", "width": 120},
        {"label": "Purchase Invoice", "fieldname": "purchase_invoice", "fieldtype": "Link", "options": "Purchase Invoice", "width": 150},
    ]

def get_data(filters):
    if not filters: filters = {}
    conditions = "docstatus IN (0,1)"
    values = {}

    if filters.get("farmer"):
        conditions += " AND farmer = %(farmer)s"
        values["farmer"] = filters["farmer"]
    if filters.get("from_date"):
        conditions += " AND period_from >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND period_to <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    return frappe.db.sql(f"""
        SELECT name, farmer, period_from, period_to, total_litres_supplied,
               gross_amount, total_deductions, net_payable, purchase_invoice
        FROM `tabFarmer Invoice`
        WHERE {conditions}
        ORDER BY period_from DESC, farmer
    """, values, as_dict=True)
