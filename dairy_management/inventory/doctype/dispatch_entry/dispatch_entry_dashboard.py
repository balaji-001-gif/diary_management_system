from frappe import _

def get_data():
    return {
        "fieldname": "dispatch_entry",
        "transactions": [
            {
                "label": _("Inventory Transfer"),
                "items": ["Stock Entry"]
            }
        ]
    }
