# Copyright (c) 2022, DAS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WorkLog(Document):
	def before_submit(self):
		if self.waktu_mulai and self.waktu_selesai:
			diff_in_seconds = frappe.db.sql("select UNIX_TIMESTAMP('{}') - UNIX_TIMESTAMP('{}') as diff".format(self.waktu_selesai, self.waktu_mulai))[0][0]
			if diff_in_seconds > 0:
				self.jam = int(diff_in_seconds / 3600)
				self.menit = int(diff_in_seconds % 3600 / 60)
				self.detik = int(diff_in_seconds % 3600 % 60)
		if self.resume_from is not None:
			resume_from_doc = frappe.get_doc("Work Log", self.resume_from)
			diff_in_seconds = (resume_from_doc.jam_akumulasi * 3600) + (self.jam * 3600) + (resume_from_doc.menit_akumulasi * 60) + (self.menit * 60) + (resume_from_doc.detik_akumulasi) + (self.detik)
			self.jam_akumulasi = int(diff_in_seconds / 3600)
			self.menit_akumulasi = int(diff_in_seconds % 3600 / 60)
			self.detik_akumulasi = int(diff_in_seconds % 3600 % 60)
		else:
			self.jam_akumulasi = self.jam
			self.menit_akumulasi = self.menit
			self.detik_akumulasi = self.detik
		
		frappe.db.set_value("SPKO", self.spko, {
			"jam_akumulasi": self.jam_akumulasi,
			"menit_akumulasi": self.menit_akumulasi,
			"detik_akumulasi": self.detik_akumulasi,
		}) 
	pass
