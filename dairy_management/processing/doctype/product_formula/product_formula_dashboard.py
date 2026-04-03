from frappe import _

def get_data():
    return {
        "fieldname": "product_formula",
        "transactions": [
            {
                "label": _("Planning"),
                "items": ["Processing Order"]
            }
        ]
    }
