import frappe
import json

@frappe.whitelist()
def login_by_id(employee_id):
    employee = frappe.get_value("Employee", employee_id)
    if employee:
        doc = frappe.get_doc("Employee", employee)
        user = frappe.get_value("Employee", employee, "user_id")
        if user:
            token = generate_token(user)
            return {
                "doc": doc,
                "token": token
            }
    frappe.throw("Not found")

@frappe.whitelist()
def validate_token():
    param = json.loads(frappe.request.data)
    valid_token = generate_token(param['user'])
    return param['token'] == valid_token

@frappe.whitelist()
def generate_token(user, is_force=False):
    api_key = frappe.get_value("User", user, "api_key")
    if api_key is None or is_force:
        from frappe.core.doctype.user.user import generate_keys
        generate_token = generate_keys(user)
        user_doc = frappe.get_doc("User", user)
        token = "token {}:{}".format(user_doc.api_key, generate_token['api_secret'])
    else:
        from frappe.utils.password import get_decrypted_password
        user_doc = frappe.get_doc("User", user)
        token = "token {}:{}".format(user_doc.api_key, get_decrypted_password("User", user, "api_secret"))
    return token
    

@frappe.whitelist()
def forgot_password(user):
    from frappe.core.doctype.user.user import reset_password
    reset_password(user)
    return "success"