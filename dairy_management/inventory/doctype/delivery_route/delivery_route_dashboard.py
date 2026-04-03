from frappe import _

def get_data():
    return {
        "fieldname": "route",
        "transactions": [
            {
                "label": _("Distribution"),
                "items": ["Dispatch Entry"]
            }
        ]
    }
