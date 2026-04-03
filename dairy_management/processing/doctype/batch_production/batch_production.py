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
        """Auto-create ERPNext Stock Entry (Repack) with multiple ingredients."""
        settings = frappe.get_single("Dairy Management Settings")
        
        if not self.target_warehouse:
            frappe.msgprint("<b>Step 6 Failed:</b> Please select a <b>Target Warehouse</b> for the finished milk.", alert=True, indicator="orange")
            return

        if not self.calculated_ingredients:
            frappe.msgprint("<b>Step 6 Failed:</b> No ingredients found. Please ensure the Processing Order is correctly set up.", alert=True, indicator="orange")
            return

        try:
            se = frappe.new_doc("Stock Entry")
            se.stock_entry_type = "Repack"
            se.batch_production = self.name
            se.posting_date = self.production_date
            
            # 1. CONSUME EVERYTHING in the ingredients table
            for row in self.calculated_ingredients:
                is_milk = frappe.db.get_value("Item", row.item_code, "item_group") == "Milk" or "Milk" in row.item_code
                
                # Source warehouse: Milk from Raw Tank, others from Item Default or a General Store
                s_warehouse = settings.raw_milk_warehouse if is_milk else frappe.db.get_value("Item", row.item_code, "website_warehouse") or "Stores - BDD"
                
                se.append("items", {
                    "item_code": row.item_code,
                    "qty": row.required_qty,
                    "s_warehouse": s_warehouse,
                    "uom": row.uom,
                    "is_finished_item": 0,
                })
            
            # 2. PRODUCE the final product
            se.append("items", {
                "item_code": self.product,
                "qty": self.quantity_produced,
                "t_warehouse": self.target_warehouse,
                "is_finished_item": 1,
                "batch_no": self.batch_no,
            })
            
            se.insert(ignore_permissions=True)
            self.db_set("stock_entry", se.name)
            frappe.msgprint(f"<b>Step 6 Success:</b> Created multi-ingredient Repack {se.name}.", alert=True)
        except Exception as e:
            frappe.log_error(str(e), "Batch Production: Stock Entry (Repack) Creation Failed")
            frappe.msgprint("<b>Step 6 Failed:</b> Check Error Log for details.", alert=True, indicator="red")

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
