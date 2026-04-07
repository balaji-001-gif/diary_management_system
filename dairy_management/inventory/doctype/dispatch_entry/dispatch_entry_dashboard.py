from frappe import _

def get_data(data=None):
    return {
        "fieldname": "dispatch_entry",
        "transactions": [
            {
                "label": _("Inventory and Billing"),
                "items": ["Stock Entry", "Sales Invoice"]
            }
        ]
    }
