import frappe
from frappe.model.document import Document

class QcInspection(Document):
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
