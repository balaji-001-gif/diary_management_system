import frappe
from frappe.model.document import Document
from frappe.utils import flt

class BatchProduction(Document):
    def before_save(self):
        self._calculate_yield()

    def _calculate_yield(self):
        if self.quantity_produced and self.raw_milk_used_litres and self.raw_milk_used_litres > 0:
            self.yield_percentage = flt(self.quantity_produced) / flt(self.raw_milk_used_litres) * 100

    def on_submit(self):
        self._create_stock_entry()

    def _create_stock_entry(self):
        """Auto-create ERPNext Stock Entry (Manufacture) on submit."""
        try:
            se = frappe.new_doc("Stock Entry")
            se.stock_entry_type = "Manufacture"
            se.batch_production = self.name
            se.posting_date = self.production_date
            se.append("items", {
                "item_code": self.product,
                "qty": self.quantity_produced,
                "t_warehouse": self.target_warehouse,
                "batch_no": self.batch_no,
            })
            se.insert(ignore_permissions=True)
            self.db_set("stock_entry", se.name)
            frappe.msgprint(f"Stock Entry {se.name} created.", alert=True)
        except Exception as e:
            frappe.log_error(str(e), "Batch Production: Stock Entry Creation Failed")
