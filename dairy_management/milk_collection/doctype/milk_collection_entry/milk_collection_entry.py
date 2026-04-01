import frappe
from frappe.model.document import Document
from dairy_management.utils.calculations import calculate_collection_amount

class MilkCollectionEntry(Document):
    def before_save(self):
        calculate_collection_amount(self)

    def validate(self):
        if self.quantity_litres and self.quantity_litres <= 0:
            frappe.throw("Quantity must be greater than 0.")
        if self.fat_percentage and (self.fat_percentage < 0 or self.fat_percentage > 15):
            frappe.throw("Fat % must be between 0 and 15.")
        if self.snf_percentage and (self.snf_percentage < 0 or self.snf_percentage > 15):
            frappe.throw("SNF % must be between 0 and 15.")

    def on_submit(self):
        self._auto_create_quality_test()

    def _auto_create_quality_test(self):
        if not frappe.db.exists("Milk Quality Test", {"collection_entry": self.name}):
            qc = frappe.new_doc("Milk Quality Test")
            qc.collection_entry = self.name
            qc.test_date = self.collection_date
            qc.fat = self.fat_percentage
            qc.snf = self.snf_percentage
            qc.insert(ignore_permissions=True)
            frappe.msgprint(f"Milk Quality Test {qc.name} auto-created.", alert=True)
