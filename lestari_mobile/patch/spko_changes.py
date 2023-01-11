import frappe

def execute():
    #spko no
    data = frappe.get_all("SPKO", filters=[["no_spko","is","not set"]])
    if len(data) > 0:
        frappe.db.sql("update `tabSPKO` set no_spko = no_spok")
        frappe.db.commit()
    
    data = frappe.get_all("Work Log", filters=[["spko","is","not set"]])
    if len(data) > 0:
        frappe.db.sql("update `tabWork Log` set spko = spok")
        frappe.db.commit()

    