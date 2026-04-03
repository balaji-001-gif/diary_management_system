from frappe import _

def get_data():
    return {
        "fieldname": "batch_production",
        "transactions": [
            {
                "label": _("Quality and Inventory"),
                "items": ["Quality Check Inspection", "Stock Entry"]
            }
        ]
    }
