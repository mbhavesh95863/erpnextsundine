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
	for row in data["master_purchase_order_item"]:
		return data["shipping_date"]


@frappe.whitelist()
def makeMasterPoOrder(po,ps):
	data=json.loads(po)
	data2=frappe.get_doc({
							"docstatus": 0,
							"naming_series": "MPO-",
							"doctype": "Master Purchase Order",
							"name": "New Master Purchase Order 1",
							"shipping_date": data["shipping_date"],
							"arrival_date": data["arrival_date"],
							"cad": data["cad"],
							"pallet_weight": data["pallet_weight"],
							"usd": data["usd"],
							"total_actual_cost": data["total_actual_cost"],
							"total_actual_cost_usd": data["total_actual_cost_usd"],
							"order_type": data["order_type"],
							"master_purchase_order_item": []
						})
	d=data2.insert(ignore_permissions=True)
	if d:
		for row in data["master_purchase_order_item"]:

			data3=frappe.get_doc({
								"docstatus": 0,
								"doctype": "Master Purchase Order Item",
								"name": "New Master Purchase Order Item 1",
								"owner": str(frappe.session.user),
								"parent": d.name,
								"parentfield": "master_purchase_order_item",
								"parenttype": "Master Purchase Order",
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
								"supplier_name": row["supplier_name"],
								"supplier": row["supplier"],
								"row_number": row["row_number"],
								"col_number": row["col_number"]
							})
			d1=data3.insert(ignore_permissions=True)
		poname = d.name
		makepo1(poname,ps)
		
		return d.name

@frappe.whitelist()
def makepo1(poname,ps):
	data=json.loads(ps)
	count=0
	i=0
	for row in data["details"]:
	
		data3=frappe.get_doc({
							"naming_series": "PO-",
							"doctype": "Purchase Order",
							"conversion_rate": row[0]["conversion_rate"],
							"currency": getCurrency(row[0]["supplier"]),
							"transaction_date":row[0]["shipping_date"],
							"supplier":row[0]["supplier"],
							"order_type": row[0]["order_type"],
							"docstatus": 0,
							"ignore_pricing_rule": 0,
							"schedule_date": row[0]["arrival_date"],
							"name": "New Purchase Order 1",
							"master_po_id": poname,
							"col_number": row[0]["col_number"],
							"idx": 0,
							"items": row[0]["items"],
							"price_list_currency": getCurrency(row[0]["supplier"]),
							"plc_conversion_rate": row[0]["plc_conversion_rate"],
							"total_boxes": row[0]["total_boxes"],
							"total_pallet": row[0]["total_pallet"],
							"total_net_weight": row[0]["total_net_weight"],
							"total_gross_weight_lbs": row[0]["total_gross_weight_lbs"],
							"total_weight_kg": row[0]["total_weight_kg"]
						})
		d=data3.insert(ignore_permissions=True)
		frappe.db.sql("""UPDATE `tabMaster Purchase Order Item`  SET `purchase_order` = %s
        where  parent = %s AND supplier = %s AND col_number = %s """, (d.name, poname, row[0]["supplier"], row[0]["col_number"]))
		count=count+1

@frappe.whitelist()
def getCurrency(sup):
	data=frappe.db.sql("""select default_currency from `tabSupplier` where name=%s""",sup)
	if len(data):
		return data[0][0]
	else:
		return "CAD"
		
@frappe.whitelist()
def makeReceivingSheet(master_purchase_order):
	to_date=today()
	master_po=frappe.get_doc("Master Purchase Order",str(master_purchase_order))
	
	if not frappe.db.exists("Receiving Sheet",str(master_purchase_order)):
		data2=frappe.get_doc({
							"docstatus": 0,
							"doctype": "Receiving Sheet",
							"name": "New Receiving Sheet 1",
							"master_purchase_order": master_purchase_order,
							"shipping_date": master_po.shipping_date,
							"arrival_date": master_po.arrival_date,
							"order_type": master_po.order_type,
							"receiving_date": to_date
						})
		d=data2.insert(ignore_permissions=True)
		if d:
			return d.name
	else:
		check_sheet=frappe.get_doc("Receiving Sheet",str(master_purchase_order))
		return check_sheet.name		
		
