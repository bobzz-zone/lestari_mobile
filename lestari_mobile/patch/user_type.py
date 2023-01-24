import frappe

def execute():
    data = {
        "name": "User App",
        "is_standard": 1,
        "doctype": "User Type",
        "user_doctypes": [
        
        ],
        "custom_select_doctypes": [
        
        ],
        "select_doctypes": [
        
        ],
        "user_type_modules": [
        
        ]
    }
    value = frappe.get_value("User Type", data["name"])
    if value is None:
        doc = frappe.new_doc("User Type")
        doc.update(data)
        doc.insert()
    