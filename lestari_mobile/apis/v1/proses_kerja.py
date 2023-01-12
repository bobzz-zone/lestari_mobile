import frappe

@frappe.whitelist()
def get():
    data = frappe.get_list("Operation",fields=["*"])
    results = []
    for item in data:
        item['proses_kerja'] = item['name']
        results.append(item)
    return results

