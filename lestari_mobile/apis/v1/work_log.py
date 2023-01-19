import frappe

@frappe.whitelist()
def get(spok_name):
    return frappe.get_all("Work Log",fields=["*"],filters=[["spko","=",spok_name],['docstatus','=',1]],order_by="modified desc")

@frappe.whitelist()
def start(spok_name):
    #check employee
    employee = frappe.get_value("Employee", {"user_id": frappe.session.user}, "name")

    #check existing
    exist = frappe.get_value("Work Log", {"spko": spok_name, "docstatus": 0},"name")
    if exist:
        frappe.throw("Tidak bisa start, karena sedang ada yang berjalan")
    doc = frappe.new_doc("Work Log")
    doc.update({
        "employee": employee,
        "spko": spok_name,
        "waktu_mulai": frappe.utils.now()
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc


@frappe.whitelist()
def batch_start(spok_names):
    spkos = spok_names.split("<>")
    #check employee
    employee = frappe.get_value("Employee", {"user_id": frappe.session.user}, "name")

    for spko in spkos:
        #check existing
        exist = frappe.get_value("Work Log", {"spko": spko, "docstatus": 0},"name")
        if exist:
            frappe.throw("Tidak bisa start, karena SPKO {} sedang ada yang berjalan".format(spko))
    
    doc = frappe.new_doc("Batch Work Log")
    doc.update({
        "employee": employee,
        "spkos": spok_names.replace("<>", "\n"),
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

@frappe.whitelist()
def batch_stop(batch_work_log):
    doc = frappe.get_doc("Batch Work Log", batch_work_log)
    doc.update({
        "waktu_selesai": frappe.utils.now(),
        "docstatus": 1
    })
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return doc
