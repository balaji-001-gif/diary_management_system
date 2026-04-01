import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, flt

class LactationCycle(Document):
    def validate(self):
        if self.dry_off_date and self.start_date and self.dry_off_date < self.start_date:
            frappe.throw("Dry-off Date cannot be before Start Date.")
        self._calculate_avg_daily_yield()

    def _calculate_avg_daily_yield(self):
        if self.total_yield_litres and self.start_date and self.dry_off_date:
            days = date_diff(self.dry_off_date, self.start_date)
            if days > 0:
                self.avg_daily_yield = flt(self.total_yield_litres) / days
