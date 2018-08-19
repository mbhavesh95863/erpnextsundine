from __future__ import unicode_literals
import frappe
from frappe.utils import cint, get_gravatar,flt,format_datetime, now_datetime,add_days,today,formatdate,date_diff,getdate,get_last_day
from frappe import throw, msgprint, _
from frappe.utils.password import update_password as _update_password
from frappe.desk.notifications import clear_notifications
from frappe.utils.user import get_system_managers
from erpnext.accounts.doctype.sales_invoice.sales_invoice import make_delivery_note
import frappe.permissions
import frappe.share
import re
import string
import random
import json
import time
from datetime import datetime
from datetime import date
from datetime import timedelta
import collections
import math
import logging

d1=[]
d2=[]


@frappe.whitelist()
def get_items(date1):
	object_list=[]
	# item_list=frappe.db.sql("""select distinct si.item_code,si.item_name from `tabSales Order` so inner join `tabSales Order Item` si on so.name=si.parent where si.qty>0 and so.transaction_date between %s and %s""",(date1,add_days(date1,5)))
	# for row in item_list:
	# 	balance_qty = frappe.db.sql("""select sum(qty_after_transaction) from `tabStock Ledger Entry`	
	# 	where item_code=%s and is_cancelled='No' limit 1""", (row[0]))
	# 	if not len(balance_qty):
	# 		b_qty=0
	# 	else:
	# 		b_qty=balance_qty[0][0]

	# 	infinity_sale_qty=frappe.db.sql("""select sum(qty) from `tabSales Order Item` where item_code=%s and delivery_date>=%s""",(row[0],today()))
	# 	if not len(infinity_sale_qty):
	# 		inf_s_qty=0
	# 	else:
	# 		inf_s_qty=infinity_sale_qty[0][0]

	# 	infinity_purchase_qty=frappe.db.sql("""select sum(qty) from `tabPurchase Order Item` where item_code=%s and schedule_date>=%s""",(row[0],today()))
	# 	if not len(infinity_purchase_qty):
	# 		inf_p_qty=0
	# 	else:
	# 		inf_p_qty=infinity_purchase_qty[0][0]

	# 	week_sales_qty=frappe.db.sql("""select sum(qty) from `tabSales Order Item` where item_code=%s and delivery_date between %s and %s""",(row[0],(today()),add_days(today(),5)))
	# 	if not len(week_sales_qty):
	# 		week_s_qty=0
	# 	else:
	# 		week_s_qty=week_sales_qty[0][0]

	# 	week_purchase_qty=frappe.db.sql("""select sum(qty) from `tabPurchase Order Item` where item_code=%s and schedule_date between %s and %s""",(row[0],(today()),add_days(today(),5)))
	# 	if not len(week_purchase_qty):
	# 		week_p_qty=0
	# 	else:
	# 		week_p_qty=week_purchase_qty[0][0]

	
	# 	if b_qty==None:
	# 		b_qty=0
	# 	if inf_s_qty==None:
	# 		inf_s_qty=0
	# 	if inf_p_qty==None:
	# 		inf_p_qty=0
	# 	if week_s_qty==None:
	# 		week_s_qty=0
	# 	if week_p_qty==None:
	# 		week_p_qty=0
			
			
	# 	d1 = collections.OrderedDict()
	# 	d1['item_code']=row[0]
	# 	d1['item_name']=row[1]
	# 	d1['balance_qty']=b_qty
	# 	d1['infinity_sales_qty']=inf_s_qty
	# 	d1['infinity_purchase_qty']=inf_p_qty
	# 	d1['week_sales_qty']=week_s_qty
	# 	d1['week_purchase_qty']=week_p_qty
	# 	object_list.append(d1)
		




	item_list1=frappe.db.sql("""select distinct si.item_code,si.item_name from `tabSales Order` so inner join `tabSales Order Item` si on so.name=si.parent where si.qty>0  and so.transaction_date>=%s and so.docstatus=0""",date1)
	for row in item_list1:
		balance_qty = frappe.db.sql("""select qty_after_transaction from `tabStock Ledger Entry`	
		where item_code=%s and is_cancelled='No' order by posting_date desc, posting_time desc, name desc limit 1""", (row[0]))
		if not len(balance_qty):
			b_qty=0
		else:
			b_qty=balance_qty[0][0]

		infinity_sale_qty=frappe.db.sql("""select sum(si.qty) from  `tabSales Order` so inner join `tabSales Order Item` si on so.name=si.parent where si.item_code=%s and so.delivery_date>=%s and so.docstatus=0""",(row[0],date1))
		if not len(infinity_sale_qty):
			inf_s_qty=0
		else:
			inf_s_qty=infinity_sale_qty[0][0]

		infinity_purchase_qty=frappe.db.sql("""select sum(qty) from `tabPurchase Order Item` where item_code=%s and schedule_date>=%s and docstatus=0""",(row[0],date1))
		if not len(infinity_purchase_qty):
			inf_p_qty=0
		else:
			inf_p_qty=infinity_purchase_qty[0][0]

		week_sales_qty=frappe.db.sql("""select sum(si.qty) from  `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent  where si.item_code=%s and so.docstatus=0 and so.delivery_date between %s and %s group by si.item_code""",(row[0],date1,add_days(date1,4)))
		#return week_sales_qty
		if not len(week_sales_qty):
			week_s_qty=0
		else:
			week_s_qty=week_sales_qty[0][0]

		week_purchase_qty=frappe.db.sql("""select sum(qty) from `tabPurchase Order Item` where item_code=%s and schedule_date between %s and %s and docstatus=0""",(row[0],(date1),add_days(date1,5)))
		if not len(week_purchase_qty):
			week_p_qty=0
		else:
			week_p_qty=week_purchase_qty[0][0]

	
		if b_qty==None:
			b_qty=0
		if inf_s_qty==None:
			inf_s_qty=0
		if inf_p_qty==None:
			inf_p_qty=0
		if week_s_qty==None:
			week_s_qty=0
		if week_p_qty==None:
			week_p_qty=0

		dayname=getdate(date1).strftime("%A")
		first1=frappe.db.sql("""select sum(si.qty) from `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent where si.item_code=%s and so.delivery_date=%s and so.docstatus=0""",(row[0],date1))
		second1=frappe.db.sql("""select sum(si.qty) from `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent where si.item_code=%s and so.delivery_date=%s and so.docstatus=0""",(row[0],add_days(date1,1)))
		third1=frappe.db.sql("""select sum(si.qty) from `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent where si.item_code=%s and so.delivery_date=%s and so.docstatus=0""",(row[0],add_days(date1,2)))
		four1=frappe.db.sql("""select sum(si.qty) from `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent where si.item_code=%s and so.delivery_date=%s and so.docstatus=0""",(row[0],add_days(date1,3)))
		five1=frappe.db.sql("""select sum(si.qty) from `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent where si.item_code=%s and so.delivery_date=%s and so.docstatus=0""",(row[0],add_days(date1,4)))
		
		if not first1[0][0]==None:
			first=first1[0][0]
		else:
			first=0

		if not second1[0][0]==None:
			second=second1[0][0]
		else:
			second=0

		if not third1[0][0]==None:
			third=third1[0][0]
		else:
			third=0

		if not four1[0][0]==None:
			four=four1[0][0]
		else:
			four=0

		if not five1[0][0]==None:
			five=five1[0][0]
		else:
			five=0

			
		d1 = collections.OrderedDict()
		d1['item_code']=row[0]
		d1['item_name']=row[1]
		d1['balance_qty']=b_qty
		d1['infinity_sales_qty']=inf_s_qty
		d1['infinity_purchase_qty']=inf_p_qty
		d1['week_sales_qty']=week_s_qty
		d1['week_purchase_qty']=week_p_qty
		d1['dayname']=dayname
		d1['first_date']=date1
		d1['second_date']=add_days(date1,1)
		d1['third_date']=add_days(date1,2)
		d1['four_date']=add_days(date1,3)
		d1['five_date']=add_days(date1,4)
		d1['first']=first
		d1['second']=second
		d1['third']=third
		d1['four']=four
		d1['five']=five
		object_list.append(d1)
		
		
		
		
	return object_list


