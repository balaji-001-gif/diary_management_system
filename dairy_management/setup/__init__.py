
import frappe

def load_demo_data():
    """Populate sample data for Dairy Management System"""
    print("Loading Demo Data...")
    
    # 1. Breeds
    breeds_to_create = [
        {"breed_name": "Holstein Friesian", "avg_daily_yield_litres": 25, "standard_lactation_days": 305, "avg_fat_percentage": 3.7},
        {"breed_name": "Jersey", "avg_daily_yield_litres": 18, "standard_lactation_days": 305, "avg_fat_percentage": 4.8},
        {"breed_name": "Gir", "avg_daily_yield_litres": 12, "standard_lactation_days": 280, "avg_fat_percentage": 4.5}
    ]
    for b in breeds_to_create:
        if not frappe.db.exists("Breed", b["breed_name"]):
            doc = frappe.get_doc({"doctype": "Breed", **b})
            doc.insert()
            print(f"Created Breed: {b['breed_name']}")

    # 2. Collection Centers
    centers = ["Center A", "Center B"]
    for c in centers:
        if not frappe.db.exists("Collection Center", c):
            doc = frappe.get_doc({"doctype": "Collection Center", "center_name": c})
            doc.insert()
            print(f"Created Center: {c}")

    # 3. Milk Routes
    routes = [
        {"route_name": "North Route", "collection_center": "Center A", "distance_km": 15},
        {"route_name": "South Route", "collection_center": "Center B", "distance_km": 22}
    ]
    for r in routes:
        if not frappe.db.exists("Milk Route", r["route_name"]):
            doc = frappe.get_doc({"doctype": "Milk Route", **r})
            doc.insert()
            print(f"Created Route: {r['route_name']}")

    # 4. Farmers
    farmers_to_create = [
        {"farmer_code": "F001", "farmer_name": "John Doe", "village": "Village 1", "route": "North Route"},
        {"farmer_code": "F002", "farmer_name": "Jane Smith", "village": "Village 2", "route": "South Route"}
    ]
    for f in farmers_to_create:
        if not frappe.db.exists("Farmer", f["farmer_code"]):
            doc = frappe.get_doc({"doctype": "Farmer", **f})
            doc.insert()
            print(f"Created Farmer: {f['farmer_name']}")

    # 5. Animals
    animals_to_create = [
        {"animal_id": "TAG-101", "animal_name": "Bessie", "breed": "Holstein Friesian", "sex": "Female", "status": "Active", "farmer": "F001"},
        {"animal_id": "TAG-102", "animal_name": "Daisy", "breed": "Jersey", "sex": "Female", "status": "Active", "farmer": "F002"}
    ]
    for a in animals_to_create:
        if not frappe.db.exists("Animal", {"animal_id": a["animal_id"]}):
            # We need to manually set naming_series for Animal since it uses autoname
            doc = frappe.get_doc({
                "doctype": "Animal",
                "naming_series": "ANM-.YYYY.-.####",
                **a
            })
            doc.insert()
            print(f"Created Animal: {a['animal_name']}")

    frappe.db.commit()
    print("Demo Data Loaded Successfully!")
