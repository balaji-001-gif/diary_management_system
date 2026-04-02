frappe.ui.form.on("Processing Order", {
    product_formula: function(frm) {
        if (frm.doc.product_formula) {
            frappe.db.get_value("Product Formula", frm.doc.product_formula, ["product", "raw_milk_litres_per_unit"], (r) => {
                if (r && r.product) {
                    frm.set_value("product", r.product);
                    calculate_raw_milk(frm, r.raw_milk_litres_per_unit);
                }
            });
        }
    },
    planned_quantity: function(frm) {
        if (frm.doc.product_formula) {
            frappe.db.get_value("Product Formula", frm.doc.product_formula, "raw_milk_litres_per_unit", (r) => {
                calculate_raw_milk(frm, r.raw_milk_litres_per_unit);
            });
        }
    }
});

var calculate_raw_milk = function(frm, ratio) {
    if (frm.doc.planned_quantity && ratio) {
        let total = flt(frm.doc.planned_quantity) * flt(ratio);
        frm.set_value("raw_milk_required_litres", total);
    }
};
