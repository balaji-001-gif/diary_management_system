import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, today, getdate

class ExpiryTracker(Document):
    def before_save(self):
        if self.expiry_date:
            self.days_to_expiry = date_diff(getdate(self.expiry_date), getdate(today()))
            if self.days_to_expiry < 0:
                self.status = "Expired"
            elif self.days_to_expiry <= 7:
                self.status = "Near Expiry"
            else:
                self.status = "Safe"
