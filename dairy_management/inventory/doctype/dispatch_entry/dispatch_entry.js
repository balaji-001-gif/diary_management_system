frappe.ui.form.on("Dispatch Entry", {
    onload: function(frm) {
        if (frm.is_new()) {
            frappe.db.get_single_value("Dairy Management Settings", "finished_goods_warehouse", (val) => {
                if (val) frm.set_value("source_warehouse", val);
            });
        }
    },
    route: function(frm) {
        if (frm.doc.route) {
            frappe.db.get_doc("Delivery Route", frm.doc.route).then(route => {
                if (route.driver) frm.set_value("driver", route.driver);
                if (route.vehicle_no) frm.set_value("vehicle_no", route.vehicle_no);
            });
        }
    },
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__("View Stock Entry"), function() {
                frappe.set_route("Form", "Stock Entry", frm.doc.stock_entry);
            });
        }
    }
});

frappe.ui.form.on("Dispatch Entry Item", {
    item_code: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code) {
            frappe.db.get_value("Item", row.item_code, "stock_uom", (r) => {
                if (r.stock_uom) frappe.model.set_value(cdt, cdn, "uom", r.stock_uom);
            });
        }
    }
});
