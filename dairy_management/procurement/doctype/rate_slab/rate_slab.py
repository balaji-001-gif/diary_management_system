import frappe
from frappe.model.document import Document

class RateSlab(Document):
    def validate(self):
        if self.effective_to and self.effective_from and self.effective_to < self.effective_from:
            frappe.throw("Effective To date cannot be before Effective From date.")
