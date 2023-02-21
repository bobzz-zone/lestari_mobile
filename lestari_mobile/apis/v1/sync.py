import frappe
import math
from frappe.utils import add_to_date
from datetime import datetime

SPKO_DAYS_BEFORE = -3

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
    keterangan_pause = {
        "total_page": math.ceil(total_data / limit_page_length),
        "total_data": total_data
    }

    doctype = 'Operation'
    workstation = frappe.get_value("Employee", {"id_employee": employee_id}, "workstation")
    filters = get_filters(doctype, array_last_modifieds[1], None, workstation)
    if workstation is not None:
        total_data = frappe.db.count(doctype, filters=filters)
    else:
        total_data = 0
    
    operation = {
        "total_page": math.ceil(total_data / limit_page_length),
        "total_data": total_data
    }

    doctype = 'SPKO'
    filters = get_filters(doctype, array_last_modifieds[2], None, None, None, SPKO_DAYS_BEFORE)
    spkos = frappe.get_all(doctype, filters=filters, pluck="name")
    total_data = len(spkos)
    print(filters)
    spko = {
        "total_page": math.ceil(total_data / limit_page_length),
        "total_data": total_data
    }

    doctype = 'Work Log'
    filters = get_filters(doctype, array_last_modifieds[3], None, None, spkos)
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
def download(doctype, last_modified, employee_id,page,limit_page_length=100):
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
        employee_id = None
    else:
        days_before = None
    if doctype == "Work Log":
        spkos = frappe.get_all("SPKO", filters=get_filters("SPKO", last_modified, None, None, None, SPKO_DAYS_BEFORE), pluck="name")
        employee_id = None
    else:
        spkos = None
    filters = get_filters(doctype, last_modified, employee_id, workstation, spkos, days_before)

    order_by = "name asc"
    if doctype == "Operation":
        order_by = "index_operation asc"
    return limit_page_length
    return frappe.get_all(doctype, filters=filters, fields=["*"], order_by=order_by,limit_page_length=int(limit_page_length),limit_start=int(page) * int(limit_page_length))