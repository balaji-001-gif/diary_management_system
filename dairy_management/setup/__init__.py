
import frappe
from frappe.utils import add_days, today, flt, getdate
import random

def load_demo_data():
    """Populate comprehensive sample data for the Dairy Management System."""
    print("🚀 Starting Comprehensive Demo Data Seeding...")
    
    # 0. ERPNext Infrastructure Prerequisites
    create_erpnext_prerequisites()
    
    # 1. Core Configuration Masters
    create_core_masters()
    
    # 2. Entity Masters (Farmers, Routes, Animals)
    create_entities()
    
    # 3. Last 30 Days of Transactions
    populate_transactions()

    frappe.db.commit()
    print("✅ Full-Stack Demo Data Loaded Successfully!")

def create_erpnext_prerequisites():
    print("--- 📦 Seeding ERPNext Prerequisites...")
    
    # Get primary company
    company = frappe.db.get_value("Company", {}, "name")
    if not company:
        print("⚠️ No Company found. Skipping warehouse creation.")
        return

    # UOM
    if not frappe.db.exists("UOM", "Litre"):
        frappe.get_doc({"doctype": "UOM", "uom_name": "Litre", "must_be_whole_number": 0}).insert(ignore_permissions=True)
        
    # Item Group
    parent_item_group = frappe.db.get_value("Item Group", {"is_group": 1, "parent_item_group": ""}, "name") or "All Item Groups"
    if not frappe.db.exists("Item Group", "Dairy Products"):
        frappe.get_doc({"doctype": "Item Group", "item_group_name": "Dairy Products", "parent_item_group": parent_item_group}).insert(ignore_permissions=True)

    # Warehouse
    parent_warehouse = frappe.db.get_value("Warehouse", {"is_group": 1, "company": company, "parent_warehouse": ["in", ["", None]]}, "name")
    if not parent_warehouse:
         # Fallback search
         parent_warehouse = frappe.db.get_value("Warehouse", {"is_group": 1, "company": company}, "name")

    company_abbr = frappe.db.get_value("Company", company, "abbr")

    if not frappe.db.exists("Warehouse", f"Finished Goods - {company_abbr}"):
        try:
            frappe.get_doc({
                "doctype": "Warehouse", 
                "warehouse_name": "Finished Goods", 
                "is_group": 0, 
                "company": company,
                "parent_warehouse": parent_warehouse
            }).insert(ignore_permissions=True, ignore_if_duplicate=True)
        except frappe.DuplicateEntryError:
            pass

    # Items
    items = [
        {"item_code": "Raw Milk", "item_name": "Raw Milk", "item_group": "Dairy Products", "stock_uom": "Litre", "is_stock_item": 1},
        {"item_code": "Full Cream Milk", "item_name": "Full Cream Milk", "item_group": "Dairy Products", "stock_uom": "Litre", "is_stock_item": 1},
        {"item_code": "Skimmed Milk", "item_name": "Skimmed Milk", "item_group": "Dairy Products", "stock_uom": "Litre", "is_stock_item": 1},
        {"item_code": "Curd", "item_name": "Curd", "item_group": "Dairy Products", "stock_uom": "Nos", "is_stock_item": 1}
    ]
    for i in items:
        if not frappe.db.exists("Item", i["item_code"]):
            frappe.get_doc({"doctype": "Item", **i}).insert(ignore_permissions=True)

    # Supplier Group
    if not frappe.db.exists("Supplier Group", "Dairy Farmers"):
        frappe.get_doc({"doctype": "Supplier Group", "supplier_group_name": "Dairy Farmers"}).insert(ignore_permissions=True)

