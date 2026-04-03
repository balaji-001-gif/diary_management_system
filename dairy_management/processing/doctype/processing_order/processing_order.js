frappe.ui.form.on("Processing Order", {
    product_formula: function(frm) {
        if (frm.doc.product_formula) {
            frappe.model.with_doc("Product Formula", frm.doc.product_formula, function() {
                let formula = frappe.get_doc("Product Formula", frm.doc.product_formula);
                frm.set_value("product", formula.product);
                calculate_ingredients(frm, formula);
            });
        }
    },
    planned_quantity: function(frm) {
        if (frm.doc.product_formula) {
            frappe.model.with_doc("Product Formula", frm.doc.product_formula, function() {
                let formula = frappe.get_doc("Product Formula", frm.doc.product_formula);
                calculate_ingredients(frm, formula);
            });
        }
    }
});

var calculate_ingredients = function(frm, formula) {
    frm.clear_table("calculated_ingredients");
    
    if (frm.doc.planned_quantity && formula.ingredients) {
        formula.ingredients.forEach(row => {
            let child = frm.add_child("calculated_ingredients");
            child.item_code = row.item_code;
            child.uom = row.uom;
            child.required_qty = flt(frm.doc.planned_quantity) * flt(row.qty_per_unit);
        });
        
        // Backward compatibility for the legacy field (hidden)
        let milk_row = formula.ingredients.find(i => i.is_raw_milk);
        if (milk_row) {
            frm.set_value("raw_milk_required_litres", flt(frm.doc.planned_quantity) * flt(milk_row.qty_per_unit));
        }
    }
    
    frm.refresh_field("calculated_ingredients");
};
