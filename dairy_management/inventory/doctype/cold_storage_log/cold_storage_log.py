import frappe
from frappe.model.document import Document
from frappe.utils import flt

class ColdStorageLog(Document):
    def before_save(self):
        self._calculate_min_max()

    def _calculate_min_max(self):
        if not self.readings:
            return
        temps = [r.temperature_c for r in self.readings if r.temperature_c is not None]
        if temps:
            self.min_temp_recorded_c = min(temps)
            self.max_temp_recorded_c = max(temps)
            
            # Safe lookup for warehouse-specific threshold
            threshold = 4.0
            if frappe.get_meta("Warehouse").has_field("custom_target_temp_c"):
                threshold = frappe.db.get_value("Warehouse", self.warehouse, "custom_target_temp_c") or 4.0
                
            self.temperature_breach = 1 if self.max_temp_recorded_c > flt(threshold) + 1 else 0