def create_core_masters():
    print("--- 🛠️ Seeding Core DM Masters...")
    
    # Deduction Master
    deductions = [
        {"deduction_type": "Feed Loan Recovery", "description": "Weekly recovery for cattle feed supply"},
        {"deduction_type": "Membership Fee", "description": "Annual cooperative membership"},
        {"deduction_type": "Cattle Insurance", "description": "Monthly premium for animal health insurance"}
    ]
    for d in deductions:
        if not frappe.db.exists("Deduction Master", d["deduction_type"]):
            frappe.get_doc({"doctype": "Deduction Master", **d}).insert()

    # Lab Test Template (contains child table Quality Check Parameter)
    template_name = "Standard Raw Milk Test"
    if not frappe.db.exists("Lab Test Template", template_name):
        frappe.get_doc({
            "doctype": "Lab Test Template",
            "template_name": template_name,
            "product_category": "Dairy Products",
            "parameters": [
                {"parameter_name": "Fat %", "unit": "%", "min_acceptable": 3.0, "max_acceptable": 10.0, "mandatory": 1},
                {"parameter_name": "SNF %", "unit": "%", "min_acceptable": 8.0, "max_acceptable": 12.0, "mandatory": 1},
                {"parameter_name": "Bacteria Count", "unit": "CFU/ml", "min_acceptable": 0, "max_acceptable": 50000}
            ]
        }).insert()

    # Rate Slab
    if not frappe.db.exists("Rate Slab", "Standard Quality Slab"):
        slab = frappe.get_doc({
            "doctype": "Rate Slab",
            "slab_name": "Standard Quality Slab",
            "effective_from": add_days(today(), -365),
            "effective_to": add_days(today(), 365),
            "base_rate": 35.0,
            "fat_snf_matrix": [
                {"fat_from": 3.0, "fat_to": 4.5, "snf_from": 8.0, "snf_to": 8.5, "rate_per_litre": 38.0},
                {"fat_from": 4.5, "fat_to": 6.0, "snf_from": 8.5, "snf_to": 9.0, "rate_per_litre": 42.0},
                {"fat_from": 6.0, "fat_to": 10.0, "snf_from": 9.0, "snf_to": 12.0, "rate_per_litre": 48.0}
            ]
        })
        slab.insert()

    # Breed
    breeds = [
        {"breed_name": "Holstein Friesian", "avg_daily_yield_litres": 25, "standard_lactation_days": 305, "avg_fat_percentage": 3.7},
        {"breed_name": "Jersey", "avg_daily_yield_litres": 18, "standard_lactation_days": 305, "avg_fat_percentage": 4.8},
        {"breed_name": "Gir", "avg_daily_yield_litres": 12, "standard_lactation_days": 280, "avg_fat_percentage": 4.5}
    ]
    for b in breeds:
        if not frappe.db.exists("Breed", b["breed_name"]):
            frappe.get_doc({"doctype": "Breed", **b}).insert()

def create_entities():
    print("--- 🐄 Seeding Farmers & Animals...")
    
    # Collection Centers
    centers = ["Main Collection Hub", "East Village Center"]
    for c in centers:
        if not frappe.db.exists("Collection Center", c):
            frappe.get_doc({"doctype": "Collection Center", "center_name": c}).insert()

    # Milk Routes
    routes = [
        {"route_name": "North Valley Route", "collection_center": "Main Collection Hub", "distance_km": 15},
        {"route_name": "Green Ridge Route", "collection_center": "East Village Center", "distance_km": 22}
    ]
    for r in routes:
        if not frappe.db.exists("Milk Route", r["route_name"]):
            frappe.get_doc({"doctype": "Milk Route", **r}).insert()

    # Farmers
    farmers_data = [
        {"farmer_code": "FRM-001", "name": "Rajesh Kumar", "village": "North Valley", "route": "North Valley Route"},
        {"farmer_code": "FRM-002", "name": "Anita Devi", "village": "Green Ridge", "route": "Green Ridge Route"},
        {"farmer_code": "FRM-003", "name": "Suresh Patil", "village": "North Valley", "route": "North Valley Route"}
    ]
    for fd in farmers_data:
        # Create ERPNext Supplier if missing
        if not frappe.db.exists("Supplier", fd["name"]):
            frappe.get_doc({
                "doctype": "Supplier",
                "supplier_name": fd["name"],
                "supplier_group": "Dairy Farmers",
                "supplier_type": "Individual"
            }).insert(ignore_permissions=True)
            
        if not frappe.db.exists("Farmer", fd["farmer_code"]):
            frappe.get_doc({
                "doctype": "Farmer",
                "farmer_code": fd["farmer_code"],
                "farmer_name": fd["name"],
                "supplier": fd["name"],
                "village": fd["village"],
                "route": fd["route"]
            }).insert()
        else:
            # Repair existing farmer if supplier link is missing
            frappe.db.set_value("Farmer", fd["farmer_code"], "supplier", fd["name"])

    # Animals
    animals_data = [
        {"animal_id": "TAG-1001", "name": "Ganga", "breed": "Gir", "farmer": "FRM-001"},
        {"animal_id": "TAG-1002", "name": "Yamuna", "breed": "Holstein Friesian", "farmer": "FRM-002"},
        {"animal_id": "TAG-1003", "name": "Kavery", "breed": "Jersey", "farmer": "FRM-003"}
    ]
    for ad in animals_data:
        if not frappe.db.exists("Animal", {"animal_id": ad["animal_id"]}):
            frappe.get_doc({
                "doctype": "Animal",
                "naming_series": "ANM-.YYYY.-.####",
                "animal_id": ad["animal_id"],
                "animal_name": ad["name"],
                "breed": ad["breed"],
                "sex": "Female",
                "status": "Active",
                "farmer": ad["farmer"]
            }).insert()

