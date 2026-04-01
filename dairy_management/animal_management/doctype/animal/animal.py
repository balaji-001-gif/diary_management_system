import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, today

class Animal(Document):
    def validate(self):
        if self.date_of_birth and self.date_of_birth > today():
            frappe.throw("Date of Birth cannot be in the future.")

    def get_age_months(self):
        if self.date_of_birth:
            return date_diff(today(), self.date_of_birth) // 30
        return 0