@frappe.whitelist()
def makeLandingCost(master_purchase_order):
	master_po=frappe.get_doc("Master Purchase Order",str(master_purchase_order))
	cad = master_po.cad
	usd = master_po.usd
	
	if not frappe.db.exists("Master PO Landing Cost",str(master_purchase_order)):
		data2=frappe.get_doc({
							"docstatus": 0,
							"doctype": "Master PO Landing Cost",
							"name": "New Master PO Landing Cost 1",
							"master_purchase_order": master_purchase_order,
							"cad": cad,
							"usd": usd
						})
		d=data2.insert(ignore_permissions=True)
		if d:
			return d.name
	else:
		check_sheet=frappe.get_doc("Master PO Landing Cost",str(master_purchase_order))
		return check_sheet.name
	
@frappe.whitelist()
def updateMasterPoOrder(po,ps):
	data=json.loads(po)
	master_po_data=frappe.get_doc("Master Purchase Order",str(data["name"]))
	
	master_po_data.shipping_date = data["shipping_date"]
	master_po_data.arrival_date = data["arrival_date"]
	master_po_data.cad = data["cad"]
	master_po_data.usd = data["usd"]
	master_po_data.pallet_weight = data["pallet_weight"]
	master_po_data.total_actual_cost = data["total_actual_cost"]
	master_po_data.total_actual_cost_usd = data["total_actual_cost_usd"]
	master_po_data.order_type = data["order_type"]
	
	master_po_data.save(ignore_permissions=True)
	
	frappe.db.sql("""delete from `tabMaster Purchase Order Item` 
        where parent = %s """, master_po_data.name)
	
	for row in data["master_purchase_order_item"]:

			data3=frappe.get_doc({
								"docstatus": 0,
								"doctype": "Master Purchase Order Item",
								"name": "New Master Purchase Order Item 1",
								"owner": str(frappe.session.user),
								"parent": master_po_data.name,
								"parentfield": "master_purchase_order_item",
								"parenttype": "Master Purchase Order",
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
								"supplier_name": row["supplier_name"],
								"supplier": row["supplier"],
								"row_number": row["row_number"],
								"col_number": row["col_number"]
							})
			d1=data3.insert(ignore_permissions=True)
	
	return master_po_data.name

@frappe.whitelist()
def getCreditto(cur):

	if cur=="USD":
		return "2200 - USD Accounts Payable - ."
	else:
		return "2100 - CAD Accounts Payable - ."
	
@frappe.whitelist()
def saveReceivingSheet(po,ps):
	data=json.loads(po)
	datap=json.loads(ps)
	for row in data["master_purchase_order_items"]:
		
		master_po_data=frappe.get_doc("Master Purchase Order Item",str(row["name"]))
		master_po_data.received_qty = row["received_qty"]
		master_po_data.save(ignore_permissions=True)
				
	for row1 in datap["details"]:
	
		data3=frappe.get_doc({
							"docstatus":0, 
							"status": "Draft",
							"doctype": "Purchase Receipt",
							"name": "New Purchase Receipt 1",
							"posting_date": today(),
							"company": "Sundine Produce",
							"currency": getCurrency(row1[0]["supplier"]),
							"supplier":row1[0]["supplier"],
							"items": row1[0]["items"],
							"total_boxes": row1[0]["total_boxes"],
							"total_pallet": row1[0]["total_pallet"],
							"total_net_weight": row1[0]["total_net_weight"],
							"total_gross_weight_lbs": row1[0]["total_gross_weight_lbs"],
							"total_weight_kg": row1[0]["total_weight_kg"]
						})
		d=data3.insert(ignore_permissions=True)
		d.submit()
	
	
	return data["master_purchase_order"]
	
@frappe.whitelist()
def MasterPOitemsList(poname):
	itm_list=frappe.db.sql("""select mpoi.name,mpoi.item_name,mpoi.item_code,mpoi.weight_per_unit,mpoi.purchase_pallets,(SELECT sum(received_qty) FROM `tabMaster Purchase Order Item` WHERE mpoi.row_number = row_number and parent = mpoi.parent)ttl_qty,(SELECT sum(received_qty * price)/sum(received_qty) FROM `tabMaster Purchase Order Item` WHERE mpoi.row_number = row_number and parent = mpoi.parent)avg_price,(SELECT sum(received_qty * price) FROM `tabMaster Purchase Order Item` WHERE  parent = mpoi.parent)ttl_cad,mpoi.uom from `tabMaster Purchase Order Item` mpoi where mpoi.parent=%s GROUP BY mpoi.row_number """,str(poname))
	
	return itm_list
	