def populate_transactions():
    print("--- 📊 Seeding Last 30 Days of Transactions...")
    
    farmers = frappe.get_all("Farmer", pluck="name")
    animals = frappe.get_all("Animal", pluck="name")
    
    for i in range(1, 31):
        trans_date = add_days(today(), -i)
        
        # 1. Health Records (Every few days for random animals)
        if i % 5 == 0:
            target_animal = random.choice(animals)
            hr = frappe.get_doc({
                "doctype": "Health Record",
                "animal": target_animal,
                "date": trans_date,
                "event_type": "Checkup",
                "disease_condition": "Routine Deworming",
                "medicine": "Albendazole",
                "cost": 150.0
            })
            hr.insert()
            if i % 10 == 0: hr.submit() # Mix of Submit and Draft

        # 2. Milk Collection Entries (Daily for all farmers)
        for f_code in farmers:
            farmer_doc = frappe.get_doc("Farmer", f_code)
            for shift in ["Morning", "Evening"]:
                qty = flt(random.uniform(5.5, 12.0), 2)
                fat = flt(random.uniform(4.0, 7.5), 2)
                snf = flt(random.uniform(8.5, 9.5), 2)
                
                mce = frappe.get_doc({
                    "doctype": "Milk Collection Entry",
                    "farmer": f_code,
                    "route": farmer_doc.route,
                    "collection_date": trans_date,
                    "shift": shift,
                    "quantity_litres": qty,
                    "fat_percentage": fat,
                    "snf_percentage": snf,
                    "grade": "Grade A",
                    "rate_per_litre": 42.0,
                    "amount": qty * 42.0
                })
                mce.insert()
                # Submit most entries to populate reports, keep last 2 days as Drafts
                if i > 2:
                    mce.submit()

    # 3. Batch Production (Processing)
    print("--- 🧪 Seeding Production Batches...")
    
    company = frappe.db.get_value("Company", {}, "name")
    company_abbr = frappe.db.get_value("Company", company, "abbr")
    target_warehouse = f"Finished Goods - {company_abbr}"

    if not frappe.db.exists("Product Formula", "Full Cream Milk"):
        frappe.get_doc({
            "doctype": "Product Formula",
            "product": "Full Cream Milk",
            "processing_type": "Full Cream",
            "raw_milk_litres_per_unit": 0.98,
            "cream_ratio": 0.05
        }).insert()

    for i in [15, 7, 2]: # Three sample production batches
        p_date = add_days(today(), -i)
        
        # Create Processing Order first (mandatory for Batch Production)
        po = frappe.get_doc({
            "doctype": "Processing Order",
            "product": "Full Cream Milk",
            "planned_quantity": 500,
            "planned_start_date": p_date,
            "status": "Completed"
        })
        po.insert()
        if i > 5: po.submit()

        bp = frappe.get_doc({
            "doctype": "Batch Production",
            "processing_order": po.name,
            "product": "Full Cream Milk",
            "production_date": p_date,
            "quantity_produced": 500,
            "raw_milk_used_litres": 490,
            "target_warehouse": target_warehouse
        })
        bp.insert()
        if i > 5: bp.submit()

    # 4. Billing (Farmer Invoices)
    print("--- 💰 Seeding Farmer Invoices...")
    one_month_ago = add_days(today(), -30)
    for f_code in farmers:
        finv = frappe.get_doc({
            "doctype": "Farmer Invoice",
            "farmer": f_code,
            "period_from": add_days(one_month_ago, 1),
            "period_to": today(),
            "total_litres_supplied": 240,
            "gross_amount": 10000,
            "total_deductions": 500,
            "net_payable": 9500
        })
        finv.insert()
        # Keep latest invoice as draft, others submitted
        if random.random() > 0.3:
            finv.submit()
            # Integration logic usually would create Purchase Invoice here via server-side hook
            # but we just seed the FINV for demo purposes.
