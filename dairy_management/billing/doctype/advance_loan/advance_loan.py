import frappe
from frappe.model.document import Document
from frappe.utils import flt

class AdvanceLoan(Document):
    def before_save(self):
        if self.loan_amount and self.repayment_months and self.repayment_months > 0:
            self.monthly_deduction = flt(self.loan_amount) / self.repayment_months
        if not self.outstanding_balance:
            self.outstanding_balance = self.loan_amount

    def validate(self):
        if self.repayment_months and self.repayment_months <= 0:
            frappe.throw("Repayment months must be greater than 0.")
