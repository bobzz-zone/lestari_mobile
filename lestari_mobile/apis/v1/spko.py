import frappe

@frappe.whitelist()
def get(spok_name):
    spko = frappe.get_value("SPKO", {"qr_code_hash": spok_name.strip()}, "name")
    if spko is None:
        spko = frappe.get_value("SPKO", spok_name.strip(), "name")
    if spko:
        last_work_log = frappe.get_all("Work Log", fields=["*"], filters=[["spko","=",spok_name.strip()]], order_by="creation desc", limit_page_length=1)
        return {
            "doc": frappe.get_doc("SPKO", spko),
            "last_work_log": last_work_log
        }
    frappe.throw("Not found")