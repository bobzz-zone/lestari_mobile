import frappe

@frappe.whitelist()
def get(spok_name):
    spko = frappe.get_value("SPKO", {"qr_code_hash": spok_name}, "name")
    if spko is None:
        spko = frappe.get_value("SPKO", spok_name, "name")
    if spko:
        return frappe.get_doc("SPKO", spko)
    frappe.throw("Not found")