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
        self._ensure_batch_exists()
        self._create_stock_entry()

    def _ensure_batch_exists(self):
        """Automatically create ERPNext Batch if it doesn"t exist for the item."""
        if not self.batch_no:
            return

        if not frappe.db.exists("Batch", self.batch_no):
            try:
                batch = frappe.new_doc("Batch")
                batch.batch_id = self.batch_no
                batch.item = self.product
                batch.expiry_date = self.expiry_date
                batch.insert(ignore_permissions=True)
                frappe.msgprint(f"Batch {self.batch_no} created.", alert=True)
            except Exception as e:
                frappe.log_error(str(e), "Batch Production: Batch Creation Failed")

    def _create_stock_entry(self):
        """Auto-create ERPNext Stock Entry (Repack) for the simplified dairy flow."""
        settings = frappe.get_single("Dairy Management Settings")
        
        if not self.target_warehouse:
            frappe.msgprint("<b>Step 6 Failed:</b> Please select a <b>Target Warehouse</b> for the finished milk.", alert=True, indicator="orange")
            return

        if not settings.raw_milk_warehouse:
            frappe.msgprint("<b>Step 6 Failed:</b> Please configure 'Default Raw Milk Warehouse' in <b>Dairy Management Settings</b>.", alert=True, indicator="orange")
            return

        try:
            se = frappe.new_doc("Stock Entry")
            se.stock_entry_type = "Repack"
            se.batch_production = self.name
            se.posting_date = self.production_date
            
            # Row 1: SOURCE - Consume Raw Milk
            se.append("items", {
                "item_code": settings.raw_milk_item or "Raw Milk",
                "qty": self.raw_milk_used_litres,
                "s_warehouse": settings.raw_milk_warehouse,
                "uom": "Litre",
                "is_finished_item": 0,
            })
            
            # Row 2: TARGET - Produce Finished Product
            se.append("items", {
                "item_code": self.product,
                "qty": self.quantity_produced,
                "t_warehouse": self.target_warehouse,
                "is_finished_item": 1,
                "batch_no": self.batch_no,
            })
            
            se.insert(ignore_permissions=True)
            self.db_set("stock_entry", se.name)
            frappe.msgprint(f"<b>Step 6 Success:</b> Created Repack Stock Entry {se.name}.", alert=True)
        except Exception as e:
            frappe.log_error(str(e), "Batch Production: Stock Entry (Repack) Creation Failed")
            frappe.msgprint("<b>Step 6 Failed:</b> Check Error Log for details.", alert=True, indicator="red")

@frappe.whitelist()
def get_processing_order_details(processing_order):
    """Utility to auto-fill Batch Production fields from the linked Work Order."""
    po = frappe.get_doc("Processing Order", processing_order)
    
    # Defaults from Processing Order
    data = {
        "product": po.product,
        "quantity_produced": po.planned_quantity,
        "raw_milk_used_litres": po.raw_milk_required_litres,
        "target_warehouse": frappe.db.get_single_value("Dairy Management Settings", "finished_goods_warehouse")
    }
    
    # If a Work Order exists, it is the source of truth for production
    if po.work_order:
        wo = frappe.get_doc("Work Order", po.work_order)
        data.update({
            "quantity_produced": wo.qty,
            "product": wo.production_item
        })
        
    return data

def on_submit(doc, method=None):
    """Module-level fallback to satisfy stale hooks.py cache if bench hasn"t restarted."""
    if hasattr(doc, "on_submit"):
        doc.on_submit()
