frappe.ui.form.on('Farmer Invoice', {
    refresh: function(frm) {
        if (!frm.doc.__islocal && frm.doc.docstatus === 0) {
            frm.add_custom_button(__('Fetch Collection Data'), function() {
                frm.call({
                    method: 'get_billing_data',
                    doc: frm.doc,
                    callback: function(r) {
                        if (r.message) {
                            let data = r.message;
                            
                            // 1. Update Totals
                            frm.set_value('total_litres_supplied', data.total_litres_supplied);
                            frm.set_value('gross_amount', data.gross_amount);
                            frm.set_value('total_deductions', data.total_deductions);
                            frm.set_value('net_payable', data.net_payable);
                            
                            // 2. Populate Deductions Table
                            frm.clear_table('deductions');
                            data.deductions.forEach(d => {
                                let row = frm.add_child('deductions');
                                row.deduction_voucher = d.deduction_voucher;
                                row.deduction_type = d.deduction_type;
                                row.amount = d.amount;
                            });
                            
                            frm.refresh_field('deductions');
                            frappe.msgprint(__('Billing data fetched and applied successfully.'));
                        }
                    }
                });
            }, __('Actions'));
        }
    }
});
