# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint, get_gravatar, format_datetime, now_datetime,add_days,today,formatdate,date_diff,getdate,get_last_day
from frappe import throw, msgprint, _
from frappe.utils.password import update_password as _update_password
from frappe.desk.notifications import clear_notifications
from frappe.utils.user import get_system_managers
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
from frappe.utils import flt




def execute(filters=None):
	if not filters: filters = {}

	columns1 = get_columns(filters)
	data = get_data(filters)

	return columns1, data

def get_columns(filters):
	columns= [
		_("Item") + ":Link/Item:60", _("Item Name") + ":Data:120", _("AVQTY") + ":Data:60", _("ISQ") + ":Data:60", _("IPQ") + ":Data:60", _("WSQ") + ":Data:60", _("PSQ") + ":Data:60"
	]
	f_date=filters.get("date")
	dayname=getdate(f_date).strftime("%A")
	


	if dayname=='Monday':
		columns+=[_("MO") + ":Int:10"]
		columns+=[_("TU") + ":Int:10"]
		columns+=[_("WD") + ":Int:10"]
		columns+=[_("TH") + ":Int:10"]
		columns+=[_("FR") + ":Int:10"]

	if dayname=='Tuesday':
		columns+=[_("TU") + ":Int:10"]
		columns+=[_("WD") + ":Int:10"]
		columns+=[_("TH") + ":Int:10"]
		columns+=[_("FR") + ":Int:10"]
		columns+=[_("ST") + ":Int:10"]
		

	if dayname=='Wednesday':
		columns+=[_("WD") + ":Int:10"]
		columns+=[_("TH") + ":Int:10"]
		columns+=[_("FR") + ":Int:10"]
		columns+=[_("ST") + ":Int:10"]
		columns+=[_("SU") + ":Int:10"]
		

	if dayname=='Thursday':
		columns+=[_("TH") + ":Int:10"]
		columns+=[_("FR") + ":Int:10"]
		columns+=[_("ST") + ":Int:10"]
		columns+=[_("SU") + ":Int:10"]
		columns+=[_("MN") + ":Int:10"]


	if dayname=='Friday':
		columns+=[_("FR") + ":Int:10"]
		columns+=[_("ST") + ":Int:10"]
		columns+=[_("SU") + ":Int:10"]
		columns+=[_("MN") + ":Int:10"]
		columns+=[_("TU") + ":Int:10"]


	if dayname=='Saturday':
		columns+=[_("ST") + ":Int:10"]
		columns+=[_("SU") + ":Int:10"]
		columns+=[_("MN") + ":Int:10"]
		columns+=[_("TU") + ":Int:10"]
		columns+=[_("WD") + ":Int:10"]
		

	if dayname=='Sunday':
		columns+=[_("SU") + ":Int:10"]
		columns+=[_("MN") + ":Int:10"]
		columns+=[_("TU") + ":Int:10"]
		columns+=[_("WD") + ":Int:10"]
		columns+=[_("TH") + ":Int:10"]


	columns+=[_("")+":Data:10"]

	if dayname=='Monday':
		columns+=[_("mo") + ":Int:10"]
		columns+=[_("tu") + ":Int:10"]
		columns+=[_("wd") + ":Int:10"]
		columns+=[_("th") + ":Int:10"]
		columns+=[_("fr") + ":Int:10"]
		

	if dayname=='Tuesday':
		columns+=[_("tu") + ":Int:10"]
		columns+=[_("wd") + ":Int:10"]
		columns+=[_("th") + ":Int:10"]
		columns+=[_("fr") + ":Int:10"]
		columns+=[_("st") + ":Int:10"]
		

	if dayname=='Wednesday':
		columns+=[_("wd") + ":Int:10"]
		columns+=[_("th") + ":Int:10"]
		columns+=[_("fr") + ":Int:10"]
		columns+=[_("st") + ":Int:10"]
		columns+=[_("su") + ":Int:10"]
		

	if dayname=='Thursday':
		columns+=[_("th") + ":Int:10"]
		columns+=[_("fr") + ":Int:10"]
		columns+=[_("st") + ":Int:10"]
		columns+=[_("su") + ":Int:10"]
		columns+=[_("mn") + ":Int:10"]


	if dayname=='Friday':
		columns+=[_("fr") + ":Int:10"]
		columns+=[_("st") + ":Int:10"]
		columns+=[_("su") + ":Int:10"]
		columns+=[_("mn") + ":Int:10"]
		columns+=[_("tu") + ":Int:10"]


	if dayname=='Saturday':
		columns+=[_("st") + ":Int:10"]
		columns+=[_("su") + ":Int:10"]
		columns+=[_("mn") + ":Int:10"]
		columns+=[_("tu") + ":Int:10"]
		columns+=[_("wd") + ":Int:10"]


	if dayname=='Sunday':
		columns+=[_("su") + ":Int:10"]
		columns+=[_("mn") + ":Int:10"]
		columns+=[_("tu") + ":Int:10"]
		columns+=[_("wd") + ":Int:10"]
		columns+=[_("th") + ":Int:10"]
		

	
	columns+=[_(" ") + ":Data:10"]

	
	
	return columns
					

