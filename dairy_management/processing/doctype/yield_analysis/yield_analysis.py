import frappe
from frappe.model.document import Document
from frappe.utils import flt

class YieldAnalysis(Document):
    def before_save(self):
        if self.raw_milk_input_litres and self.output_quantity and self.raw_milk_input_litres > 0:
            self.yield_percentage = flt(self.output_quantity) / flt(self.raw_milk_input_litres) * 100
