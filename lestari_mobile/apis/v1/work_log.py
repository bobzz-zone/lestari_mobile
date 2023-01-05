import frappe

@frappe.whitelist()
def get(spok_name):
    return frappe.get_all("Work Log",fields=["*"],filters=[["spok","=",spok_name],['docstatus','=',1]])

@frappe.whitelist()
def start(spok_name):
    #check existing
    exist = frappe.get_value("Work Log", {"spok": spok_name, "docstatus": 0},"name")
    if exist:
        frappe.throw("Tidak bisa start, karena sedang ada yang berjalan")
    doc = frappe.new_doc("Work Log")
    doc.update({
        "spok": spok_name,
        "waktu_mulai": frappe.utils.now()
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc

@frappe.whitelist()
def stop(work_log):
    doc = frappe.get_doc("Work Log", work_log)
    doc.update({
        "waktu_selesai": frappe.utils.now(),
        "docstatus": 1
    })
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return doc