@frappe.whitelist()
def saveLandingCostPO(po):
	data=json.loads(po)
	count=0
	i=0
	for row1 in data["landing_cost_suppliers"]:
	
		data3=frappe.get_doc({
							"docstatus": 1, 
							"status": "Draft",
							"doctype": "Purchase Invoice",
							"naming_series": "PINV-",
							"name": "New Purchase Invoice 1",
							"supplier":row1["supplier"],
							"posting_date": today(),
							"due_date": data["arrival_date"],
							"master_po_id": data["master_purchase_order"],
							"idx": 0,
							"items": row1["items"],
							"credit_to": "2100 - CAD Accounts Payable  - ."
						})
		d=data3.insert(ignore_permissions=True)
		count=count+1
		
@frappe.whitelist()
def saveLandingCostPO1(po):
	data=json.loads(po)
	count=0
	i=0
	for row in data["landing_cost_suppliers"]:
	
		data3=frappe.get_doc({
							"naming_series": "PO-",
							"doctype": "Purchase Order",
							"conversion_rate": 1,
							"transaction_date":data["shipping_date"],
							"supplier":row["supplier"],
							"currency": getCurrency(row["supplier"]),
							"docstatus": 1,
							"buying_price_list": "Standard Buying",
							"ignore_pricing_rule": 0,
							"status": "Draft",
							"schedule_date": data["arrival_date"],
							"name": "New Purchase Order 1",
							"master_po_id": data["master_purchase_order"],
							"idx": 0,
							"items": row["items"],
							"taxes": row["taxes"],
							"price_list_currency": getCurrency(row["supplier"]),
							"plc_conversion_rate": 1
						})
		d=data3.insert(ignore_permissions=True)
		count=count+1
		
	for row1 in data["landing_cost_suppliers1"]:
	
		data4=frappe.get_doc({
							"docstatus": 1, 
							"status": "Draft",
							"doctype": "Purchase Invoice",
							"naming_series": "PINV-",
							"name": "New Purchase Invoice 1",
							"supplier":row1["supplier"],
							"currency": getCurrency(row1["supplier"]),
							"posting_date": today(),
							"due_date": add_days(today(),2),
							"master_po_id": data["master_purchase_order"],
							"idx": 0,
							"items": row1["items"],
							"taxes": row1["taxes"]
						})
		d1=data4.insert(ignore_permissions=True)
		count=count+1
		
	return count

@frappe.whitelist()
def saveReceivingSheet1(po,ps):
	data=json.loads(po)
	datap=json.loads(ps)
	# for row in data["master_purchase_order_items"]:
		
	# 	master_po_data=frappe.get_doc("Master Purchase Order Item",str(row["name"]))
	# 	master_po_data.received_qty = row["received_qty"]
	# 	master_po_data.save(ignore_permissions=True)
				
	for row1 in datap["details"]:
		#return row1[0]["items"]
		return savePurchaseReceiptForMasterPO(row1[0]["supplier"],json.dumps(row1[0]["items"]))
	
		# data3=frappe.get_doc({
		# 					"docstatus": 1, 
		# 					"status": "Draft",
		# 					"doctype": "Purchase Invoice",
		# 					"naming_series": "PINV-",
		# 					"name": "New Purchase Invoice 1",
		# 					"currency": getCurrency(row1[0]["supplier"]),
		# 					"supplier":row1[0]["supplier"],
		# 					"posting_date": today(),
		# 					"master_po_id": row1[0]["master_purchase_order"],
		# 					"idx": 0,
		# 					"items": row1[0]["items"]
		# 				})
		# d=data3.insert(ignore_permissions=True)
	
	




@frappe.whitelist()
def savePurchaseReceiptForMasterPO(supplier,item_object):
	itemobj=json.loads(item_object)
	doc=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Purchase Receipt",
						"name": "New Purchase Receipt 1",
						"naming_series": "PREC-",
						"posting_date": today(),
						"company": "Sundine Produce",
						"currency": getCurrency(supplier),
						"status": "Draft",
						"items": [],
						"supplier":supplier,
						"total_net_weight": "",
						"total_boxes": "",
						"total_pallet": "",
						"total_weight_kg": ""
					})
	#return doc
	doc1=doc.insert()
	for row in itemobj:
		savePurchaseReceiptItem(row["item_code"],row["qty"],doc1.name)
	doc2=frappe.get_doc("Purchase Receipt",doc1.name)
	return doc2




@frappe.whitelist()
def savePurchaseReceiptItem(item_code,qty,parent):
	doc=frappe.get_doc({
							"docstatus": 0,
							"doctype": "Purchase Receipt Item",
							"name": "New Purchase Receipt Item 1",
							"parent":parent,
							"parentfield": "items",
							"parenttype": "Purchase Receipt",
							"received_qty":qty,
							"item_code":item_code,
							"warehouse":"Sundine Kestrel- . - ."
						})
	doc.insert()

