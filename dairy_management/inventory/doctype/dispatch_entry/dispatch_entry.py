import frappe
from frappe.model.document import Document

class DispatchEntry(Document):
    def on_submit(self):
        """Automatically issue stock from the warehouse when a dispatch is confirmed."""
        self._create_material_issue()

    def on_cancel(self):
        """Cancel the linked stock entry if the dispatch is cancelled."""
        if self.stock_entry:
            try:
                se = frappe.get_doc("Stock Entry", self.stock_entry)
                if se.docstatus == 1:
                    se.cancel()
                frappe.msgprint(f"Linked Stock Entry {self.stock_entry} has been cancelled.", alert=True)
            except Exception as e:
                frappe.log_error(str(e), "Dispatch Entry: Stock Entry Cancellation Failed")

    def _create_material_issue(self):
        """Helper to create and submit a Material Issue Stock Entry for the dispatch."""
        if not self.items:
            frappe.throw("No items to dispatch. Please add products to the list.")

        try:
            se = frappe.new_doc("Stock Entry")
            se.stock_entry_type = "Material Issue"
            se.dispatch_entry = self.name # Assuming a custom field or manual link
            se.posting_date = self.posting_date
            
            for row in self.items:
                se.append("items", {
                    "item_code": row.item_code,
                    "qty": row.qty,
                    "s_warehouse": self.source_warehouse,
                    "batch_no": row.batch_no,
                    "uom": row.uom
                })
            
            se.insert(ignore_permissions=True)
            se.submit()
            
            self.db_set("stock_entry", se.name)
            frappe.msgprint(f"<b>Dispatch Successful:</b> Created and Submitted Material Issue {se.name}.", alert=True)
            
        except Exception as e:
            frappe.log_error(str(e), "Dispatch Entry: Stock Issue Failed")
            frappe.throw(f"Inventory update failed: {str(e)}")
