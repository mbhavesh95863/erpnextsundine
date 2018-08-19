from __future__ import unicode_literals
import frappe

from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.utils import getdate, validate_email_add, today, add_years,add_days,format_datetime
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
from datetime import datetime
from frappe.model.naming import make_autoname
from frappe import throw, _, scrub
import frappe.permissions
from frappe.model.document import Document
import json
import collections


@frappe.whitelist()
def test(po):
	data=json.loads(po)
	for row in data["master_sales_order_item"]:
		return data["shipping_date"]

@frappe.whitelist()
def makeMasterPoOrder(po,ps):
	data=json.loads(po)
	data2=frappe.get_doc({
							"docstatus": 0,
							"naming_series": "MSO-",
							"doctype": "Master Sales Order",
							"name": "New Master Sales Order 1",
							"shipping_date": data["shipping_date"],
							"delivery_date": data["delivery_date"],
							"cad": data["cad"],
							"pallet_weight": data["pallet_weight"],
							"usd": data["usd"],
							"total_actual_cost": data["total_actual_cost"],
							"total_actual_cost_usd": data["total_actual_cost_usd"],
							"order_type": data["order_type"],
							"master_sales_order_item": []
						})
	d=data2.insert(ignore_permissions=True)
	if d:
		for row in data["master_sales_order_item"]:

			data3=frappe.get_doc({
								"docstatus": 0,
								"doctype": "Master Sales Order Item",
								"name": "New Master Sales Order Item 1",
								"owner": str(frappe.session.user),
								"parent": d.name,
								"parentfield": "master_sales_order_item",
								"parenttype": "Master Sales Order",
								"qty": row["qty"],
								"price": row["price"],
								"weight": row["weight"],
								"received_qty": row["received_qty"],
								"default_currency": row["default_currency"],
								"weight_per_unit": row["weight"],
								"gross_weight": row["gross_weight"],
								"uom": row["uom"],
								"description": row["description"],
								"purchase_pallets": row["purchase_pallets"],
								"item_code": row["item_code"],
								"item_name": row["item_name"],
								"customer_name": row["customer_name"],
								"customer": row["customer"],
								"row_number": row["row_number"],
								"col_number": row["col_number"]
							})
			d1=data3.insert(ignore_permissions=True)
		poname = d.name
		makeso1(poname,ps)
		
		return d.name

@frappe.whitelist()
def makeso1(poname,ps):
	data=json.loads(ps)
	count=0
	i=0
	for row in data["details"]:
	
		data3=frappe.get_doc({
							"naming_series": "SO-",
							"doctype": "Sales Order",
							"conversion_rate": 1,
							"currency": getCurrency(row[0]["customer"]),
							"transaction_date":row[0]["shipping_date"],
							"customer":row[0]["customer"],
							"docstatus": 0,
							"ignore_pricing_rule": 0,
							"schedule_date": row[0]["delivery_date"],
							"name": "New Sales Order 1",
							"master_so_id": poname,
							"idx": 0,
							"items": row[0]["items"],
							"price_list_currency": getCurrency(row[0]["customer"]),
							"plc_conversion_rate": 1
						})
		d=data3.insert(ignore_permissions=True)
		count=count+1

@frappe.whitelist()
def getCurrency(sup):
	data=frappe.db.sql("""select default_currency from `tabCustomer` where name=%s""",sup)
	if len(data):
		return data[0][0]
	else:
		return "CAD"
		
@frappe.whitelist()
def makeReceivingSheet(master_sales_order):
	to_date=today()
	master_so=frappe.get_doc("Master Sales Order",str(master_sales_order))
	
	if not frappe.db.exists("Master Sales Receiving Mode",str(master_sales_order)):
		data2=frappe.get_doc({
							"docstatus": 0,
							"doctype": "Master Sales Receiving Mode",
							"name": "New Master Sales Receiving Mode 1",
							"master_sales_order": master_sales_order,
							"shipping_date": master_so.shipping_date,
							"delivery_date": master_so.delivery_date,
							"order_type": master_so.order_type,
							"receiving_date": to_date
						})
		d=data2.insert(ignore_permissions=True)
		if d:
			return d.name
	else:
		check_sheet=frappe.get_doc("Receiving Sheet",str(master_sales_order))
		return check_sheet.name		
		

@frappe.whitelist()
def updateMasterPoOrder(po,ps):
	data=json.loads(po)
	master_so_data=frappe.get_doc("Master Sales Order",str(data["name"]))
	
	master_so_data.shipping_date = data["shipping_date"]
	master_so_data.delivery_date = data["delivery_date"]
	master_so_data.cad = data["cad"]
	master_so_data.usd = data["usd"]
	master_so_data.pallet_weight = data["pallet_weight"]
	master_so_data.total_actual_cost = data["total_actual_cost"]
	master_so_data.total_actual_cost_usd = data["total_actual_cost_usd"]
	master_so_data.order_type = data["order_type"]
	
	master_so_data.save(ignore_permissions=True)
	
	frappe.db.sql("""delete from `tabMaster Sales Order Item` 
        where parent = %s """, master_so_data.name)
	
	for row in data["master_sales_order_item"]:

			data3=frappe.get_doc({
								"docstatus": 0,
								"doctype": "Master Sales Order Item",
								"name": "New Master Sales Order Item 1",
								"owner": str(frappe.session.user),
								"parent": master_so_data.name,
								"parentfield": "master_sales_order_item",
								"parenttype": "Master Sales Order",
								"qty": row["qty"],
								"price": row["price"],
								"weight": row["weight"],
								"weight_per_unit": row["weight"],
								"gross_weight": row["gross_weight"],
								"uom": row["uom"],
								"description": row["description"],
								"purchase_pallets": row["purchase_pallets"],
								"item_code": row["item_code"],
								"item_name": row["item_name"],
								"received_qty": row["received_qty"],
								"default_currency": row["default_currency"],
								"customer_name": row["customer_name"],
								"customer": row["customer"],
								"row_number": row["row_number"],
								"col_number": row["col_number"]
							})
			d1=data3.insert(ignore_permissions=True)
	
	return master_so_data.name
		
@frappe.whitelist()
def saveReceivingSheet(po,ps):
	data=json.loads(po)
	datap=json.loads(ps)
	for row in data["master_sales_order_items"]:
		
		master_so_data=frappe.get_doc("Master Sales Order Item",str(row["name"]))
		master_so_data.received_qty = row["received_qty"]
		master_so_data.save(ignore_permissions=True)
				
	for row1 in datap["details"]:
	
		data3=frappe.get_doc({
							"docstatus": 1, 
							"status": "Draft",
							"doctype": "Sales Invoice",
							"naming_series": "SINV-",
							"name": "New Sales Invoice 1",
							"currency": getCurrency(row1[0]["customer"]),
							"customer":row1[0]["customer"],
							"posting_date": today(),
							"due_date": row1[0]["delivery_date"],
							"master_so_id": row1[0]["master_sales_order"],
							"idx": 0
						})
		d=data3.insert(ignore_permissions=True)
	
	
	return data["master_sales_order"]
	