import frappe
from frappe.model.document import Document
from frappe.utils import flt
from frappe import _

class FarmerInvoice(Document):
    @frappe.whitelist()
    def get_billing_data(self):
        """Fetch and aggregate milk collection and deduction data for the period."""
        if not (self.period_from and self.period_to):
            frappe.throw(_("Please select both 'Period From' and 'Period To'"))

        # 1. Fetch Milk Collection Data
        collection_data = frappe.db.get_value(
            "Milk Collection Entry",
            {"farmer": self.farmer, "collection_date": ["between", [self.period_from, self.period_to]], "docstatus": 1},
            ["sum(quantity_litres)", "sum(amount)"],
            as_dict=1
        )

        self.total_litres_supplied = collection_data.get("sum(quantity_litres)") or 0
        self.gross_amount = collection_data.get("sum(amount)") or 0

        # 2. Fetch Deduction Vouchers
        self.set("deductions", [])
        deduction_records = frappe.get_all(
            "Deduction Voucher",
            filters={"farmer": self.farmer, "posting_date": ["between", [self.period_from, self.period_to]], "docstatus": 1},
            fields=["name", "amount", "deduction_type"]
        )

        total_deductions = 0
        for d in deduction_records:
            self.append("deductions", {
                "deduction_voucher": d.name,
                "amount": d.amount,
                "deduction_type": d.deduction_type
            })
            total_deductions += d.amount

        self.total_deductions = total_deductions
        self.net_payable = self.gross_amount - self.total_deductions

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
