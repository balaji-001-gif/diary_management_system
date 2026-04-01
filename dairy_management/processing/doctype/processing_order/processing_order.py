import frappe
from frappe.model.document import Document

class ProcessingOrder(Document):
    def on_submit(self):
        self._create_work_order()

    def _create_work_order(self):
        """Auto-create ERPNext Work Order on submit."""
        if not self.bom:
            frappe.msgprint("No BOM linked — Work Order not created.", alert=True)
            return
        try:
            wo = frappe.new_doc("Work Order")
            wo.production_item = self.product
            wo.bom_no = self.bom
            wo.qty = self.planned_quantity
            wo.planned_start_date = self.planned_start_date
            wo.insert(ignore_permissions=True)
            self.db_set("work_order", wo.name)
            self.db_set("status", "In Progress")
            frappe.msgprint(f"Work Order {wo.name} created.", alert=True)
        except Exception as e:
            frappe.log_error(str(e), "Processing Order: Work Order Creation Failed")
