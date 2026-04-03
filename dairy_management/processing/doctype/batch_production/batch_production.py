import frappe
from frappe.model.document import Document
from frappe.utils import flt

class BatchProduction(Document):
    def after_insert(self):
        """Auto-create a Draft Lab Test as soon as a new batch record is started."""
        self.db_set("status", "Pending Lab Test")
        self._create_quality_inspection()

    def before_save(self):
        self._calculate_yield()

    def _calculate_yield(self):
        """Calculate the efficiency/yield percentage of the production run."""
        if self.quantity_produced and self.raw_milk_used_litres and self.raw_milk_used_litres > 0:
            self.yield_percentage = (flt(self.quantity_produced) / flt(self.raw_milk_used_litres)) * 100

    def before_submit(self):
        """Block submission if the Lab Test has not passed."""
        if self.status != "QA Approved":
            frappe.throw("<b>Stop:</b> Production cannot be finalized until the Lab Test is <b>Submitted & Passed</b>.")

    def on_submit(self):
        self._ensure_batch_exists()
        self._create_stock_entry()
        self.db_set("status", "Completed")
        
        # Link back to Processing Order and mark it as Completed
        if self.processing_order:
            frappe.db.set_value("Processing Order", self.processing_order, "status", "Completed")
            frappe.msgprint(f"<b>Planning Loop Closed:</b> Processing Order {self.processing_order} is now Completed.", alert=True)

    def _create_quality_inspection(self):
        """Helper to create a Draft Quality Check Inspection linked to this batch."""
        if frappe.db.exists("Quality Check Inspection", {"batch_production": self.name}):
            return

        try:
            # Get the Item Group of the product to find the matching QC template
            item_group = frappe.db.get_value("Item", self.product, "item_group")
            template = frappe.db.get_value("Lab Test Template", {"product_category": item_group})
            
            qci = frappe.new_doc("Quality Check Inspection")
            qci.batch_production = self.name
            qci.template = template
            qci.inspection_date = self.production_date
            qci.insert(ignore_permissions=True)
            
            frappe.msgprint(f"<b>Laboratory Step:</b> Draft Lab Test {qci.name} has been queued.", alert=True)
        except Exception as e:
            frappe.log_error(str(e), "Batch Production: Lab Test Creation Failed")

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
        """Auto-create ERPNext Stock Entry (Repack) with multiple ingredients and fallback."""
        settings = frappe.get_single("Dairy Management Settings")
        
        if not self.target_warehouse:
            frappe.throw("<b>Inventory Error:</b> Please select a <b>Target Warehouse</b> (Finished Goods Shelf) for this batch.")

        try:
            se = frappe.new_doc("Stock Entry")
            se.stock_entry_type = "Repack"
            se.batch_production = self.name
            se.posting_date = self.production_date
            
            # 1. CONSUME INGREDIENTS
            has_ingredients = False
            for row in self.calculated_ingredients:
                has_ingredients = True
                is_milk = frappe.db.get_value("Item", row.item_code, "item_group") == "Milk" or "Milk" in row.item_code
                s_warehouse = settings.raw_milk_warehouse if is_milk else frappe.db.get_value("Item", row.item_code, "website_warehouse") or "Stores - BDD"
                
                se.append("items", {
                    "item_code": row.item_code,
                    "qty": row.required_qty,
                    "s_warehouse": s_warehouse,
                    "uom": row.uom,
                    "is_finished_item": 0,
                })
            
            # FALLBACK: If table is empty, use the main Milk Item from settings
            if not has_ingredients:
                if not settings.raw_milk_warehouse or not settings.raw_milk_item:
                    frappe.throw("No ingredients found AND 'Dairy Management Settings' is missing default milk item/warehouse.")
                
                # Use raw_milk_used_litres (legacy field) or calculate from quantity_produced
                milk_qty = self.raw_milk_used_litres or self.quantity_produced
                se.append("items", {
                    "item_code": settings.raw_milk_item,
                    "qty": milk_qty,
                    "s_warehouse": settings.raw_milk_warehouse,
                    "uom": "Litre",
                    "is_finished_item": 0,
                })

            # 2. PRODUCE FINAL PRODUCT
            se.append("items", {
                "item_code": self.product,
                "qty": self.quantity_produced,
                "t_warehouse": self.target_warehouse,
                "is_finished_item": 1,
                "batch_no": self.batch_no,
            })
            
            se.flags.ignore_permissions = True
            se.insert()
            se.submit()
            
            self.db_set("stock_entry", se.name)
            frappe.msgprint(f"<b>Stock Received:</b> Repack Entry {se.name} created successfully.", alert=True)
            
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Batch Production: Stock Entry Creation Failed")
            frappe.throw(f"<b>Inventory Failed:</b> {str(e)}. Please check your stock levels or configuration.")

@frappe.whitelist()
def get_processing_order_details(processing_order):
    """Utility to auto-fill Batch Production fields and ingredients from Processing Order."""
    po = frappe.get_doc("Processing Order", processing_order)
    
    data = {
        "product": po.product,
        "quantity_produced": po.planned_quantity,
        "target_warehouse": frappe.db.get_single_value("Dairy Management Settings", "finished_goods_warehouse"),
        "ingredients": []
    }
    
    for row in po.calculated_ingredients:
        data["ingredients"].append({
            "item_code": row.item_code,
            "required_qty": row.required_qty,
            "uom": row.uom
        })
        
    return data

def on_submit(doc, method=None):
    """Module-level fallback to satisfy stale hooks.py cache if bench hasn"t restarted."""
    if hasattr(doc, "on_submit"):
        doc.on_submit()
