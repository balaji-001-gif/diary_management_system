import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    # Ensure custom fields exist on Stock Entry for traceability
    custom_fields = {
        "Stock Entry": [
            {
                "fieldname": "dispatch_entry",
                "label": "Dispatch Entry",
                "fieldtype": "Link",
                "options": "Dispatch Entry",
                "insert_after": "naming_series",
                "read_only": 1
            },
            {
                "fieldname": "batch_production",
                "label": "Batch Production",
                "fieldtype": "Link",
                "options": "Batch Production",
                "insert_after": "dispatch_entry",
                "read_only": 1
            }
        ],
        "Sales Invoice": [
            {
                "fieldname": "dispatch_entry",
                "label": "Dispatch Entry",
                "fieldtype": "Link",
                "options": "Dispatch Entry",
                "insert_after": "customer",
                "read_only": 1
            }
        ],
        "Purchase Invoice": [
            {
                "fieldname": "custom_farmer_invoice",
                "label": "Farmer Invoice",
                "fieldtype": "Link",
                "options": "Farmer Invoice",
                "insert_after": "supplier",
                "read_only": 1
            }
        ]
    }
    
    create_custom_fields(custom_fields, ignore_validate=True)
    frappe.db.commit()
    print("✅ Custom fields for Traceability added to Stock Entry.")
