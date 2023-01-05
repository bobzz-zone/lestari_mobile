import frappe
import qrcode

def execute(code, doctype, docname, docfield, is_private=1):
    img=qrcode.make(code)

    
    filename = "{}.png".format(code)
    from lestari_mobile.functions.get_filename_fullpath import execute
    fullpath = execute(filename, is_private)
    img.save(fullpath)

    from lestari_mobile.functions.get_filename_fileurl import execute
    fileurl = execute(filename, is_private)

    from lestari_mobile.functions.get_filename_filesize import execute
    filesize = execute(fullpath)
    
    doc = frappe.new_doc("File")
    doc.update({
        "file_name": filename,
        "is_private": is_private,
        "file_url": fileurl,
        "file_size": filesize,
        "folder": "Home/Attachments",
        "attached_to_doctype": doctype,
        "attached_to_name": docname,
        "attached_to_field": docfield,
        "doctype": "File"
        })
    doc.insert(ignore_permissions=True)

    frappe.db.set_value(doctype, docname, docfield, fileurl)
    frappe.db.commit()