import frappe
from frappe.model.document import Document

class QualityCheckInspection(Document):
    def before_save(self):
        self._evaluate_results()

    def _evaluate_results(self):
        if not self.results:
            return
        failed = [r for r in self.results if r.result_value is not None
                  and ((r.min_acceptable and r.result_value < r.min_acceptable)
                       or (r.max_acceptable and r.result_value > r.max_acceptable))]
        for r in self.results:
            r.status = "Fail" if r in failed else "Pass"
        if failed:
            self.overall_result = "Fail"
        elif not self.overall_result:
            self.overall_result = "Pass"

    def on_submit(self):
        """When the lab test is finalized, update the status of the linked batch production."""
        if not self.batch_production:
            return

        status = "QA Approved" if self.overall_result == "Pass" else "QA Failed"
        frappe.db.set_value("Batch Production", self.batch_production, "status", status)
        
        # Notify the production team
        msg = "<b>QA Approved:</b> This batch is now ready for final stock entry." if status == "QA Approved" \
              else "<b>QA Failed:</b> This batch cannot be finalized due to quality failure."
        frappe.msgprint(msg, alert=True)
