import frappe
from frappe.model.document import Document

class Farmer(Document):
    def after_insert(self):
        """Automatically create a Website User for the Farmer using their Code as Username."""
        self.create_portal_user()

    def create_portal_user(self):
        if frappe.db.exists("User", self.name):
            return

        # Create a dummy email for the User record (internal only)
        dummy_email = f"{self.name.lower().replace('-', '_')}@dms.local"
        
        user_doc = frappe.get_doc({
            "doctype": "User",
            "email": self.email_id or dummy_email,
            "first_name": self.farmer_name,
            "username": self.name,  # The Farmer Code used as Login ID
            "send_welcome_email": 0,
            "roles": [{"role": "Farmer"}]
        })
        
        # Set a default password so they can log in immediately
        user_doc.insert(ignore_permissions=True)
        user_doc.add_roles("Farmer")
        frappe.db.set_value("User", user_doc.name, "new_password", "Farmer@123")
        
        frappe.msgprint(f"<b>Portal Access Created!</b><br>Username: {self.name}<br>Password: Farmer@123", alert=True)
