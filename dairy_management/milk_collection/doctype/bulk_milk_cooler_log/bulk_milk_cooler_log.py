import frappe
from frappe.model.document import Document

class BulkMilkCoolerLog(Document):
    def validate(self):
        center = frappe.db.get_value("Collection Center", {"bmc_id": self.bmc_id}, "target_temp_c")
        threshold = center or 4.0
        if self.morning_temp_c and self.morning_temp_c > threshold + 2:
            frappe.msgprint(f"⚠️ Morning temperature {self.morning_temp_c}°C exceeds target {threshold}°C.", alert=True)
        if self.evening_temp_c and self.evening_temp_c > threshold + 2:
            frappe.msgprint(f"⚠️ Evening temperature {self.evening_temp_c}°C exceeds target {threshold}°C.", alert=True)
