"""
dairy_management/utils/reports.py
Shared helper functions for Script Reports
"""
import frappe
from frappe.utils import flt


def get_date_range_condition(date_field, from_date, to_date, alias=None):
    prefix = f"`{alias}`." if alias else ""
    conditions = []
    if from_date:
        conditions.append(f"{prefix}`{date_field}` >= %(from_date)s")
    if to_date:
        conditions.append(f"{prefix}`{date_field}` <= %(to_date)s")
    return " AND ".join(conditions)


def sum_column(data, column_key):
    return flt(sum(row.get(column_key, 0) or 0 for row in data))
