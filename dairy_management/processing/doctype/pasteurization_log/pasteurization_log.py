import frappe
from frappe.model.document import Document

class PasteurizationLog(Document):
    def validate(self):
        if self.method == "HTST":
            if self.target_temperature_c and self.target_temperature_c < 72:
                frappe.throw("HTST requires minimum target temperature of 72°C.")
            if self.hold_time_seconds and self.hold_time_seconds < 15:
                frappe.throw("HTST requires minimum hold time of 15 seconds.")
