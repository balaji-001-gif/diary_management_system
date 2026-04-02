frappe.ui.form.on("Batch Production", {
    processing_order: function(frm) {
        if (frm.doc.processing_order) {
            frappe.call({
                method: "dairy_management.processing.doctype.batch_production.batch_production.get_processing_order_details",
                args: {
                    processing_order: frm.doc.processing_order
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value("product", r.message.product);
                        frm.set_value("quantity_produced", r.message.quantity_produced);
                        frm.set_value("raw_milk_used_litres", r.message.raw_milk_used_litres);
                        frm.set_value("target_warehouse", r.message.target_warehouse);
                    }
                }
            });
        }
    }
});
