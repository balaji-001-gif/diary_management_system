from __future__ import unicode_literals

app_name = "dairy_management"
app_title = "Dairy Management"
app_publisher = "Antigravity"
app_description = "Complete Dairy Management System (DMS) — herd, collection, processing, billing"
app_email = "admin@example.com"
app_license = "MIT"
app_version = "1.0.0"

# ── Required Apps ─────────────────────────────────────────────────────────────
required_apps = ["frappe", "erpnext"]

# ── Asset Configuration ────────────────────────────────────────────────────────
app_include_js = "/assets/dairy_management/js/dairy_management.min.js"
app_include_css = "/assets/dairy_management/css/dairy_management.min.css"

# ── Portal Configuration ──────────────────────────────────────────────────────
portal_menu_items = [
    {"title": "My Milk Collection", "route": "/farmer-portal/collection", "role": "Farmer"},
    {"title": "My Payment History", "route": "/farmer-portal/payments", "role": "Farmer"}
]

# ── Fixtures ──────────────────────────────────────────────────────────────────
fixtures = [
    {"dt": "Role", "filters": [["role_name", "in", [
        "Dairy Manager",
        "Milk Collection Supervisor",
        "Lab Technician",
        "Farmer",
        "Route Agent",
    ]]]},
    "Custom Field",
    "Property Setter",
    {
        "dt": "Module Def",
        "filters": [["module_name", "=", "Dairy Management"]]
    },
    {
        "dt": "Workspace",
        "filters": [
            ["name", "=", "Dairy Management"]
        ]
    }
]

# ── Custom Roles ──────────────────────────────────────────────────────────────
roles = [
    {"role_name": "Dairy Manager"},
    {"role_name": "Milk Collection Supervisor"},
    {"role_name": "Lab Technician"},
    {"role_name": "Farmer"},
    {"role_name": "Route Agent"},
]

# ── Scheduler Events ──────────────────────────────────────────────────────────
scheduler_events = {
    "daily": [
        "dairy_management.tasks.generate_daily_milk_summary",
        "dairy_management.tasks.check_animal_vaccination_due",
        "dairy_management.tasks.check_cold_storage_temperature",
    ],
    "weekly": [
        "dairy_management.tasks.generate_farmer_payment_vouchers",
    ],
}

# ── Dashboard Configuration ──────────────────────────────────────────────────
override_doctype_dashboards = {
    "Sales Invoice": "dairy_management.inventory.doctype.dispatch_entry.dispatch_entry_dashboard.get_data"
}

# ── Document Events ───────────────────────────────────────────────────────────
doc_events = {
}

# ── Website ───────────────────────────────────────────────────────────────────
website_route_rules = [
    {"from_route": "/farmer-portal", "to_route": "farmer_portal"},
]

# ── Jinja ─────────────────────────────────────────────────────────────────────
jinja = {
    "methods": [],
    "filters": [],
}
