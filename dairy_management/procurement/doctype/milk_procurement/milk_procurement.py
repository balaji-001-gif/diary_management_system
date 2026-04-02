import frappe
from frappe.model.document import Document
from frappe.utils import flt

class MilkProcurement(Document):
    def before_save(self):
        self.total_amount = flt(self.quantity_litres) * flt(self.agreed_rate_per_litre)

    def _create_purchase_receipt(self):
        """Auto-create ERPNext Purchase Receipt on submit."""
        settings = frappe.get_single("Dairy Management Settings")
        
        if not settings.raw_milk_item or not settings.raw_milk_warehouse:
            frappe.msgprint("<b>Step 2 (Purchase Receipt) Failed:</b><br>Please configure 'Raw Milk Item' and 'Default Raw Milk Warehouse' in <b>Dairy Management Settings</b>.", alert=True, indicator="orange")
            return

        try:
            pr = frappe.new_doc("Purchase Receipt")
            pr.supplier = self.supplier
            pr.posting_date = self.receipt_date
            pr.append("items", {
                "item_code": settings.raw_milk_item,
                "qty": self.quantity_litres,
                "rate": self.agreed_rate_per_litre,
                "uom": "Litre",
                "warehouse": settings.raw_milk_warehouse,
            })
            pr.insert(ignore_permissions=True)
            self.db_set("purchase_receipt", pr.name)
            frappe.msgprint(f"<b>Step 2 Success:</b> Purchase Receipt {pr.name} created.", alert=True)
        except Exception as e:
            frappe.log_error(str(e), "Milk Procurement: PR Creation Failed")
            frappe.msgprint("<b>Step 2 Failed:</b> Check Error Log for details.", alert=True, indicator="red")

def on_submit(doc, method=None):
    """Module-level fallback to satisfy stale hooks.py cache if bench hasn"t restarted."""
    if hasattr(doc, "on_submit"):
        doc.on_submit()