@frappe.whitelist(allow_guest=True)
def get_order_details_infinity(item,date1):
	data=frappe.db.sql("""select so.name,so.customer,si.item_code,si.item_name,si.qty from `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent where si.item_code=%s and si.delivery_date>=%s and so.docstatus=0""",(item,add_days(date1,1)),as_dict=True)
	if len(data):
		return data
	else:
		return _(False)

@frappe.whitelist(allow_guest=True)
def get_order_details_week(item,date1):
	data=frappe.db.sql("""select so.name,so.customer,si.item_code,si.item_name,si.qty from `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent where si.item_code=%s and so.docstatus=0 and si.delivery_date between %s and %s""",(item,date1,add_days(date1,4)),as_dict=True)
	if len(data):
		return data
	else:
		return _(False)

@frappe.whitelist(allow_guest=True)
def get_order_details_weekday(item,date1):
	data=frappe.db.sql("""select so.name,so.customer,si.item_code,si.item_name,si.qty from `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent where si.item_code=%s and si.delivery_date=%s and so.docstatus=0""",(item,date1),as_dict=True)
	if len(data):
		return data
	else:
		return _(False)


@frappe.whitelist(allow_guest=True)
def qtyAdjust(customer,sales_order_id,item_code,qty,adjustqty,backqty,backorder_date=None):
	if backorder_date==None:
		frappe.throw("Please Select Date")
	valso=frappe.get_doc("Sales Order",sales_order_id)
	if valso.docstatus==1:
		return "1"
	data=frappe.db.sql("""select qty from `tabSales Order Item` where parent=%s and item_code=%s""",(sales_order_id,item_code))
	if len(data):
		if not int(adjustqty)==0:
			data1=frappe.db.sql("""select name from `tabSales Order Item` where parent=%s and item_code=%s""",(sales_order_id,item_code))
			if len(data1):
				doc=frappe.get_doc("Sales Order Item",data1[0][0])
				doc.qty=int(adjustqty)
				data_soi=doc.save()
				doc1=frappe.get_doc("Sales Order",doc.parent)
				doc1.qty_adjust="1"
				doc1.total_boxes=flt(doc1.total_boxes)-flt(flt(qty)-flt(adjustqty))
				doc1.total_gross_weight_lbs=flt(doc1.total_gross_weight_lbs)-flt((flt(qty)-flt(adjustqty))*flt(data_soi.gross_weight_lbs))
				doc1.total_pallets=flt(doc1.total_pallets)-flt((flt(qty)-flt(adjustqty))/flt(data_soi.sale_pallets))
				doc1.total_weight_kg=flt(doc1.total_weight_kg)-flt((flt(qty)-flt(adjustqty))*flt(data_soi.weight_kgs))
				doc1.total_net_weight=flt(doc1.total_net_weight)-flt((flt(qty)-flt(adjustqty))*flt(data_soi.weight_lbs))
				doc1.save(ignore_permissions=True)
				if int(backqty)==0:
					return _(True)
			if not int(backqty)==0:
				flag=findBackOrder(backorder_date)
			#return flag
				so_flag=frappe.db.sql("""select name from `tabSales Order` where transaction_date=%s and customer=%s""",(str(backorder_date),customer))
				if len(so_flag):
					newqty=int(qty)-int(adjustqty)
					sodata=frappe.get_doc("Sales Order",sales_order_id)
					rate=getRate(sodata.selling_price_list,item_code)
					itemdoc_id=frappe.db.sql("""select name from `tabSales Order Item` where parent=%s and item_code=%s""",(sales_order_id,item_code))
					save_sales_order_item(so_flag[0][0],item_code,backqty,rate,itemdoc_id[0][0],backorder_date)
					sodata1=frappe.get_doc("Sales Order",sales_order_id)
					sodata1.total_boxes=flt(sodata1.total_boxes)+flt(backqty)
					sodata1.total_gross_weight_lbs=flt(sodata1.total_gross_weight_lbs)+(flt(backqty)*flt(data_soi.gross_weight_lbs))
					sodata1.total_pallets=flt(sodata1.total_pallets)+(flt(backqty)/flt(data_soi.sale_pallets))
					sodata1.total_weight_kg=flt(sodata1.total_weight_kg)+(flt(backqty)*flt(data_soi.weight_kgs))
					sodata1.total_net_weight=flt(sodata1.total_net_weight)+(flt(backqty)*flt(data_soi.weight_lbs))
					sodata1.save()

				else:
					save_sales_order(sales_order_id,item_code,backqty,backorder_date)
				if flag=="True":
					data2=frappe.db.sql("""select name from `tabBack Order` where transaction_date=%s""",str(backorder_date))
					#return data2[0][0]
					if len(data2):
						d=frappe.get_doc({
											"docstatus": 0,
											"doctype": "Back Order Item",
											"name": "New Back Order Item 1",
											"owner": "Administrator",
											"parent": str(data2[0][0]),
											"parentfield": "items",
											"parenttype": "Back Order",
											"customer": str(customer),
											"item_code": str(item_code),
											"item_name": getName(item_code),
											"order_qty": data[0][0],
											"back_qty":backqty
										})
						d1=d.insert(ignore_permissions=True)
						if d1:
							return _(True)
						else:
							return _(False)

				if flag=="False":
					d=frappe.get_doc({
										"docstatus": 0,
										"doctype": "Back Order",
										"name": "New Back Order 1",
										"owner": "Administrator",
										"posting_date":str(backorder_date),
										"items": [{
											"docstatus": 0,
											"doctype": "Back Order Item",
											"name": "New Back Order Item 1",
											"owner": "Administrator",
											"parent": "New Back Order 1",
											"parentfield": "items",
											"parenttype": "Back Order",
											"idx": 1,
											"customer": str(customer),
											"item_code": str(item_code),
											"item_name": getName(item_code),
											"order_qty": data[0][0],
											"back_qty": backqty
										}]
									})
					d1=d.insert(ignore_permissions=True)
					if d1:
						return _(True)
					else:
						return _(False)


