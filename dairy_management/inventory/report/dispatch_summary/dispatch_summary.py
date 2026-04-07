import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data, None, None, None, "Dispatch Entry"

def get_columns():
    return [
        {"label": "Route", "fieldname": "route", "fieldtype": "Link", "options": "Delivery Route", "width": 150},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
        {"label": "Product", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 200},
        {"label": "Dispatch Qty", "fieldname": "qty", "fieldtype": "Float", "width": 120},
        {"label": "UOM", "fieldname": "uom", "fieldtype": "Link", "options": "UOM", "width": 100},
        {"label": "Batch No", "fieldname": "batch_no", "fieldtype": "Link", "options": "Batch", "width": 150},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Dispatch ID", "fieldname": "name", "fieldtype": "Link", "options": "Dispatch Entry", "width": 150}
    ]

def get_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += f" AND de.posting_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND de.posting_date <= '{filters['to_date']}'"
    if filters.get("route"):
        conditions += f" AND de.route = '{filters['route']}'"

    return frappe.db.sql(f"""
        SELECT 
            de.route, de.posting_date, dei.item_code, dei.qty, dei.uom, dei.batch_no, de.customer, de.name
        FROM 
            `tabDispatch Entry` de
        JOIN 
            `tabDispatch Entry Item` dei ON dei.parent = de.name
        WHERE 
            de.docstatus = 1 {conditions}
        ORDER BY 
            de.posting_date DESC, de.route ASC
    """, as_dict=1)
