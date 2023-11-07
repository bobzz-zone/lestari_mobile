import frappe
import math
from frappe.utils import add_to_date
from datetime import datetime

SPKO_DAYS_BEFORE = -7

def get_filters(doctype, last_modified, employee_id=None, workstation=None, spkos=None, creation_day=None):
    filters = {}
    filters["modified"] =  [">=", last_modified]
    if employee_id is not None:
        filters["employee_id"] = employee_id
    if workstation is not None:
        filters["workstation"] = workstation
    if spkos is not None:
        if len(spkos) > 0:
            filters["spko"] = ["in", spkos]
    if creation_day is not None:
        today_before = add_to_date(datetime.now(), days=creation_day)
        filters['creation'] = [">=", str(today_before).split(" ")[0]]
    return filters
    

@frappe.whitelist()
def meta(last_modifieds, employee_id, limit_page_length=100):
    limit_page_length = frappe.get_single("Sync Settings").per_page
    array_last_modifieds = last_modifieds.split(',')
    doctype = 'Keterangan Pause'
    filters = get_filters(doctype, array_last_modifieds[0])
    
    total_data = frappe.db.count(doctype, filters=filters)
    filters["modified"] = [">=", "1970-01-01"]
    keterangan_pause = {
        "total_page": math.ceil(total_data / limit_page_length),
        "total_data": frappe.db.count(doctype, filters=filters)
    }

    doctype = 'Operation'
    workstation = frappe.get_value("Employee", {"id_employee": employee_id}, "workstation")
    filters = get_filters(doctype, array_last_modifieds[1], None, workstation)
    if workstation is not None:
        total_data = frappe.db.count(doctype, filters=filters)
    else:
        total_data = 0
    filters["modified"] = [">=", "1970-01-01"]
    operation = {
        "total_page": math.ceil(total_data / limit_page_length),
        "total_data": frappe.db.count(doctype, filters=filters)
    }

    doctype = 'SPKO'
    filters = get_filters(doctype, "1970-01-01", None, workstation, None, SPKO_DAYS_BEFORE)
    spkos = frappe.get_all(doctype, filters=filters, pluck="name")
    total_data = len(spkos)
    print(filters)
    spko = {
        "total_page": math.ceil(total_data / limit_page_length),
        "total_data": total_data
    }

    doctype = 'Work Log'
    filters = get_filters(doctype, "1970-01-01", employee_id, None, spkos)
    total_data = frappe.db.count(doctype, filters=filters)
    
    worklog = {
        "total_page": math.ceil(total_data / limit_page_length),
        "total_data": total_data
    }
    return {
        "keterangan_pause": keterangan_pause,
        "operation": operation,
        "spko": spko,
        "worklog": worklog
    }

@frappe.whitelist()
def download(doctype, last_modified, employee_id,page,limit_page_length=100, is_indexing=False):
    limit_page_length = frappe.get_single("Sync Settings").per_page
    if doctype == "Keterangan Pause":
        employee_id = None
    if doctype == "Operation":
        workstation = frappe.get_value("Employee", {"id_employee": employee_id}, "workstation")
        employee_id = None
    else:
        workstation = None
    
    if doctype == "SPKO":
        days_before = SPKO_DAYS_BEFORE
        workstation = frappe.get_value("Employee", {"id_employee": employee_id}, "workstation")
        employee_id = None
    else:
        days_before = None
    if doctype == "Work Log":
        spkos = frappe.get_all("SPKO", filters=get_filters("SPKO", "1970-01-01", None, workstation, None, SPKO_DAYS_BEFORE), pluck="name")
        days_before = None
        last_modified = "1970-01-01"
    else:
        spkos = None
    filters = get_filters(doctype, last_modified, employee_id, workstation, spkos, days_before)
    print(filters)
    order_by = "name asc"
    if doctype == "Operation":
        order_by = "index_operation asc"
    

    result = frappe.get_all(doctype, filters=filters, fields=["*"], order_by=order_by,limit_page_length=int(limit_page_length),limit_start=int(page) * int(limit_page_length))
    if is_indexing == "" or is_indexing == False or is_indexing is None or is_indexing == "null":
        return result
    else:
        last_modified = frappe.utils.now()
        if (len(result) > 0):
            last_modified = result[-1]["modified"]
        return {
            "data": result,
            "total_data": len(result),
            "last_modified": last_modified
        }
@frappe.whitelist()
def setReturn(success, message, data, error):
    data = {
        "success":success,
        "message":message,
        "data":data,
        "error":error
    }
    return data
@frappe.whitelist()
def DownloadWorklog(id_employee=None, creation=None):
    if id_employee is None:
        data_return = setReturn(False, "Id employee is required", None, None)
        # return data_return as json with 400 status code in erpnext
        frappe.local.response['http_status_code'] = 400
        return data_return
    if creation is None:
        data_return = setReturn(False, "Creation is required", None, None)
        # return data_return as json with 400 status code in erpnext
        frappe.local.response['http_status_code'] = 400
        return data_return

    # get data worklog
    worklogs = a = frappe.get_list("Work log Testing", filters={"employee_id":id_employee,"creation":[">",creation]})
    worklog_datas = []
    for item in worklogs:
        worklog = frappe.get_doc("Work log Testing", item)
        data = {
            "name":worklog.name,
            "operation":worklog.operation,
            "is_batch":worklog.is_batch,
            "employee":worklog.employee,
            "employee_id":worklog.employee_id,
            "employee_name":worklog.employee_name,
            "waktu_mulai":worklog.waktu_mulai,
            "waktu_selesai":worklog.waktu_selesai,
            "total_rusak":worklog.total_rusak,
            "total_detik":worklog.total_detik,
            "total_detik_working":worklog.total_detik_working,
            "total_detik_pause":worklog.total_detik_pause,
            "uuid":worklog.uuid,
            "upload_time":worklog.creation,
            "list_pause":[],
            "list_spko":[],
            "total_pcs":worklog.total_pcs
        }
        for spko in worklog.list_spko:
            data_spko = {
                "spko":spko.spko,
                "total_rusak":spko.total_rusak,
                "qr_code_hash":frappe.get_value("SPKO",spko.spko,["qr_code_hash"])
            }
            data["list_spko"].append(data_spko)

        for pause in worklog.list_pause:
            data_pause = {
                "start_pause":pause.start_pause,
                "end_pause":pause.end_pause,
                "keterangan_pause":pause.keterangan_pause,
                "catatan":pause.catatan,
                "total_seconds":pause.total_seconds
            }
            data["list_pause"].append(data_pause)

        worklog_datas.append(data)
    
    data_return = setReturn(True, "Success", worklog_datas, None)
    frappe.local.response['http_status_code'] = 200
    return data_return
