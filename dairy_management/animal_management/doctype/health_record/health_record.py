import frappe
from frappe.model.document import Document

class HealthRecord(Document):
    def validate(self):
        if self.next_due_date and self.date and self.next_due_date < self.date:
            frappe.throw("Next Due Date cannot be before the Event Date.")