def get_data(filters):
	data_obj = []
	item_list=frappe.db.sql("""select distinct item_code,item_name from `tabItem`""")
	order_type=filters.get("order_type")
	order_type="Sales Order"
	if order_type=="Sales Order":

		for row in item_list:
			#frappe.msgprint(row[0])
			date_fil=filters.get("date")
			row1=[]
			count=0
			row1.append(row[0])
			row1.append(row[1])
			#mon=tue=wed=thur=fri=sat=sun=0
			balance_qty = frappe.db.sql("""select qty_after_transaction from `tabStock Ledger Entry`	
		where item_code=%s and is_cancelled='No' order by posting_date desc limit 1""", (row[0]))

			if not balance_qty:
				row1.append('')
			else:
				row1.append(balance_qty[0][0])

			if_qty=frappe.db.sql("""select sum(si.qty) from  `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent where not so.status='Completed' and not so.status='Cancelled' and not so.status='Closed' and not so.billing_status='Fully Billed' and si.item_code=%s and si.delivery_date>=%s""",(row[0],date_fil))
			
			if not if_qty:
				row1.append('')
			else:
				row1.append(if_qty[0][0])

			if_qty1=frappe.db.sql("""select sum(pi.box) from `tabPurchase Order` as po inner join `tabPurchase Order Item` as pi on po.name=pi.parent where not po.status='Completed' and not po.status='Closed' and not po.status='To Bill' and  pi.item_code=%s and pi.schedule_date>=%s and pi.received_qty<=0""",(row[0],date_fil))
			
			if not if_qty1:
				row1.append('')
			else:
				row1.append(if_qty1[0][0])

			
			w_qty=frappe.db.sql("""select sum(si.qty) from `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent where not so.status="Completed" and not so.status='Cancelled' and not so.status='Closed' and not so.billing_status='Fully Billed' and  si.item_code=%s and si.delivery_date between %s and %s""",(row[0],date_fil,add_days(date_fil,4)))

			if not w_qty:
				row1.append('')
			else:
				row1.append(w_qty[0][0])

			wp_qty=frappe.db.sql("""select sum(pi.box) from `tabPurchase Order` as po inner join `tabPurchase Order Item` as pi on po.name=pi.parent where not po.status='Completed' and not po.status='Closed' and not po.status='To Bill' and  pi.item_code=%s and pi.schedule_date between %s and %s and pi.received_qty<=0""",(row[0],date_fil,add_days(date_fil,4)))

			if not wp_qty:
				row1.append('')
			else:
				row1.append(wp_qty[0][0])



			
	
			first=frappe.db.sql("""select sum(si.qty) from `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent where not so.status="Completed" and not so.status='Cancelled' and not so.status='Closed'  and not so.billing_status='Fully Billed' and  si.item_code=%s and si.delivery_date=%s""",(row[0],date_fil))
			second=frappe.db.sql("""select sum(si.qty) from `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent where not so.status="Completed" and not so.status='Cancelled' and not so.status='Closed' and not so.billing_status='Fully Billed' and  si.item_code=%s and si.delivery_date=%s""",(row[0],add_days(date_fil,1)))
			third=frappe.db.sql("""select sum(si.qty) from `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent where not so.status="Completed" and not so.status='Cancelled' and not so.status='Closed' and not so.billing_status='Fully Billed' and not so.billing_status='Fully Billed' and  si.item_code=%s and si.delivery_date=%s""",(row[0],add_days(date_fil,2)))
			four=frappe.db.sql("""select sum(si.qty) from `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent where not so.status="Completed" and not so.status='Cancelled' and not so.status='Closed' and not so.billing_status='Fully Billed' and  si.item_code=%s and si.delivery_date=%s""",(row[0],add_days(date_fil,3)))
			five=frappe.db.sql("""select sum(si.qty) from `tabSales Order` as so inner join `tabSales Order Item` as si on so.name=si.parent where not so.status="Completed" and not so.status='Cancelled' and not so.status='Closed' and not so.billing_status='Fully Billed' and  si.item_code=%s and si.delivery_date=%s""",(row[0],add_days(date_fil,4)))

			if not first:
				row1.append(' ')
			else:
				row1.append(first[0][0])
		
			if not second:
				row1.append(' ')
			else:
				row1.append(second[0][0])
			
			if not third:
				row1.append(' ')
			else:
				row1.append(third[0][0])
			
			if not four:
				row1.append(' ')
			else:
				row1.append(four[0][0])
			
			if not five:
				row1.append(' ')
			else:
				row1.append(five[0][0])
			

			
			row1.append('')

			first1=frappe.db.sql("""select sum(pi.box) from `tabPurchase Order` as po inner join `tabPurchase Order Item` as pi on po.name=pi.parent where not po.status='Completed' and not po.status='Closed' and not po.status='To Bill' and  pi.item_code=%s and pi.schedule_date=%s and pi.received_qty<=0""",(row[0],date_fil))
			second1=frappe.db.sql("""select sum(pi.box) from `tabPurchase Order` as po inner join `tabPurchase Order Item` as pi on po.name=pi.parent where not po.status='Completed' and not po.status='Closed' and not po.status='To Bill' and  pi.item_code=%s and pi.schedule_date=%s and pi.received_qty<=0""",(row[0],add_days(date_fil,1)))
			third1=frappe.db.sql("""select sum(pi.box) from `tabPurchase Order` as po inner join `tabPurchase Order Item` as pi on po.name=pi.parent where not po.status='Completed' and not po.status='Closed' and not po.status='To Bill' and  pi.item_code=%s and pi.schedule_date=%s and pi.received_qty<=0""",(row[0],add_days(date_fil,2)))
			four1=frappe.db.sql("""select sum(pi.box) from `tabPurchase Order` as po inner join `tabPurchase Order Item` as pi on po.name=pi.parent where not po.status='Completed' and not po.status='Closed' and not po.status='To Bill' and  pi.item_code=%s and pi.schedule_date=%s and pi.received_qty<=0""",(row[0],add_days(date_fil,3)))
			five1=frappe.db.sql("""select sum(pi.box) from `tabPurchase Order` as po inner join `tabPurchase Order Item` as pi on po.name=pi.parent where not po.status='Completed' and not po.status='Closed' and not po.status='To Bill' and  pi.item_code=%s and pi.schedule_date=%s and pi.received_qty<=0""",(row[0],add_days(date_fil,4)))

			if not first1:
				row1.append('')
			else:
				row1.append(first1[0][0])
			
				
			if not second1:
				row1.append('')
			else:
				row1.append(second1[0][0])
			
			if not third1:
				row1.append('')
			else:
				row1.append(third1[0][0])
			
			if not four1:
				row1.append('')
			else:
				row1.append(four1[0][0])
			
			if not five1:
				row1.append('')
			else:
				row1.append(five1[0][0])

			

			
			data_obj.append(row1)
				

		return data_obj
	
		
			
			
				
			
			
			
		
		
	




















