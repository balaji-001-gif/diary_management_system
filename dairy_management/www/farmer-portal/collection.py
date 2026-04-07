import frappe
from frappe import _

def get_context(context):
    """Fetch milk collection entries for the logged-in farmer."""
    user = frappe.session.user
    
    # 1. Identify the Farmer record linked to this user's email
    farmer = frappe.db.get_value("Farmer", {"email_id": user}, ["name", "farmer_name"], as_dict=1)
    
    if not farmer:
        context.no_farmer_found = True
        return context

    context.farmer_name = farmer.farmer_name
    
    # 2. Fetch filters from the URL (if any)
    filters = frappe.form_dict
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    
    # 3. Build query conditions
    conditions = {"farmer": farmer.name, "docstatus": 1}
    if from_date:
        conditions["collection_date"] = [">=", from_date]
    if to_date:
        conditions["collection_date"] = ["<=", to_date]

    # 4. Fetch the data
    context.entries = frappe.get_all(
        "Milk Collection Entry",
        filters=conditions,
        fields=["name", "collection_date", "shift", "quantity_litres", "fat_percentage", "snf_percentage", "amount", "grade"],
        order_by="collection_date desc"
    )
    
    return context
