import frappe
from frappe.model.document import Document
from frappe.utils import flt

class ShiftSummary(Document):
    def before_save(self):
        self.aggregate_collection_entries()

    def aggregate_collection_entries(self):
        """Fetch and sum up all submitted Milk Collection Entries for this route/date/shift."""
        entries = frappe.get_all(
            "Milk Collection Entry",
            filters={
                "route": self.route,
                "collection_date": self.collection_date,
                "shift": self.shift,
                "docstatus": 1 # Only aggregate submitted entries
            },
            fields=["quantity_litres", "fat_percentage", "snf_percentage", "farmer", "amount"]
        )

        if not entries:
            # Reset totals if no entries found
            self.total_quantity_litres = 0
            self.avg_fat_percentage = 0
            self.avg_snf_percentage = 0
            self.farmer_count = 0
            self.total_amount = 0
            return

        total_qty = sum(flt(e.quantity_litres) for e in entries)
        total_amt = sum(flt(e.amount) for e in entries)
        farmer_list = set(e.farmer for e in entries)
        
        # Weighted average for quality (litres * percentage / total_litres)
        if total_qty > 0:
            avg_fat = sum(flt(e.fat_percentage) * flt(e.quantity_litres) for e in entries) / total_qty
            avg_snf = sum(flt(e.snf_percentage) * flt(e.quantity_litres) for e in entries) / total_qty
        else:
            avg_fat = 0
            avg_snf = 0

        self.total_quantity_litres = total_qty
        self.avg_fat_percentage = flt(avg_fat, 2)
        self.avg_snf_percentage = flt(avg_snf, 2)
        self.farmer_count = len(farmer_list)
        self.total_amount = total_amt
