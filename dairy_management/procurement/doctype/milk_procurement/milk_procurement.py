import frappe
from frappe.model.document import Document
from frappe.utils import flt

class MilkProcurement(Document):
    def before_save(self):
        self.total_amount = flt(self.quantity_litres) * flt(self.agreed_rate_per_litre)

    def on_submit(self):
        self._create_purchase_receipt()

    def _create_purchase_receipt(self):
        """Auto-create ERPNext Purchase Receipt on submit."""
        try:
            pr = frappe.new_doc("Purchase Receipt")
            pr.supplier = self.supplier
            pr.posting_date = self.receipt_date
            pr.append("items", {
                "item_code": frappe.db.get_single_value("Dairy Management Settings", "raw_milk_item") or "Raw Milk",
                "qty": self.quantity_litres,
                "rate": self.agreed_rate_per_litre,
                "uom": "Litre",
                "warehouse": frappe.db.get_single_value("Dairy Management Settings", "raw_milk_warehouse") or "",
            })
            pr.insert(ignore_permissions=True)
            self.db_set("purchase_receipt", pr.name)
            frappe.msgprint(f"Purchase Receipt {pr.name} created.", alert=True)
        except Exception as e:
            frappe.log_error(str(e), "Milk Procurement: PR Creation Failed")