@frappe.whitelist(allow_guest=True)
def findBackOrder(backorder_date):
	data=frappe.db.sql("""select name from `tabBack Order` where transaction_date=%s""",str(backorder_date))
	if data:
		return _(True)
	else:
		return _(False)


@frappe.whitelist(allow_guest=True)
def getName(item):
	data=frappe.db.sql("""select item_name from `tabItem` where item_code=%s""",item)
	if len(data):
		return data[0][0]
	else:
		return str()

@frappe.whitelist()
def getRate(price_list,item_code):
	rate=frappe.db.sql("""select price_list_rate from `tabItem Price` where price_list=%s and item_code=%s""",(price_list,item_code))
	if rate:
		return rate[0][0]
	else:
		return 0


@frappe.whitelist(allow_guest=True)
def save_sales_order(sales_order_id,item_code,qty,backorder_date):
	d=frappe.get_doc("Sales Order",sales_order_id)
	rate=getRate(d.selling_price_list,item_code)
	d1=frappe.get_doc({
					"docstatus": 0,
					"doctype": "Sales Order",
					"name": "New Sales Order 1",
					"__islocal": 1,
					"__unsaved": 1,
					"order_type": "Sales",
					"company": d.company,
					"transaction_date": str(backorder_date),
					"customer_group": "Individual",
					"currency": "CAD",
					"selling_price_list":d.selling_price_list,
					"status": "Draft",
					"items": [],
					"terms": "",
					"customer": d.customer,
					"delivery_date":str(backorder_date)
				})
	d2=d1.insert(ignore_permissions=True)
	itemdoc_id=frappe.db.sql("""select name from `tabSales Order Item` where parent=%s and item_code=%s""",(sales_order_id,item_code))
	data_soi=save_sales_order_item(d2.name,item_code,qty,rate,itemdoc_id[0][0],backorder_date)
	sales_order_data=frappe.get_doc("Sales Order",d2.name)
	sales_order_data.payment_schedule=""
	sales_order_data.docstatus=0
	sales_order_data.selling_price_list=d.selling_price_list
	sales_order_data.total_boxes=flt(qty)
	sales_order_data.total_gross_weight_lbs=flt(qty)*flt(data_soi.gross_weight_lbs)
	sales_order_data.total_pallets=flt(qty)/flt(data_soi.sale_pallets)
	sales_order_data.total_weight_kg=flt(qty)*flt(data_soi.weight_kgs)
	sales_order_data.total_net_weight=flt(qty)*flt(data_soi.weight_lbs)
	final=sales_order_data.save(ignore_permissions=True)
	if final:
		return _(True)


