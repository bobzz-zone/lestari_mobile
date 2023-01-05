# Copyright (c) 2022, DAS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WorkLog(Document):
	def before_submit(self):
		if self.waktu_mulai and self.waktu_selesai:
			diff_in_seconds = frappe.db.sql("select UNIX_TIMESTAMP('{}') - UNIX_TIMESTAMP('{}') as diff".format(self.waktu_selesai, self.waktu_mulai))[0][0]
			if diff_in_seconds > 0:
				self.jam = diff_in_seconds / 3600
				self.menit = diff_in_seconds % 3600 / 60
				self.detik = diff_in_seconds % 3600 % 60

	pass
