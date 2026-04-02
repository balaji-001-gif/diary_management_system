import frappe
from frappe.model.document import Document

class ProcessingOrder(Document):
    def on_submit(self):
        self._create_work_order()

    def _create_work_order(self):
        """Auto-create ERPNext Work Order on submit."""
        settings = frappe.get_single("Dairy Management Settings")
        
        if not self.bom:
            frappe.msgprint("<b>Step 4 Failed:</b> Please link a BOM first.", alert=True, indicator="orange")
            return
            
        if not settings.finished_goods_warehouse:
            frappe.msgprint("<b>Step 4 Failed:</b> Please configure 'Default Finished Goods Warehouse' in <b>Dairy Management Settings</b>.", alert=True, indicator="orange")
            return

        try:
            wo = frappe.new_doc("Work Order")
            wo.production_item = self.product
            wo.bom_no = self.bom
            wo.qty = self.planned_quantity
            wo.planned_start_date = self.planned_start_date
            wo.fg_warehouse = settings.finished_goods_warehouse
            wo.insert(ignore_permissions=True)
            
            self.db_set("work_order", wo.name)
            self.db_set("status", "In Progress")
            frappe.msgprint(f"<b>Step 4 Success:</b> Work Order {wo.name} created.", alert=True)
        except Exception as e:
            frappe.log_error(str(e), "Processing Order: Work Order Creation Failed")
            frappe.msgprint("<b>Step 4 Failed:</b> Check Error Log for details.", alert=True, indicator="red")

def on_submit(doc, method=None):
    """Module-level fallback to satisfy stale hooks.py cache if bench hasn"t restarted."""
    if hasattr(doc, "on_submit"):
        doc.on_submit()
