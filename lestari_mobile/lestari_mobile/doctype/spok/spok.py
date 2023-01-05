# Copyright (c) 2022, DAS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import hashlib

class SPOK(Document):
	def after_insert(self):
		code = hashlib.md5(self.name.encode()).hexdigest()
		from lestari_mobile.qr_code.generate_qr import execute
		execute(code, self.doctype, self.name, 'qr_image', 0)
		frappe.db.set_value(self.doctype, self.name, "qr_code_hash", code)
	pass
