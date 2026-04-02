import frappe
from frappe.model.document import Document

class ProcessingOrder(Document):
    def on_submit(self):
        # In the simplified flow, submission only marks the plan as ready.
        # No Work Order is created.
        self.db_set("status", "In Progress")
        frappe.msgprint("<b>Plan Ready:</b> You can now proceed to Batch Production.", alert=True)

def on_submit(doc, method=None):
    """Module-level fallback."""
    if hasattr(doc, "on_submit"):
        doc.on_submit()
