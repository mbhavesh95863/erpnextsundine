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
        _("Item") + ":Link/Item:50", _("Item Name") + ":Data:60", _("AVQTY") + ":Data:50", _("ISQ") + ":Data:50", _("IPQ") + ":Data:50", _("WSQ") + ":Data:40", _("PSQ") + ":Data:40"
    ]
    f_date=filters.get("date")
    dayname=getdate(f_date).strftime("%A")
    


    if dayname=='Monday':
        columns+=[_("TU") + ":Int:10"]
        columns+=[_("WD") + ":Int:10"]
        columns+=[_("TH") + ":Int:10"]
        columns+=[_("FR") + ":Int:10"]
        columns+=[_("ST") + ":Int:10"]

    if dayname=='Tuesday':
        columns+=[_("WD") + ":Int:10"]
        columns+=[_("TH") + ":Int:10"]
        columns+=[_("FR") + ":Int:10"]
        columns+=[_("ST") + ":Int:10"]
        columns+=[_("SU") + ":Int:10"]

    if dayname=='Wednesday':
        columns+=[_("TH") + ":Int:10"]
        columns+=[_("FR") + ":Int:10"]
        columns+=[_("ST") + ":Int:10"]
        columns+=[_("SU") + ":Int:10"]
        columns+=[_("MN") + ":Int:10"]

    if dayname=='Thursday':
        columns+=[_("FR") + ":Int:10"]
        columns+=[_("ST") + ":Int:10"]
        columns+=[_("SU") + ":Int:10"]
        columns+=[_("MN") + ":Int:10"]
        columns+=[_("TU") + ":Int:10"]

    if dayname=='Friday':
        columns+=[_("ST") + ":Int:10"]
        columns+=[_("SU") + ":Int:10"]
        columns+=[_("MN") + ":Int:10"]
        columns+=[_("TU") + ":Int:10"]
        columns+=[_("WD") + ":Int:10"]

    if dayname=='Saturday':
        columns+=[_("SU") + ":Int:10"]
        columns+=[_("MN") + ":Int:10"]
        columns+=[_("TU") + ":Int:10"]
        columns+=[_("WD") + ":Int:10"]
        columns+=[_("TH") + ":Int:10"]

    if dayname=='Sunday':
        columns+=[_("MN") + ":Int:10"]
        columns+=[_("TU") + ":Int:10"]
        columns+=[_("WD") + ":Int:10"]
        columns+=[_("TH") + ":Int:10"]
        columns+=[_("FR") + ":Int:10"]

    columns+=[_("")+":Data:10"]

    if dayname=='Monday':
        columns+=[_("tu") + ":Int:10"]
        columns+=[_("wd") + ":Int:10"]
        columns+=[_("th") + ":Int:10"]
        columns+=[_("fr") + ":Int:10"]
        columns+=[_("st") + ":Int:10"]

    if dayname=='Tuesday':
        columns+=[_("wd") + ":Int:10"]
        columns+=[_("th") + ":Int:10"]
        columns+=[_("fr") + ":Int:10"]
        columns+=[_("st") + ":Int:10"]
        columns+=[_("su") + ":Int:10"]

    if dayname=='Wednesday':
        columns+=[_("th") + ":Int:10"]
        columns+=[_("fr") + ":Int:10"]
        columns+=[_("st") + ":Int:10"]
        columns+=[_("su") + ":Int:10"]
        columns+=[_("mn") + ":Int:10"]

    if dayname=='Thursday':
        columns+=[_("fr") + ":Int:10"]
        columns+=[_("st") + ":Int:10"]
        columns+=[_("su") + ":Int:10"]
        columns+=[_("mn") + ":Int:10"]
        columns+=[_("tu") + ":Int:10"]

    if dayname=='Friday':
        columns+=[_("st") + ":Int:10"]
        columns+=[_("su") + ":Int:10"]
        columns+=[_("mn") + ":Int:10"]
        columns+=[_("tu") + ":Int:10"]
        columns+=[_("wd") + ":Int:10"]

    if dayname=='Saturday':
        columns+=[_("su") + ":Int:10"]
        columns+=[_("mn") + ":Int:10"]
        columns+=[_("tu") + ":Int:10"]
        columns+=[_("wd") + ":Int:10"]
        columns+=[_("th") + ":Int:10"]

    if dayname=='Sunday':
        columns+=[_("mn") + ":Int:10"]
        columns+=[_("tu") + ":Int:10"]
        columns+=[_("wd") + ":Int:10"]
        columns+=[_("th") + ":Int:10"]
        columns+=[_("fr") + ":Int:10"]

    columns+=[_(" ") + ":Data:10", _("L1") + ":Int:10", _("L2")+ ":Int:10",
        _("L3") + ":Int:10", _("L4") + ":Int:10",
        _("L5") + ":Int:10", _("L6") + ":Int:10", _("L7") + ":Int:10", _("L8") + ":Int:10", _("L9")+ ":Int:10",
        _("L10") + ":Int:10", _("L11") + ":Int:10",
        _("L12") + ":Int:10", _("L13") + ":Int:10", _("L14") + ":Int:10", _("L15")+ ":Int:10",
        _("L16") + ":Int:10", _("L17") + ":Int:10",
        _("L18") + ":Int:10", _("L19") + ":Int:10", _("L20") + ":Int:10"]
        
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
            balance_qty = frappe.db.sql("""select sum(qty_after_transaction) from `tabStock Ledger Entry`
        where item_code=%s and is_cancelled='No' limit 1""", (row[0]))

            if not balance_qty:
                row1.append('')
            else:
                row1.append(balance_qty[0][0])

            if_qty=frappe.db.sql("""select sum(qty) from `tabSales Order Item` where item_code=%s and delivery_date>=%s""",(row[0],date_fil))
            
            if not if_qty:
                row1.append('')
            else:
                row1.append(if_qty[0][0])

            if_qty1=frappe.db.sql("""select sum(qty) from `tabPurchase Order Item` where item_code=%s and schedule_date>=%s""",(row[0],date_fil))
            
            if not if_qty1:
                row1.append('')
            else:
                row1.append(if_qty1[0][0])

            
            w_qty=frappe.db.sql("""select sum(qty) from `tabSales Order Item` where item_code=%s and delivery_date between %s and %s""",(row[0],(date_fil),add_days(date_fil,5)))

            if not w_qty:
                row1.append('')
            else:
                row1.append(w_qty[0][0])

            wp_qty=frappe.db.sql("""select sum(qty) from `tabPurchase Order Item` where item_code=%s and schedule_date between %s and %s""",(row[0],(date_fil),add_days(date_fil,5)))

            if not wp_qty:
                row1.append('')
            else:
                row1.append(wp_qty[0][0])



            
    
            first=frappe.db.sql("""select sum(qty) from `tabSales Order Item` where item_code=%s and delivery_date=%s""",(row[0],date_fil))
            second=frappe.db.sql("""select sum(qty) from `tabSales Order Item` where item_code=%s and delivery_date=%s""",(row[0],add_days(date_fil,1)))
            third=frappe.db.sql("""select sum(qty) from `tabSales Order Item` where item_code=%s and delivery_date=%s""",(row[0],add_days(date_fil,2)))
            four=frappe.db.sql("""select sum(qty) from `tabSales Order Item` where item_code=%s and delivery_date=%s""",(row[0],add_days(date_fil,3)))
            five=frappe.db.sql("""select sum(qty) from `tabSales Order Item` where item_code=%s and delivery_date=%s""",(row[0],add_days(date_fil,4)))

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

            first1=frappe.db.sql("""select sum(qty) from `tabPurchase Order Item` where item_code=%s and schedule_date=%s""",(row[0],date_fil))
            second1=frappe.db.sql("""select sum(qty) from `tabPurchase Order Item` where item_code=%s and schedule_date=%s""",(row[0],add_days(date_fil,1)))
            third1=frappe.db.sql("""select sum(qty) from `tabPurchase Order Item` where item_code=%s and schedule_date=%s""",(row[0],add_days(date_fil,2)))
            four1=frappe.db.sql("""select sum(qty) from `tabPurchase Order Item` where item_code=%s and schedule_date=%s""",(row[0],add_days(date_fil,3)))
            five1=frappe.db.sql("""select sum(qty) from `tabPurchase Order Item` where item_code=%s and schedule_date=%s""",(row[0],add_days(date_fil,4)))

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

            
            row1.append('')

            lv1=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L1'""",str(row[0]))
            lv2=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L2'""",str(row[0]))
            lv3=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L3'""",str(row[0]))
            lv4=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L4'""",str(row[0]))
            lv5=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L5'""",str(row[0]))
            lv6=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L6'""",str(row[0]))
            lv7=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L7'""",str(row[0]))
            lv8=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L8'""",str(row[0]))
            lv9=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L9'""",str(row[0]))
            lv10=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L10'""",str(row[0]))
            lv11=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L11'""",str(row[0]))
            lv12=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L12'""",str(row[0]))
            lv13=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L13'""",str(row[0]))
            lv14=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L14'""",str(row[0]))
            lv15=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L15'""",str(row[0]))
            lv16=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L16'""",str(row[0]))
            lv17=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L17'""",str(row[0]))
            lv18=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L18'""",str(row[0]))
            lv19=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L19'""",str(row[0]))
            lv20=frappe.db.sql("""select ifnull(price_list_rate,0) from `tabItem Price` where item_code=%s and price_list='L20'""",str(row[0]))
            
            if not lv1:
                row1.append(0)
            else:
                row1.append(lv1[0][0])

            if not lv2:
                row1.append(0)
            else:
                row1.append(lv2[0][0])
            if not lv3:
                row1.append(0)
            else:
                row1.append(lv3[0][0])

            if not lv4:
                row1.append(0)
            else:
                row1.append(lv4[0][0])

            if not lv5:
                row1.append(0)
            else:
                row1.append(lv5[0][0])

            if not lv6:
                row1.append(0)
            else:
                row1.append(lv6[0][0])

            if not lv7:
                row1.append(0)
            else:
                row1.append(lv7[0][0])

            if not lv8:
                row1.append(0)
            else:
                row1.append(lv8[0][0])
            if not lv9:
                row1.append(0)
            else:
                row1.append(lv9[0][0])

            if not lv10:
                row1.append(0)
            else:
                row1.append(lv10[0][0])

            if not lv11:
                row1.append(0)
            else:
                row1.append(lv11[0][0])
            if not lv12:
                row1.append(0)
            else:
                row1.append(lv12[0][0])

            if not lv13:
                row1.append(0)
            else:
                row1.append(lv13[0][0])

            if not lv14:
                row1.append(0)
            else:
                row1.append(lv14[0][0])

            if not lv15:
                row1.append(0)
            else:
                row1.append(lv15[0][0])

            if not lv16:
                row1.append(0)
            else:
                row1.append(lv16[0][0])

            if not lv17:
                row1.append(0)
            else:
                row1.append(lv17[0][0])

            if not lv18:
                row1.append(0)
            else:
                row1.append(lv18[0][0])

            if not lv19:
                row1.append(0)
            else:
                row1.append(lv19[0][0])

            if not lv20:
                row1.append(0)
            else:
                row1.append(lv20[0][0])

            

            
            data_obj.append(row1)
                

        return data_obj
    
    