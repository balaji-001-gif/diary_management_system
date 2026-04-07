import frappe
from frappe.model.document import Document

class DispatchEntry(Document):
    def on_submit(self):
        """Automatically issue stock and optionally create an invoice."""
        self._create_material_issue()
        if self.customer:
            self._create_sales_invoice()

    def on_cancel(self):
        """Cancel the linked stock entry and sales invoice if the dispatch is cancelled."""
        if self.stock_entry:
            try:
                se = frappe.get_doc("Stock Entry", self.stock_entry)
                if se.docstatus == 1:
                    se.cancel()
            except Exception as e:
                frappe.log_error(str(e), "Dispatch Entry: Stock Entry Cancellation Failed")

        if self.sales_invoice:
            try:
                si = frappe.get_doc("Sales Invoice", self.sales_invoice)
                if si.docstatus == 1:
                    si.cancel()
            except Exception as e:
                frappe.log_error(str(e), "Dispatch Entry: Sales Invoice Cancellation Failed")

    def _create_sales_invoice(self):
        """Helper to create a Sales Invoice for the dispatched items."""
        try:
            si = frappe.new_doc("Sales Invoice")
            si.customer = self.customer
            si.posting_date = self.posting_date
            si.dispatch_entry = self.name
            
            for row in self.items:
                si.append("items", {
                    "item_code": row.item_code,
                    "qty": row.qty,
                    "uom": row.uom,
                    "batch_no": row.batch_no,
                    "income_account": frappe.db.get_value("Company", si.company, "default_income_account") or "Sales - BDD"
                })
            
            si.insert(ignore_permissions=True)
            # We keep it as DRAFT so the accountant can review the prices
            self.db_set("sales_invoice", si.name)
            frappe.msgprint(f"<b>Billing Ready:</b> Draft Sales Invoice {si.name} created for {self.customer}.", alert=True)
            
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Dispatch Entry: Sales Invoice Creation Failed")
            frappe.msgprint(f"Failed to create Sales Invoice: {str(e)}", indicator="orange")

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
