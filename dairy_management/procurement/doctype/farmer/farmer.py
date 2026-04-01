import frappe
from frappe.model.document import Document

class Farmer(Document):
    def validate(self):
        if self.aadhar_no and len(self.aadhar_no) not in (12, 0):
            frappe.throw("Aadhar Number must be 12 digits.")
