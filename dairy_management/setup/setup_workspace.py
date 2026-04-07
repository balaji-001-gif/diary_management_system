import frappe
import json

def execute():
    # Ensure Module Def exists first
    if not frappe.db.exists("Module Def", "Dairy Management"):
        module = frappe.new_doc("Module Def")
        module.module_name = "Dairy Management"
        module.app_name = "dairy_management"
        module.insert(ignore_permissions=True)
        frappe.db.commit()
        print("✅ Module Def created")

    # Define the hierarchical workspace structure
    dashboards = {
        "Animal Management": [
            {"id": "663f79a2", "type": "card", "data": {"card_name": "Animal Management", "links": [
                {"type": "link", "label": "Animal", "link_to": "Animal", "link_type": "DocType"},
                {"type": "link", "label": "Breed", "link_to": "Breed", "link_type": "DocType"},
                {"type": "link", "label": "Health Record", "link_to": "Health Record", "link_type": "DocType"},
                {"type": "link", "label": "Breeding Record", "link_to": "Breeding Record", "link_type": "DocType"},
                {"type": "link", "label": "Lactation Cycle", "link_to": "Lactation Cycle", "link_type": "DocType"}
            ]}}
        ],
        "Milk Collection": [
            {"id": "bc430189", "type": "shortcut", "data": {"shortcut_name": "Milk Collection Entry", "col": 3}},
            {"id": "d10b15e4", "type": "card", "data": {"card_name": "Milk Collection", "links": [
                {"type": "link", "label": "Collection Center", "link_to": "Collection Center", "link_type": "DocType"},
                {"type": "link", "label": "Milk Collection Entry", "link_to": "Milk Collection Entry", "link_type": "DocType"},
                {"type": "link", "label": "Milk Quality Test", "link_to": "Milk Quality Test", "link_type": "DocType"},
                {"type": "link", "label": "Shift Summary", "link_to": "Shift Summary", "link_type": "DocType"},
                {"type": "link", "label": "Bulk Milk Cooler Log", "link_to": "Bulk Milk Cooler Log", "link_type": "DocType"},
                {"type": "link", "label": "Rejection Record", "link_to": "Rejection Record", "link_type": "DocType"}
            ]}}
        ],
        "Procurement": [
            {"id": "c9d8c501", "type": "shortcut", "data": {"shortcut_name": "Milk Procurement", "col": 3}},
            {"id": "701613b8", "type": "card", "data": {"card_name": "Procurement", "links": [
                {"type": "link", "label": "Milk Route", "link_to": "Milk Route", "link_type": "DocType"},
                {"type": "link", "label": "Rate Slab", "link_to": "Rate Slab", "link_type": "DocType"},
                {"type": "link", "label": "Farmer", "link_to": "Farmer", "link_type": "DocType"},
                {"type": "link", "label": "Milk Procurement", "link_to": "Milk Procurement", "link_type": "DocType"},
                {"type": "link", "label": "Deduction Master", "link_to": "Deduction Master", "link_type": "DocType"},
                {"type": "link", "label": "Procurement Payment", "link_to": "Procurement Payment", "link_type": "DocType"}
            ]}}
        ],
        "Processing": [
            {"id": "6903a06c", "type": "shortcut", "data": {"shortcut_name": "Batch Production", "col": 3}},
            {"id": "c9d8c502", "type": "shortcut", "data": {"shortcut_name": "Processing Order", "col": 3}},
            {"id": "2597a9ff", "type": "card", "data": {"card_name": "Procurement & Planning", "links": [
                {"type": "link", "label": "Product Formula", "link_to": "Product Formula", "link_type": "DocType"},
                {"type": "link", "label": "Processing Order", "link_to": "Processing Order", "link_type": "DocType"},
                {"type": "link", "label": "Batch Production", "link_to": "Batch Production", "link_type": "DocType"},
                {"type": "link", "label": "Yield Analysis", "link_to": "Yield Analysis", "link_type": "DocType"}
            ]}},
            {"id": "5297a9fe", "type": "card", "data": {"card_name": "Factory Logs", "links": [
                {"type": "link", "label": "Pasteurization Log", "link_to": "Pasteurization Log", "link_type": "DocType"},
                {"type": "link", "label": "Packaging Record", "link_to": "Packaging Record", "link_type": "DocType"},
                {"type": "link", "label": "Plant Downtime Log", "link_to": "Plant Downtime Log", "link_type": "DocType"}
            ]}}
        ],
        "Inventory": [
            {"id": "b91257ed", "type": "shortcut", "data": {"shortcut_name": "Dispatch Entry", "col": 3}},
            {"id": "b91257ec", "type": "card", "data": {"card_name": "Inventory", "links": [
                {"type": "link", "label": "Crate Container Master", "link_to": "Crate Container Master", "link_type": "DocType"},
                {"type": "link", "label": "Temperature Reading", "link_to": "Temperature Reading", "link_type": "DocType"},
                {"type": "link", "label": "Cold Storage Log", "link_to": "Cold Storage Log", "link_type": "DocType"},
                {"type": "link", "label": "Expiry Tracker", "link_to": "Expiry Tracker", "link_type": "DocType"},
                {"type": "link", "label": "Delivery Route", "link_to": "Delivery Route", "link_type": "DocType"},
                {"type": "link", "label": "Dispatch Entry", "link_to": "Dispatch Entry", "link_type": "DocType"}
            ]}}
        ],
        "Quality Control": [
            {"id": "d7710594", "type": "card", "data": {"card_name": "Quality Control", "links": [
                {"type": "link", "label": "Quality Check Parameter", "link_to": "Quality Check Parameter", "link_type": "DocType"},
                {"type": "link", "label": "Lab Test Template", "link_to": "Lab Test Template", "link_type": "DocType"},
                {"type": "link", "label": "Quality Check Result", "link_to": "Quality Check Result", "link_type": "DocType"},
                {"type": "link", "label": "Quality Check Inspection", "link_to": "Quality Check Inspection", "link_type": "DocType"},
                {"type": "link", "label": "Compliance Log", "link_to": "Compliance Log", "link_type": "DocType"},
                {"type": "link", "label": "Supplier Milk Rejection Log", "link_to": "Supplier Milk Rejection Log", "link_type": "DocType"},
                {"type": "link", "label": "Equipment Calibration Log", "link_to": "Equipment Calibration Log", "link_type": "DocType"}
            ]}}
        ],
        "Billing": [
            {"id": "12fcf34a", "type": "shortcut", "data": {"shortcut_name": "Farmer Invoice", "col": 3}},
            {"id": "4628ca14", "type": "card", "data": {"card_name": "Billing", "links": [
                {"type": "link", "label": "Farmer Invoice", "link_to": "Farmer Invoice", "link_type": "DocType"},
                {"type": "link", "label": "Advance Loan", "link_to": "Advance Loan", "link_type": "DocType"},
                {"type": "link", "label": "Deduction Voucher", "link_to": "Deduction Voucher", "link_type": "DocType"},
                {"type": "link", "label": "Milk Price Revision", "link_to": "Milk Price Revision", "link_type": "DocType"},
                {"type": "link", "label": "Payment Cycle Setting", "link_to": "Payment Cycle Setting", "link_type": "DocType"},
                {"type": "link", "label": "Cooperative Member", "link_to": "Cooperative Member", "link_type": "DocType"}
            ]}}
        ],
        "Reports": [
            {"id": "c461d21a", "type": "card", "data": {"card_name": "Reports", "links": [
                {"type": "link", "label": "Herd Yield Report", "link_to": "Herd Yield Report", "link_type": "Report"},
                {"type": "link", "label": "Animal Health Calendar", "link_to": "Animal Health Calendar", "link_type": "Report"},
                {"type": "link", "label": "Milk Procurement Summary", "link_to": "Milk Procurement Summary", "link_type": "Report"},
                {"type": "link", "label": "Processing Yield Report", "link_to": "Processing Yield Report", "link_type": "Report"},
                {"type": "link", "label": "Dispatch Summary", "link_to": "Dispatch Summary", "link_type": "Report"},
                {"type": "link", "label": "Cold Chain Compliance", "link_to": "Cold Chain Compliance", "link_type": "Report"},
                {"type": "link", "label": "Expiry Alert Report", "link_to": "Expiry Alert Report", "link_type": "Report"},
                {"type": "link", "label": "Farmer Payment Register", "link_to": "Farmer Payment Register", "link_type": "Report"},
                {"type": "link", "label": "Dairy PL Summary", "link_to": "Dairy PL Summary", "link_type": "Report"}
            ]}}
        ],
        "Settings": [
            {"id": "s88119ae", "type": "card", "data": {"card_name": "Settings", "links": [
                {"type": "link", "label": "Dairy Management Settings", "link_to": "Dairy Management Settings", "link_type": "DocType"}
            ]}}
        ]
    }

    # 1. Create or ensure the Parent Dairy Management Group exists
    if not frappe.db.exists("Workspace", "Dairy Management"):
        ws_parent = frappe.new_doc("Workspace")
        ws_parent.name = "Dairy Management"
    else:
        ws_parent = frappe.get_doc("Workspace", "Dairy Management")
        
    ws_parent.label = "Dairy Management"
    ws_parent.title = "Dairy Management"
    ws_parent.module = "Dairy Management"
    ws_parent.public = 1
    ws_parent.is_hidden = 0
    ws_parent.sequence_id = 1.0
    ws_parent.content = "[]" 
    ws_parent.save(ignore_permissions=True)
    
    # 2. Iterate and create children Workspaces
    seq_id = 2.0
    for name, content_list in dashboards.items():
        if not frappe.db.exists("Workspace", name):
            ws_child = frappe.new_doc("Workspace")
            ws_child.name = name
        else:
            ws_child = frappe.get_doc("Workspace", name)

        ws_child.label = name
        ws_child.title = name
        ws_child.module = "Dairy Management"
        ws_child.parent_page = "Dairy Management" # Nests it under parent
        ws_child.public = 1
        ws_child.is_hidden = 0
        ws_child.sequence_id = seq_id
        ws_child.content = json.dumps(content_list)
        ws_child.save(ignore_permissions=True)
        seq_id += 1.0

    frappe.db.commit()
    frappe.clear_cache()
    print("✅ Split Modular Workspaces updated and Cache cleared successfully.")
