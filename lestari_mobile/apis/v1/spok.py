import frappe

@frappe.whitelist()
def get(spok_name):
    spok = frappe.get_value("SPOK", {"qr_code_hash": spok_name}, "name")
    if spok:
        return frappe.get_doc("SPOK", spok)
    frappe.throw("Not found")