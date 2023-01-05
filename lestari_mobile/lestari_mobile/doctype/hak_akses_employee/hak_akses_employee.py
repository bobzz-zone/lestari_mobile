# Copyright (c) 2023, DAS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class HakAksesEmployee(Document):
	def after_insert(self):
		from lestari_mobile.qr_code.generate_qr import execute
		execute(self.name, self.doctype, self.name, 'qr_image', 0)
	
	pass
