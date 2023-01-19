import frappe

@frappe.whitelist()
def get(spok_name, using_work_log="1"):
    spko = frappe.get_value("SPKO", {"qr_code_hash": spok_name.strip()}, "name")
    if spko is None:
        spko = frappe.get_value("SPKO", spok_name.strip(), "name")
    if spko:
        if str(using_work_log) == "1":
            last_work_log = frappe.get_all("Work Log", fields=["*"], filters=[["spko","=",spok_name.strip()]], order_by="creation desc", limit_page_length=1)
        else:
            last_work_log = []
        return {
            "doc": frappe.get_doc("SPKO", spko),
            "last_work_log": last_work_log
        }
    frappe.throw("Not found")


@frappe.whitelist()
def get_multi(spok_names):
    spkos = spok_names.split("<>")
    result = []
    weight = 0
    jumlah = 0
    error = []
    for spko in spkos:
        try:
            doc = get(spko, "0")
            weight += doc["doc"].berat
            jumlah += doc["doc"].jumlah
            result.append(doc)
        except:
            error.append(spko)
    return {
        "data": result,
        "weight": weight,
        "jumlah": jumlah,
        "error": error
    }