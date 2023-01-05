import frappe


def execute(filename, is_private=0):
    site_path = frappe.utils.get_bench_path() + '/sites' + frappe.utils.get_site_path().replace('./','/')
    if is_private == 0:
        public_path = site_path + '/public/files/'
        if '.' not in filename:
            filename = filename + '.jpg'
        else:
            filename = filename
        file_url = '/public/files/' + filename
    else:
        private_path = site_path + '/private/files/'
        if '.' not in filename:
            filename = filename + '.jpg'
        else:
            filename = filename
        file_url = '/private/files/' + filename
    return site_path + file_url