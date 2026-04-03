frappe.ui.form.on("Batch Production", {
    setup: function(frm) {
        // Only show Processing Orders that are currently In Progress
        frm.set_query("processing_order", function() {
            return {
                filters: [
                    ["status", "=", "In Progress"],
                    ["docstatus", "=", 1]
                ]
            };
        });
    },
    production_date: function(frm) {
        // Re-calculate expiry if production date changes
        frm.trigger("product");
    },
    product: function(frm) {
        if (frm.doc.product) {
            frappe.db.get_value("Item", frm.doc.product, "shelf_life_in_days", (r) => {
                if (r && r.shelf_life_in_days) {
                    let expiry = frappe.datetime.add_days(frm.doc.production_date || frappe.datetime.get_today(), r.shelf_life_in_days);
                    frm.set_value("expiry_date", expiry);
                }
            });
        }
    },
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
                        frm.set_value("target_warehouse", r.message.target_warehouse);
                        
                        // Clear and Fill Ingredients Table
                        frm.clear_table("calculated_ingredients");
                        if (r.message.ingredients) {
                            r.message.ingredients.forEach(row => {
                                let child = frm.add_child("calculated_ingredients");
                                child.item_code = row.item_code;
                                child.required_qty = row.required_qty;
                                child.uom = row.uom;
                            });
                        }
                        frm.refresh_field("calculated_ingredients");
                        
                        // Auto-calculate yield if values are present
                        frm.trigger("quantity_produced");
                    }
                }
            });
        }
    },
    quantity_produced: function(frm) {
        // Calculate yield based on the milk ingredient in the table
        let milk_qty = 0;
        if (frm.doc.calculated_ingredients) {
            frm.doc.calculated_ingredients.forEach(i => {
                if (i.item_code.toLowerCase().includes("milk")) {
                    milk_qty += flt(i.required_qty);
                }
            });
        }
        
        if (frm.doc.quantity_produced && milk_qty > 0) {
            let yield_pct = (flt(frm.doc.quantity_produced) / flt(milk_qty)) * 100;
            frm.set_value("yield_percentage", yield_pct);
        }
    },
    refresh: function(frm) {
        if (frm.doc.status === "Pending Lab Test") {
            frm.set_df_property("status", "description", "<b>Wait:</b> Lab Technician must submit the QC test first.");
        }
        
        // Add indicator colors
        let color = "orange";
        if (frm.doc.status === "QA Approved" || frm.doc.status === "Completed") color = "green";
        if (frm.doc.status === "QA Failed") color = "red";
        
        frm.page.set_indicator(frm.doc.status, color);
    }
});
