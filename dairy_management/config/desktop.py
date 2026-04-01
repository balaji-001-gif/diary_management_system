from __future__ import unicode_literals
from frappe import _

def get_data():
    return [
        {
            "module_name": "Animal Management",
            "color": "#2e7d32",
            "icon": "octicon octicon-server",
            "type": "module",
            "label": _("Animal Management"),
        },
        {
            "module_name": "Milk Collection",
            "color": "#1565c0",
            "icon": "octicon octicon-beaker",
            "type": "module",
            "label": _("Milk Collection"),
        },
        {
            "module_name": "Processing",
            "color": "#6a1b9a",
            "icon": "octicon octicon-tools",
            "type": "module",
            "label": _("Processing"),
        },
        {
            "module_name": "Procurement",
            "color": "#e65100",
            "icon": "octicon octicon-package",
            "type": "module",
            "label": _("Procurement"),
        },
        {
            "module_name": "Inventory",
            "color": "#00695c",
            "icon": "octicon octicon-database",
            "type": "module",
            "label": _("Inventory"),
        },
        {
            "module_name": "Quality Control",
            "color": "#37474f",
            "icon": "octicon octicon-checklist",
            "type": "module",
            "label": _("Quality Control"),
        },
        {
            "module_name": "Billing",
            "color": "#558b2f",
            "icon": "octicon octicon-credit-card",
            "type": "module",
            "label": _("Billing"),
        },
        {
            "module_name": "Reports",
            "color": "#283593",
            "icon": "octicon octicon-graph",
            "type": "module",
            "label": _("Reports & Analytics"),
        },
    ]
