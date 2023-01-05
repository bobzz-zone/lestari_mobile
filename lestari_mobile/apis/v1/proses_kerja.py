import frappe

@frappe.whitelist()
def get():
    return frappe.get_list("Proses Kerja",fields=["*"])

