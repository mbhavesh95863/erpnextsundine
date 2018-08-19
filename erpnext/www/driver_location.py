#copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, cint, nowdate, today
from datetime import datetime
from frappe.model.naming import make_autoname
from frappe import throw, _, scrub
import frappe.permissions
from frappe.model.document import Document
import json
import collections
# import urllib
# import urllib2

import frappe.website.render

no_cache = 1
no_sitemap = 1

@frappe.whitelist(allow_guest=True)
def getUserLocation(date1=None):        
	if not date1 or date1==None:
		data=frappe.db.sql("""select u.name,u.user,u.date from `tabUser Location Log` u inner join (select name,user,max(date) as d from `tabUser Location Log` group by user) as v on u.user = v.user and u.date = v.d ORDER BY u.date DESC""")
	else:
		data=frappe.db.sql("""select name from `tabUser Location Log` WHERE date=%s GROUP BY user ORDER BY date DESC""",str(date1))    

	if data:
                objects_list = []
                for row in data:
                        data1=frappe.db.sql("""select max(ul.time) as 'time',ul.latitude,ul.longitude,ull.user,ull.date from `tabUser Location` as ul inner join `tabUser Location Log` as ull on ul.parent=ull.name where ul.parent=%s""",row[0],as_dict=True)
                        if data1:
                                objects_list.append(data1[0])
                return objects_list
        else:
                return _(False)

@frappe.whitelist(allow_guest=True)
def getUserLocation1(date1=None,user=None):        
	if not date1 or date1==None:
			date1=today()
	data=frappe.db.sql("""select name from `tabUser Location Log` WHERE date=%s and user=%s GROUP BY user ORDER BY date DESC""",(str(date1),str(user)))    

	if data:
                objects_list = []
                for row in data:
                        data1=frappe.db.sql("""select ul.time as 'time',ul.latitude,ul.longitude,ull.user,ull.date from `tabUser Location` as ul inner join `tabUser Location Log` as ull on ul.parent=ull.name where ul.parent=%s""",row[0],as_dict=True)
                        if data1:
                             for row1 in data1:
								objects_list.append(row1)
                return objects_list
        else:
                return _(False)