@frappe.whitelist(allow_guest=True)
def save_sales_order_item(sid,item_id,item_qty,rate,itemdoc_id,backorder_date):
	datasalesorder_item=frappe.get_doc("Sales Order Item",itemdoc_id)
	item_doc=frappe.get_doc({
							"docstatus": 0,
							"doctype": "Sales Order Item",
							"name": "New Sales Order Item 1",
							"owner":str(frappe.session.user),
							"parent": str(sid),
							"parentfield": "items",
							"parenttype": "Sales Order",
							"idx": 1,
							"qty": str(item_qty),
							"item_code": str(item_id),
							"item_name":getName(item_id),
							"update_stock": 0,
							"rate":rate,
							"delivery_date":str(backorder_date),
							"weight_kgs":datasalesorder_item.weight_kgs,
							"gross_weight_lbs":datasalesorder_item.gross_weight_lbs,
							"sale_pallets":datasalesorder_item.sale_pallets
						})
	return item_doc.insert()


@frappe.whitelist()
def getName(item):
	data=frappe.db.sql("""select item_name from `tabItem` where item_code=%s""",item)
	if len(data):
		return data[0][0]
	else:
		return str()

@frappe.whitelist()
def changePriceList(cf,method):
	if cf.doc_type=="Item":
		frappe.msgprint("Item")
	else:
		frappe.msgprint("usjh")


@frappe.whitelist()
def makeDelivery(si,method):
	doc=make_delivery_note(si.name)
	doc.insert()
	

			
