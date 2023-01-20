import frappe

@frappe.whitelist()
def get():
    employee = frappe.get_value("Employee", {"user_id": frappe.session.user})
    data = []
    if employee:
        workstation = frappe.get_value("Employee", employee, "workstation")
        data = frappe.get_all("Operation",fields=["*"], filters=[["workstation","=", workstation]],order_by="index_operation asc")    
    else:
        data = frappe.get_list("Operation",fields=["*"],order_by="index_operation asc")
    results = []
    for item in data:
        item['proses_kerja'] = item['name']
        results.append(item)
    return results

