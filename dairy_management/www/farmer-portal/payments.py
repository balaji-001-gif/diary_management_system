import frappe

def get_context(context):
    """Fetch payment and deduction history for the logged-in farmer."""
    user = frappe.session.user
    
    # 1. Identify by Name (Farmer Code/Username) or fallback to Email
    farmer = frappe.db.get_value("Farmer", {"name": user}, ["name", "farmer_name", "supplier"], as_dict=1)
    if not farmer:
        farmer = frappe.db.get_value("Farmer", {"email_id": user}, ["name", "farmer_name", "supplier"], as_dict=1)
    
    if not farmer:
        context.no_farmer_found = True
        return context

    context.farmer_name = farmer.farmer_name

    # 1. Fetch Deduction Vouchers (Standalone DocType we built)
    context.deductions = frappe.get_all(
        "Deduction Voucher",
        filters={"farmer": farmer.name, "docstatus": 1},
        fields=["name", "posting_date", "deduction_type", "amount", "remarks"],
        order_by="posting_date desc"
    )
    
    # 2. Fetch standard Expense/Payment items from ERPNext (if linked to Supplier)
    if farmer.supplier:
        context.invoices = frappe.get_all(
            "Purchase Invoice",
            filters={"supplier": farmer.supplier, "docstatus": 1},
            fields=["name", "posting_date", "grand_total", "status"],
            order_by="posting_date desc",
            limit=5
        )
    
    return context
