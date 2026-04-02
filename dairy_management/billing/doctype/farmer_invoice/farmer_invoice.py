import frappe
from frappe.model.document import Document
from frappe.utils import flt

class FarmerInvoice(Document):
    def before_save(self):
        self._calculate_amounts()

    def _calculate_amounts(self):
        self.total_deductions = sum(flt(d.amount) for d in self.deductions)
        self.net_payable = flt(self.gross_amount) - flt(self.total_deductions)

    def on_submit(self):
        self._create_purchase_invoice()

    def _create_purchase_invoice(self):
        """Auto-create ERPNext Purchase Invoice on submit."""
        farmer = frappe.get_doc("Farmer", self.farmer)
        supplier = farmer.supplier
        if not supplier:
            frappe.throw(f"Farmer {self.farmer} does not have a linked ERPNext Supplier.")
        try:
            pi = frappe.new_doc("Purchase Invoice")
            pi.supplier = supplier
            pi.posting_date = self.period_to
            pi.milk_collection_period = f"{self.period_from} to {self.period_to}"
            pi.append("items", {
                "item_code": frappe.db.get_single_value("Dairy Management Settings", "raw_milk_item") or "Raw Milk",
                "qty": self.total_litres_supplied,
                "rate": flt(self.gross_amount) / flt(self.total_litres_supplied) if self.total_litres_supplied else 0,
                "uom": "Litre",
            })
            pi.insert(ignore_permissions=True)
            self.db_set("purchase_invoice", pi.name)
            frappe.msgprint(f"Purchase Invoice {pi.name} created.", alert=True)
        except Exception as e:
            frappe.log_error(str(e), "Farmer Invoice: PI Creation Failed")

def on_submit(doc, method=None):
    """Module-level fallback to satisfy stale hooks.py cache if bench hasn"t restarted."""
    if hasattr(doc, "on_submit"):
        doc.on_submit()
