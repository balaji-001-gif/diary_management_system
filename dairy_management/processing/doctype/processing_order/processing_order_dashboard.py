from frappe import _

def get_data():
    return {
        "fieldname": "processing_order",
        "transactions": [
            {
                "label": _("Production"),
                "items": ["Batch Production"]
            }
        ]
    }
