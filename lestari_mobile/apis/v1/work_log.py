import frappe

@frappe.whitelist()
def get(spok_name):
    return frappe.get_all("Work Log",fields=["*"],filters=[["spko","=",spok_name],['docstatus','=',1]],order_by="modified desc")



@frappe.whitelist()
def start(spok_name, batch_work_log=None, start_time=None, operation=None):
    if start_time is None:
        start_time = frappe.utils.now()
    #check employee
    employee = frappe.get_value("Employee", {"user_id": frappe.session.user}, "name")

    #check existing
    exist = frappe.get_value("Work Log", {"employee":employee, "spko": spok_name, "docstatus": 0},"name")
    if exist:
        frappe.throw("Tidak bisa start, karena SPKO {} sdh km kerjakan".format(spok_name))

    doc = frappe.new_doc("Work Log")
    doc.update({
        "employee": employee,
        "spko": spok_name,
        "batch_work_log": batch_work_log,
        "waktu_mulai": start_time,
        "operation": operation
    })
    doc.insert(ignore_permissions=True)
    return doc

@frappe.whitelist()
def resume(work_log, batch_work_log=None, resume_time=None):
    if resume_time is None:
        resume_time = frappe.utils.now()
    #check employee
    employee = frappe.get_value("Employee", {"user_id": frappe.session.user}, "name")

    #check existing
    exist = frappe.get_value("Work Log", work_log)
    
    if exist is None:
        frappe.throw("Tidak bisa resume, karena worklog tidak ditemukan")
    work_log_doc = frappe.get_doc("Work Log", exist)
    doc = frappe.new_doc("Work Log")
    doc.update({
        "employee": employee,
        "resume_from": work_log,
        "spko": work_log_doc.spko,
        "batch_work_log": batch_work_log,
        "waktu_mulai": resume_time
    })
    doc.insert(ignore_permissions=True)
    return doc


@frappe.whitelist()
def batch_start(spok_names):
    spkos = spok_names.split("<>")
    #check employee
    employee = frappe.get_value("Employee", {"user_id": frappe.session.user}, "name")

    for spko in spkos:
        #check existing
        exist = frappe.get_value("Work Log", {"employee": employee, "spko": spko, "docstatus": 0},"name")
        if exist:
            frappe.throw("Tidak bisa start, karena SPKO {} sedang ada yang berjalan".format(spko))
    
    doc = frappe.new_doc("Batch Work Log")
    doc.update({
        "employee": employee,
        "spkos": spok_names.replace("<>", "\n"),
        "waktu_mulai": frappe.utils.now()
    })
    doc.insert(ignore_permissions=True)
    return doc

@frappe.whitelist()
def pause(work_log, pause_time=None):
    if pause_time is None:
        pause_time = frappe.utils.now()
    doc = frappe.get_doc("Work Log", work_log)
    doc.update({
        "is_pause": 1,
        "waktu_selesai": pause_time,
        "docstatus": 1
    })
    doc.save(ignore_permissions=True)
    return doc

@frappe.whitelist()
def stop(work_log, stop_time=None):
    if stop_time is None:
        stop_time = frappe.utils.now()
    doc = frappe.get_doc("Work Log", work_log)
    doc.update({
        "waktu_selesai": stop_time,
        "docstatus": 1
    })
    doc.save(ignore_permissions=True)
    spko_doc = frappe.get_doc("SPKO", doc.spko)
    spko_doc.status = "Closed"
    spko_doc.save()
    return doc

@frappe.whitelist()
def batch_stop(batch_work_log):
    doc = frappe.get_doc("Batch Work Log", batch_work_log)
    doc.update({
        "waktu_selesai": frappe.utils.now(),
        "docstatus": 1
    })
    doc.save(ignore_permissions=True)
    return doc
