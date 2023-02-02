# Copyright (c) 2023, DAS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BatchWorkLog(Document):

	def validate(self):
		self.check_spko_is_valid()

	def before_insert(self):
		self.generate_work_log()

	def before_submit(self):
		self.stop_work_log()

	def on_trash(self):
		self.delete_work_log()

	def check_spko_is_valid(self):
		array_spko = self.spkos.strip().split("\n")
		data = frappe.db.sql("select name from `tabSPKO` where name in %(spko)s",{
			"spko": array_spko
		})
		if len(array_spko) != len(data):
			frappe.throw("Terdapat SPKO ID yg tidak valid")
	
	def generate_work_log(self):
		spkos = self.spkos.strip().split("\n")
		for spko in spkos:
			value = frappe.get_value("SPKO", spko)
			if value:
				from lestari_mobile.apis.v1.work_log import start
				start(spko, self.name, self.waktu_mulai, self.operation)


	def stop_work_log(self):
		spkos = self.spkos.strip().split("\n")
		for spko in spkos:
			value = frappe.get_value("SPKO", spko)
			if value and self.is_pause == 0:
				from lestari_mobile.apis.v1.work_log import stop
				work_log = frappe.get_all("Work Log", filters=[["spko","=",spko]], order_by="creation desc")
				if len(work_log) > 0:
					stop(work_log[0]['name'], self.waktu_selesai)
			elif value and self.is_pause == 1:
				from lestari_mobile.apis.v1.work_log import pause
				work_log = frappe.get_all("Work Log", filters=[["spko","=",spko]], order_by="creation desc")
				if len(work_log) > 0:
					pause(work_log[0]['name'], self.waktu_selesai)
		pass
	
	def delete_work_log(self):
		spkos = self.spkos.strip().split("\n")
		for spko in spkos:
			value = frappe.get_value("SPKO", spko)
			if value:
				from lestari_mobile.apis.v1.work_log import stop
				work_log = frappe.get_all("Work Log", filters=[["spko","=",spko]], order_by="creation desc")
				if len(work_log) > 0:
					frappe.delete_doc("Work Log", work_log[0]["name"])
		pass
	pass
