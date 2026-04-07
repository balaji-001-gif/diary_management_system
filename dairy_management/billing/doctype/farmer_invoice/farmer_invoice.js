frappe.ui.form.on('Farmer Invoice', {
    refresh: function(frm) {
        if (!frm.doc.__islocal && frm.doc.docstatus === 0) {
            frm.add_custom_button(__('Fetch Collection Data'), function() {
                frm.call({
                    method: 'get_billing_data',
                    doc: frm.doc,
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(__('Billing data fetched and calculated successfully.'));
                            frm.refresh();
                        }
                    }
                });
            }, __('Actions'));
        }
    }
});
