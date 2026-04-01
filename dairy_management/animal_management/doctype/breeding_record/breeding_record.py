import frappe
from frappe.model.document import Document

class BreedingRecord(Document):
    def validate(self):
        if self.calving_date and self.breeding_date and self.calving_date < self.breeding_date:
            frappe.throw("Calving Date cannot be before Breeding Date.")
        if self.confirmation_date and self.breeding_date and self.confirmation_date < self.breeding_date:
            frappe.throw("Confirmation Date cannot be before Breeding Date.")
