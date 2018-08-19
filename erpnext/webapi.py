from __future__ import unicode_literals
import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

from datetime import datetime
from frappe.utils import getdate, validate_email_add, today, add_years,add_days,format_datetime,fmt_money, flt
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
from frappe.model.naming import make_autoname
from frappe import throw, _, scrub
import frappe.permissions
from frappe.model.document import Document
from frappe.desk.form.linked_with import get_linked_docs
from frappe.desk.form.save import cancel
from frappe.client import delete
import json
import collections
# import urllib
# import urllib2

@frappe.whitelist()
def test():
	return "test"


@frappe.whitelist(allow_guest=True)
def itemList():
	item_list=frappe.get_list("Item",filters={'has_variants':0},fields=["item_name", "item_code", "standard_rate", "weight_per_unit", "item_group","description","website_image"])
	if item_list:
		return item_list
	else:	
		return _(False)


@frappe.whitelist()
def getLinkedDocName():
	data=get_linked_docs(doctype='Delivery Note',name='DN-00021',linkinfo={"Sales Invoice": {
			"fieldname": "name"
		}})
	return data

