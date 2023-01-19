# Copyright (c) 2023, DAS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BatchWorkLog(Document):

	def validate(self):
		self.check_spko_is_valid()
		self.check_spko_is_on_progress()

	def check_spko_is_valid(self):
		array_spko = self.spkos.split("\n")
		data = frappe.db.sql("select name from `tabSPKO` where name in %(spko)s",{
			"spko": array_spko
		})
		if len(array_spko) != len(data):
			frappe.throw("Terdapat SPKO ID yg tidak valid")
	
	def check_spko_is_on_progress(self):
		pass
	pass
