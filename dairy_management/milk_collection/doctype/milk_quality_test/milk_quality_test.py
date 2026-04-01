import frappe
from frappe.model.document import Document

class MilkQualityTest(Document):
    def validate(self):
        self._auto_set_result()

    def _auto_set_result(self):
        if not self.result:
            if self.fat and self.snf:
                if self.fat >= 3.5 and self.snf >= 8.5 and self.adulteration_passed:
                    self.result = "Pass"
                else:
                    self.result = "Fail"
