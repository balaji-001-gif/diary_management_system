"""
dairy_management/utils/validators.py
General validation helpers for the DMS app
"""
import frappe
from frappe.utils import today, getdate


def validate_date_not_future(date_val, label="Date"):
    if date_val and getdate(date_val) > getdate(today()):
        frappe.throw(f"{label} cannot be in the future.")


def validate_positive(value, label="Value"):
    if value is not None and value < 0:
        frappe.throw(f"{label} cannot be negative.")


def validate_percentage(value, label="Percentage", min_val=0.0, max_val=100.0):
    if value is not None and not (min_val <= value <= max_val):
        frappe.throw(f"{label} must be between {min_val} and {max_val}.")
