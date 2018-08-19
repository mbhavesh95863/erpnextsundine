from __future__ import unicode_literals
import frappe

from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.utils import getdate,flt,validate_email_add, today, add_years,add_days,format_datetime
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
from datetime import datetime
from frappe.model.naming import make_autoname
from frappe import throw, _, scrub
import frappe.permissions
from frappe.model.document import Document
import json
import collections
# import urllib
# import urllib2

@frappe.whitelist()
def test():
	return "test"

@frappe.whitelist()
def makeBackOrder(so,method):
	frappe.msgprint("Test")
	for row in so.items:
		if row.projected_qty<0:
			available=row.qty
		else:
			available=row.qty-row.projected_qty

		if row.projected_qty<row.qty:
			data=frappe.get_doc({
					"docstatus": 0,
					"doctype": "Back Order",
					"name": "New Back Order 1",
					"__islocal": 1,
					"__unsaved": 1,
					"naming_series": "SO-",
					"transaction_date": so.transaction_date,
					"items": [{
					"docstatus": 0,
					"doctype": "Back Order Item",
					"name": "New Back Order Item 1",
					"__islocal": 1,
					"__unsaved": 1,
					"owner":str(frappe.session.user),
					"parent": "New Back Order 1",
					"parentfield": "items",
					"parenttype": "Back Order",
					"customer": so.customer,
					"item_code": row.item_code,
					"order_qty": row.qty,
					"available_qty": row.projected_qty,
					"back_qty": available,
					"sales_order_number":so.name
					}]
				})
			doc=data.insert()

	so=frappe.get_doc("Sales Order",str(so.name))
	# si = make_sales_invoice(so.name)
	# for item in so.items:
	# 		if not item.projected_qty<0:
	# 			if item.qty>item.projected_qty:
	# 				item.qty=item.projected_qty
	# 			else:
	# 				item.qty=item.qty
	# 		else:
	# 				frappe.delete_doc("Sales Invoice Item",item.name)

	# si.save()
	dt = getdate(add_days(today(),1))
	po_date=str(dt.month)+"-"+str(dt.day)+"-"+str(dt.year)
	data=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Sales Invoice",
						"name": "New Sales Invoice 1",
						"__islocal": 1,
						"__unsaved": 1,
						"owner": str(frappe.session.user),
						"naming_series": "SINV-",
						"posting_date":str(po_date),
						"items": [],
						"customer_name": so.customer_name,
						"customer": so.customer,
						"address_display": so.address_display,
						"due_date": add_days(today(),1),
						"taxes_and_charges": so.taxes_and_charges,
						"customer_address": so.customer_address,
					})
	sinv_doc=data.insert()
	# if sinv_doc:
	for item in so.items:
		if not item.projected_qty<0:
			if item.qty>item.projected_qty:
				save_invoice_item(item.item_code,sinv_doc.name,item.projected_qty,item.conversion_factor,item.rate,item.price_list_rate,item.uom,item.base_price_list_rate,so.name)
			else:
				save_invoice_item(item.item_code,sinv_doc.name,item.qty,item.conversion_factor,item.rate,item.price_list_rate,item.uom,item.base_price_list_rate,so.name)



	sales_invoice_data=frappe.get_doc("Sales Invoice",sinv_doc.name)
	final=sales_invoice_data.save()
	d1=frappe.get_doc("Sales Invoice",final.name)
	arr_len=len(final.items)
	if arr_len==0:
			frappe.delete_doc("Sales Invoice",final.name)
	else:		
		sales_invoice_data.docstatus=1
		sales_invoice_data.update_stock=1
		sales_invoice_data.taxes_and_charges=so.taxes_and_charges
		final1=sales_invoice_data.save()


@frappe.whitelist()
def save_invoice_item(item,name,qty,conversion_factor,rate,price_list_rate,uom,base_price_list_rate,sonum):
	item_doc=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Sales Invoice Item",
						"name": "New Sales Invoice Item 1",
						"__islocal": 1,
						"__unsaved": 1,
						"owner": str(frappe.session.user),
						"parent": str(name),
						"parentfield": "items",
						"parenttype": "Sales Invoice",
						"qty": qty,
						"item_code": item,
						"conversion_factor":conversion_factor,
						"rate": rate,
						"income_account": "Avantages sociaux - ASP",
						"price_list_rate":price_list_rate,
						"uom":uom,
						"base_price_list_rate":base_price_list_rate,
						"sales_order":sonum
					})
	item_save=item_doc.insert()


#Sale Order APIS	
@frappe.whitelist()
def salesOrderList():
	user_type=frappe.session.user
	if user_type=="Administrator":
		result_list2=[]
		d = collections.OrderedDict()
		d["status"]="404"
		d['message'] = "This is Administrator account"
		d['data']="Null"
		result_list2.append(d)
		return result_list2
		

	valemp=frappe.get_list("Employee",filters={"user_id":frappe.session.user},fields=["name"])
	
	if not len(valemp):
		result_list2=[]
		d = collections.OrderedDict()
		d["status"]="404"
		d['message'] = "This User Is Not Employee"
		d['data']="Null"
		result_list2.append(d)
		return result_list2

	emp=frappe.db.get("Employee",{"user_id":frappe.session.user}).name
	#vehicle=frappe.db.get("Vehicle",{"employee":emp}).name
	
	si_list=frappe.db.sql("""SELECT so.customer,so.customer_name,so.name,so.delivery_date,so.delivery_status,so.transaction_date,so.status,so.grand_total,so.address_display,so.driver,ad.city,ad.state,ad.country,ad.address_title,ad.address_line1,ad.latitude,ad.longitude,ad.near_by_location,ad.phone  FROM `tabSales Order` so LEFT JOIN `tabAddress` ad ON  so.customer_address = ad.name where so.driver=%s""",str(emp))
	if si_list:
		objects_list = []
		for row in si_list:
			d = collections.OrderedDict()
			d["name"]=row[2].encode('utf-8')
			d["customer"]=row[0].encode('utf-8')
			d["customee_name"]=row[1].encode('utf-8')
			d["delivery_date"]=row[3]
			d["delivery_status"]=row[4].encode('utf-8')
			d["transaction_date"]=row[5]
			d["status"]=row[6].encode('utf-8')
			d["grand_total"]=row[7]
			d["address_display"]=row[8]
			d["vehical"]=row[9].encode('utf-8')		
			d["city"]=row[10].encode('utf-8')
                        d["state"]=row[11].encode('utf-8')
                        d["country"]=row[12].encode('utf-8')
                        d["address_title"]=row[13].encode('utf-8')
                        d["address_line1"]=row[14].encode('utf-8')
                        d["latitude"]=row[15].encode('utf-8')
                        d["longitude"]=row[16].encode('utf-8')
                        d["near_by_location"]=row[17]
			d["phone"]=row[18]
			d["items"]=salesOrderItem(row[2])
			objects_list.append(d)

		result_list1=[]
		d = collections.OrderedDict()
		d["status"]="200"
		d['message'] = "Data Available"
		d['data']=objects_list
		result_list1.append(d)
		return result_list1	
	else:
		result_list2=[]
		d = collections.OrderedDict()
		d["status"]="404"
		d['message'] = "Data Not Available"
		d['data']="Null"
		result_list2.append(d)
		return result_list2

@frappe.whitelist()
def salesOrderItem(invoice_number):
	objects_list1=[]
	item_list1=frappe.db.sql("""select item_name,qty,base_rate,base_amount,description from `tabSales Order Item` where parent=%s""",invoice_number.encode('utf-8'))
	for row1 in item_list1:
	    d1 = collections.OrderedDict()
	    d1["item_name"]=row1[0].encode('utf-8')
	    d1["qty"]=row1[1]
	    d1["mrp"]=row1[2]
	    d1["amount"]=row1[3]
	    d1["item_description"]=row1[4].encode('utf-8')
	    objects_list1.append(d1)

	return objects_list1


@frappe.whitelist(allow_guest=True)
def save_sales_order(item_object,delivery_date):
	d1=frappe.get_doc({
					"docstatus": 0,
					"doctype": "Sales Order",
					"name": "New Sales Order 1",
					"__islocal": 1,
					"__unsaved": 1,
					"order_type": "Sales",
					"company": "Sundine Produce",
					"transaction_date": str(today()),
					"customer_group": "Individual",
					"currency": "CAD",
					"selling_price_list": getPriceList(),
					"apply_discount_on": "Net Total",
					"status": "Draft",
					"items": [],
					"terms": "",
					"customer": getCustomerName(),
					"delivery_date":str(delivery_date)
				})
	d2=d1.insert(ignore_permissions=True)

	item_data=json.loads(item_object)
	for row in item_data:
		data=frappe.db.sql("""select name from `tabItem` where name=%s and disabled=1""",row["item_code"])
		
		if len(data):
			temp=str(row["item_code"])+" item is disabled"
			result_list2=[]
			d = collections.OrderedDict()
			d["status"]="404"
			d['message'] = temp
			d['data']=None
			result_list2.append(d)
			return result_list2
		else:
			if row["uom"]=="lbs":
				item_weight=frappe.db.sql("""select weight_per_unit from `tabItem` where item_code=%s""",row["item_code"])
				if item_weight:
					qty=flt(row["qty"])/flt(item_weight[0][0])
					save_sales_order_item(d2.name,row["item_code"],qty)

			if row["uom"]=="Box":
					save_sales_order_item(d2.name,row["item_code"],row["qty"])

	# final=frappe.get_doc("Sales Order",d2.name)
	sales_order_data=frappe.get_doc("Sales Order",d2.name)

	sales_order_data.payment_schedule=""
	sales_order_data.docstatus=0
	# sales_order_data.apply_discount_on="Net Total"
	# sales_order_data.additional_discount_percentage=flt(3.554160)

	final=sales_order_data.save(ignore_permissions=True)
	if final:
		objects_list = []
		for row in final.items:
		    d = collections.OrderedDict()
		    d["item_name"]=row.item_name
		    d["qty"]=row.qty
		    d["base_amount"]=row.base_amount
		    d["base_rate"]=row.base_rate
		    objects_list.append(d)
		#return objects_list
		result_list1=[]
		d = collections.OrderedDict()
		d["customer_name"]=final.customer_name
		d["sales_order_id"] =final.name
		d["item"]=objects_list
		d["grand_total"]=final.rounded_total
		d["customer"]=final.customer
		result_list1.append(d)
		#return result_list1	
		result_list2=[]
		d = collections.OrderedDict()
		d["status"]="200"
		d['message'] = "Data Available"
		d['data']=result_list1
		result_list2.append(d)
		return result_list2
	else:
		result_list2=[]
		d = collections.OrderedDict()
		d["status"]="404"
		d['message'] = "Data Not Available"
		d['data']=None
		result_list2.append(d)
		return result_list2

@frappe.whitelist()
def save_sales_order_item(sid,item_id,item_qty):
	#rate=frappe.db.get("Item",{"name":item_id}).standard_rate

	item_doc=frappe.get_doc({
							"docstatus": 0,
							"doctype": "Sales Order Item",
							"name": "New Sales Order Item 1",
							"__islocal": 1,
							"__unsaved": 1,
							"owner": str(frappe.session.user),
							"parent": str(sid),
							"parentfield": "items",
							"parenttype": "Sales Order",
							"idx": 1,
							"qty": str(item_qty),
							"item_code": str(item_id),
							"rate":getItemRate(item_id),
							"update_stock": 0,
							"warehouse": "Sundine Kestrel- . - .",
							"delivery_date":str(today())
						})
	item_save=item_doc.insert()
		
#Sale Order APIS ENd - 
		
#Purchase Order APIS	
@frappe.whitelist()
def getSupplierName():
	c_name=frappe.db.get("Contact",{"user":frappe.session.user}).name
	if c_name:
			cust_name=frappe.db.get("Dynamic Link",{"parent":c_name}).link_name
			if cust_name:
					return suppl_name
					
@frappe.whitelist()
def getSupplierList():
	return frappe.get_all("Supplier",fields=["supplier_name","supplier_type"])
					
@frappe.whitelist()
def purchaseOrderList():
	user_type=frappe.session.user
	if user_type=="Administrator":
		result_list2=[]
		d = collections.OrderedDict()
		d["status"]="404"
		d['message'] = "This is Administrator account"
		d['data']="Null"
		result_list2.append(d)
		return result_list2
		

	valemp=frappe.get_list("Employee",filters={"user_id":frappe.session.user},fields=["name"])
	
	if not len(valemp):
		result_list2=[]
		d = collections.OrderedDict()
		d["status"]="404"
		d['message'] = "This User Is Not Employee"
		d['data']="Null"
		result_list2.append(d)
		return result_list2

	emp=frappe.db.get("Employee",{"user_id":frappe.session.user}).name
	#vehicle=frappe.db.get("Vehicle",{"employee":emp}).name
	
	si_list=frappe.db.sql("""SELECT so.customer,so.customer_name,so.name,so.delivery_date,so.delivery_status,so.transaction_date,so.status,so.grand_total,so.address_display,so.driver,ad.city,ad.state,ad.country,ad.address_title,ad.address_line1,ad.latitude,ad.longitude,ad.near_by_location,ad.phone  FROM `tabSales Order` so LEFT JOIN `tabAddress` ad ON  so.customer_address = ad.name where so.driver=%s""",str(emp))
	if si_list:
		objects_list = []
		for row in si_list:
			d = collections.OrderedDict()
			d["name"]=row[2].encode('utf-8')
			d["customer"]=row[0].encode('utf-8')
			d["customee_name"]=row[1].encode('utf-8')
			d["delivery_date"]=row[3]
			d["delivery_status"]=row[4].encode('utf-8')
			d["transaction_date"]=row[5]
			d["status"]=row[6].encode('utf-8')
			d["grand_total"]=row[7]
			d["address_display"]=row[8]
			d["vehical"]=row[9].encode('utf-8')		
			d["city"]=row[10].encode('utf-8')
                        d["state"]=row[11].encode('utf-8')
                        d["country"]=row[12].encode('utf-8')
                        d["address_title"]=row[13].encode('utf-8')
                        d["address_line1"]=row[14].encode('utf-8')
                        d["latitude"]=row[15].encode('utf-8')
                        d["longitude"]=row[16].encode('utf-8')
                        d["near_by_location"]=row[17]
			d["phone"]=row[18]
			d["items"]=salesOrderItem(row[2])
			objects_list.append(d)

		result_list1=[]
		d = collections.OrderedDict()
		d["status"]="200"
		d['message'] = "Data Available"
		d['data']=objects_list
		result_list1.append(d)
		return result_list1	
	else:
		result_list2=[]
		d = collections.OrderedDict()
		d["status"]="404"
		d['message'] = "Data Not Available"
		d['data']="Null"
		result_list2.append(d)
		return result_list2

@frappe.whitelist()
def purchaseOrderItem(invoice_number):
	objects_list1=[]
	item_list1=frappe.db.sql("""select item_name,qty,base_rate,base_amount,description from `tabSales Order Item` where parent=%s""",invoice_number.encode('utf-8'))
	for row1 in item_list1:
	    d1 = collections.OrderedDict()
	    d1["item_name"]=row1[0].encode('utf-8')
	    d1["qty"]=row1[1]
	    d1["mrp"]=row1[2]
	    d1["amount"]=row1[3]
	    d1["item_description"]=row1[4].encode('utf-8')
	    objects_list1.append(d1)

	return objects_list1


@frappe.whitelist(allow_guest=True)
def save_purchase_order(item_object,delivery_date):
	d1=frappe.get_doc({
					"docstatus": 0,
					"doctype": "Purchase Order",
					"name": "New Purchase Order 1",
					"__islocal": 1,
					"__unsaved": 1,
					"order_type": "Purchase",
					"company": "Sundine Produce",
					"transaction_date": str(today()),
					"supplier_group": "Individual",
					"currency": "CAD",
					"buying_price_list": getPriceList(),
					"apply_discount_on": "Net Total",
					"status": "Draft",
					"items": [],
					"terms": "",
					"supplier": getSupplierName(),
					"delivery_date":str(delivery_date)
				})
	d2=d1.insert(ignore_permissions=True)

	item_data=json.loads(item_object)
	for row in item_data:
		data=frappe.db.sql("""select name from `tabItem` where name=%s and disabled=1""",row["item_code"])
		
		if len(data):
			temp=str(row["item_code"])+" item is disabled"
			result_list2=[]
			d = collections.OrderedDict()
			d["status"]="404"
			d['message'] = temp
			d['data']=None
			result_list2.append(d)
			return result_list2
		else:
			if row["uom"]=="lbs":
				item_weight=frappe.db.sql("""select weight_per_unit from `tabItem` where item_code=%s""",row["item_code"])
				if item_weight:
					qty=flt(row["qty"])/flt(item_weight[0][0])
					save_sales_order_item(d2.name,row["item_code"],qty)

			if row["uom"]=="Box":
					save_sales_order_item(d2.name,row["item_code"],row["qty"])

	# final=frappe.get_doc("Sales Order",d2.name)
	sales_order_data=frappe.get_doc("Sales Order",d2.name)

	sales_order_data.payment_schedule=""
	sales_order_data.docstatus=0
	# sales_order_data.apply_discount_on="Net Total"
	# sales_order_data.additional_discount_percentage=flt(3.554160)

	final=sales_order_data.save(ignore_permissions=True)
	if final:
		objects_list = []
		for row in final.items:
		    d = collections.OrderedDict()
		    d["item_name"]=row.item_name
		    d["qty"]=row.qty
		    d["base_amount"]=row.base_amount
		    d["base_rate"]=row.base_rate
		    objects_list.append(d)
		#return objects_list
		result_list1=[]
		d = collections.OrderedDict()
		d["customer_name"]=final.customer_name
		d["sales_order_id"] =final.name
		d["item"]=objects_list
		d["grand_total"]=final.rounded_total
		d["customer"]=final.customer
		result_list1.append(d)
		#return result_list1	
		result_list2=[]
		d = collections.OrderedDict()
		d["status"]="200"
		d['message'] = "Data Available"
		d['data']=result_list1
		result_list2.append(d)
		return result_list2
	else:
		result_list2=[]
		d = collections.OrderedDict()
		d["status"]="404"
		d['message'] = "Data Not Available"
		d['data']=None
		result_list2.append(d)
		return result_list2

@frappe.whitelist()
def save_purchase_order_item(sid,item_id,item_qty):
	#rate=frappe.db.get("Item",{"name":item_id}).standard_rate

	item_doc=frappe.get_doc({
							"docstatus": 0,
							"doctype": "Purchase Order Item",
							"name": "New Purchase Order Item 1",
							"__islocal": 1,
							"__unsaved": 1,
							"owner": str(frappe.session.user),
							"parent": str(sid),
							"parentfield": "items",
							"parenttype": "Sales Order",
							"idx": 1,
							"qty": str(item_qty),
							"item_code": str(item_id),
							"rate":getItemRate(item_id),
							"update_stock": 0,
							"warehouse": "Sundine Kestrel- . - .",
							"delivery_date":str(today())
						})
	item_save=item_doc.insert()
	
@frappe.whitelist()
def purchaseOrderHistory():
	contact=frappe.db.sql("""select name from `tabContact` where user=%s""",frappe.session.user)
	customer_name = ""
	if len(contact):
		cust_name=frappe.db.sql("""select link_name from `tabDynamic Link` where link_doctype='Customer' and parent=%s""",contact[0][0])
		if len(cust_name):
			customer_name=cust_name[0][0]
	si_list=frappe.db.sql("""select customer,customer_name,transaction_date,grand_total,name from `tabSales Order` where customer=%s or owner=%s""",(customer_name,frappe.session.user))
	if si_list:
		objects_list = []
		for row in si_list:
			d = collections.OrderedDict()
			d["customer"]=str(row[0])
			d["customer_name"]=str(row[1])
			d["transaction_date"]=str(row[2])
			d["grand_total"]=row[3]
			d["order_number"]=str(row[4])
			d["items"]=salesinvoice_item(row[4])
			objects_list.append(d)

		result_list1=[]
		d = collections.OrderedDict()
		d["status"]="200"
		d['message'] = "Data Available"
		d['data']=objects_list
		result_list1.append(d)
		return result_list1	
	else:
		result_list2=[]
		d = collections.OrderedDict()
		d["status"]="404"
		d['message'] = "Data Not Available"
		d['data']="Null"
		result_list2.append(d)
		return result_list2

#purchase Order APIS ENd - 
		
@frappe.whitelist()
def userProfile():
	user_detail=frappe.db.sql("""select full_name,email,mobile_no,vehical from `tabUser` where name=%s""",frappe.session.user)
	if user_detail:
		objects_list = []
		d = collections.OrderedDict()
		d["full_name"]=user_detail[0][0]
		d["email"]=user_detail[0][1]
		d["mobile_no"]=user_detail[0][2]
		d["area"]=user_detail[0][3]
		objects_list.append(d)

		result_list1=[]
		d = collections.OrderedDict()
		d["status"]="200"
		d['message'] = "Data Available"
		d['data']=objects_list
		result_list1.append(d)
		return result_list1	
	else:
		result_list2=[]
		d = collections.OrderedDict()
		d["status"]="404"
		d['message'] = "Data Not Available"
		result_list2.append(d)
		return result_list2


@frappe.whitelist()
def insertUserLog(lat,lang):
	check=frappe.db.sql("""select name from `tabUser Location Log` where date=%s and user=%s""",(today(),frappe.session.user))
	if check:

		d = frappe.get_doc({
			"name": "User Location 1",
			"parent": str(check[0][0]),
			"latitude": str(lat),
			"longitude": str(lang),
			"doctype": "User Location",
			"parenttype": "User Location Log",
			"time": str(frappe.utils.data.nowtime()),
			"owner": str(frappe.session.user),
			"docstatus": 0,
			"parentfield": "user_location"
		})
		d.insert(ignore_permissions=True)
		doc1=frappe.get_doc("User Location Log",check[0][0])
		return doc1.save(ignore_permissions=True)
		
			
	else:

		doc=frappe.get_doc({
						"name": str(frappe.session.user) +" "+str(today()),
						"title":str(frappe.session.user) +" "+str(today()),
						"user_location": [{
							"name": "User Location 1",
							"parent": str(frappe.session.user) +" "+str(today()),
							"latitude": str(lat),
							"longitude": str(lang),
							"doctype": "User Location",
							"parenttype": "User Location Log",
							"time": str(frappe.utils.data.nowtime()),
							"owner": str(frappe.session.user),
							"docstatus": 0,
							"parentfield": "user_location"
						}],
						"doctype": "User Location Log",
						"user": str(frappe.session.user),
						"date": str(today()),
						"owner": str(frappe.session.user)
					})
		return doc.insert(ignore_permissions=True)

@frappe.whitelist()
def updateSalesOrderStatus(sales_order_id):
	if sales_order_id:
		data=frappe.get_doc("Sales Order",sales_order_id)
		if data:
			d=data.submit()
			return _(True)
		else:
			return _(False)
	else:
		return _(False)

@frappe.whitelist()
def getUserLocation(date1=None):
	if date1==None:
		date1=today()

	data=frappe.db.sql("""select name from `tabUser Location Log` where date=%s and user=%s""",(str(date1),frappe.session.user))
	if data:
		objects_list = []
		for row in data:
			data1=frappe.db.sql("""select max(ul.time) as 'time',ul.latitude,ul.longitude,ull.user from `tabUser Location` as ul inner join `tabUser Location Log` as ull on ul.parent=ull.name where ul.parent=%s""",row[0],as_dict=True)
			if data1:
				objects_list.append(data1[0])
		return objects_list
	else:
		return _(False)

@frappe.whitelist()
def getUserLocation1(date1=None):
        if date1==None:
                date1=today()

        data=frappe.db.sql("""select name from `tabUser Location Log` group by user order by date desc""",as_dict=True)
        if data:
                objects_list = []
                for row in data:
                        data1=frappe.db.sql("""select max(ul.time) as 'time',ul.latitude,ul.longitude,ull.user from `tabUser Location` as ul inner join `tabUser Location Log` as ull on ul.parent=ull.name where ul.parent=%s""",row[0],as_dict=True)
                        if data1:
                                objects_list.append(data1[0])
                return objects_list
        else:
                return _(False)

@frappe.whitelist()
def customerProfile():
	data=frappe.db.sql("""select email,first_name,last_name,username,gender,mobile_no from `tabUser` where name=%s""",frappe.session.user,as_dict=True)
	if not data[0]["email"]==None:
		return data[0]
	else:
		return _(False)

@frappe.whitelist(allow_guest=True)
def itemList():
	item_list=frappe.get_all("Item",filters={'has_variants':0,'show_in_website':1},fields=["item_name", "item_code", "standard_rate", "weight_per_unit", "item_group","description","website_image","show_in_website"])
	if item_list:
		return item_list
	else:	
		return _(False)


@frappe.whitelist()
def getCustomerName():
	c_name=frappe.db.get("Contact",{"user":frappe.session.user}).name
	if c_name:
			cust_name=frappe.db.get("Dynamic Link",{"parent":c_name}).link_name
			if cust_name:
					return cust_name


@frappe.whitelist()
def getPriceList():
	c_name=frappe.db.get("Contact",{"user":frappe.session.user}).name
	if c_name:
			cust_name=frappe.db.get("Dynamic Link",{"parent":c_name}).link_name
			if cust_name:
					price_list_name=frappe.db.get("Customer",{"name":cust_name}).default_price_list
					if price_list_name:
							return price_list_name

@frappe.whitelist()
def getItemRate(item_id):
	price_list=getPriceList()
	if price_list:
		data=frappe.db.sql("""select price_list_rate from `tabItem Price` where price_list=%s and item_code=%s""",(price_list,item_id))
		if len(data):
			return data[0][0]
		else:
			return "0"

@frappe.whitelist()
def salesOrderHistory():
	contact=frappe.db.sql("""select name from `tabContact` where user=%s""",frappe.session.user)
	customer_name = ""
	if len(contact):
		cust_name=frappe.db.sql("""select link_name from `tabDynamic Link` where link_doctype='Customer' and parent=%s""",contact[0][0])
		if len(cust_name):
			customer_name=cust_name[0][0]
	si_list=frappe.db.sql("""select customer,customer_name,transaction_date,grand_total,name from `tabSales Order` where customer=%s or owner=%s""",(customer_name,frappe.session.user))
	if si_list:
		objects_list = []
		for row in si_list:
			d = collections.OrderedDict()
			d["customer"]=str(row[0])
			d["customer_name"]=str(row[1])
			d["transaction_date"]=str(row[2])
			d["grand_total"]=row[3]
			d["order_number"]=str(row[4])
			d["items"]=salesinvoice_item(row[4])
			objects_list.append(d)

		result_list1=[]
		d = collections.OrderedDict()
		d["status"]="200"
		d['message'] = "Data Available"
		d['data']=objects_list
		result_list1.append(d)
		return result_list1	
	else:
		result_list2=[]
		d = collections.OrderedDict()
		d["status"]="404"
		d['message'] = "Data Not Available"
		d['data']="Null"
		result_list2.append(d)
		return result_list2

@frappe.whitelist()
def salesinvoice_item(invoice_number):
	objects_list1=[]
	item_list1=frappe.db.sql("""select item_name,qty,rate,amount,item_code,uom from `tabSales Order Item` where parent=%s""",invoice_number)
	for row1 in item_list1:
	    d1 = collections.OrderedDict()
	    d1["item_name"]=str(row1[0])
	    d1["qty"]=str(row1[1])
	    d1["rate"]=row1[2]
	    d1["amount"]=str(row1[3])
	    d1["item_code"]=str(row1[4])
	    d1["uom"]=str(row1[5])
	    objects_list1.append(d1)

	return objects_list1


@frappe.whitelist()
def getPurchasepallet(name):
	pur_pallet=frappe.db.sql("""select purchase_pallets from `tabItem` where item_code=%s""",name)
	if not pur_pallet[0][0]==None:
		return pur_pallet[0][0]
	else:
		return _(False)


@frappe.whitelist()
def getCustomerList():
	return frappe.get_all("Customer",fields=["customer_name","customer_group","customer_type"])

@frappe.whitelist()
def getDriverList():
	return frappe.get_all("Driver",filters={"status":"Active"},fields=["full_name","cell_number","employee","license_number","issuing_date","expiry_date"])


@frappe.whitelist(allow_guest=True)
def save_sales_order_for_sd(item_object,delivery_date,customer,driver):
	d1=frappe.get_doc({
					"docstatus": 0,
					"doctype": "Sales Order",
					"name": "New Sales Order 1",
					"__islocal": 1,
					"__unsaved": 1,
					"order_type": "Sales",
					"company": "Sundine Produce",
					"transaction_date": str(today()),
					"selling_price_list": getPriceList_sd(customer),
					"status": "Draft",
					"items": [],
					"terms": "",
					"customer":str(customer),
					"driver":str(driver),
					"delivery_date":str(delivery_date)
				})
	d2=d1.insert(ignore_permissions=True)

	item_data=json.loads(item_object)
	for row in item_data:
		data=frappe.db.sql("""select name from `tabItem` where name=%s and disabled=1""",row["item_code"])
		
		if len(data):
			temp=str(row["item_code"])+" item is disabled"
			result_list2=[]
			d = collections.OrderedDict()
			d["status"]="404"
			d['message'] = temp
			d['data']=None
			result_list2.append(d)
			return result_list2
		else:
			if row["uom"]=="lbs":
				item_weight=frappe.db.sql("""select weight_per_unit from `tabItem` where item_code=%s""",row["item_code"])
				if int(item_weight[0][0])==0:
					result_list2=[]
					d = collections.OrderedDict()
					d["status"]="404"
					d['message'] = str(row["item_code"])+" Item Weight Per Unit Not Available"
					d['data']=None
					result_list2.append(d)
					return result_list2
	
				else:
					qty=flt(row["qty"])/flt(item_weight[0][0])
					save_sales_order_item_for_sd(d2.name,row["item_code"],qty,row["rate"])

			if row["uom"]=="Box":
					save_sales_order_item_for_sd(d2.name,row["item_code"],row["qty"],row["rate"])

	# final=frappe.get_doc("Sales Order",d2.name)
	sales_order_data=frappe.get_doc("Sales Order",d2.name)

	sales_order_data.payment_schedule=""
	sales_order_data.docstatus=0
	# sales_order_data.apply_discount_on="Net Total"
	# sales_order_data.additional_discount_percentage=flt(3.554160)

	final=sales_order_data.save(ignore_permissions=True)
	if final:
		objects_list = []
		for row in final.items:
		    d = collections.OrderedDict()
		    d["item_name"]=row.item_name
		    d["qty"]=row.qty
		    d["base_amount"]=row.base_amount
		    d["base_rate"]=row.base_rate
		    objects_list.append(d)
		#return objects_list
		result_list1=[]
		d = collections.OrderedDict()
		d["customer_name"]=final.customer_name
		d["sales_order_id"] =final.name
		d["item"]=objects_list
		d["grand_total"]=final.rounded_total
		d["customer"]=final.customer
		result_list1.append(d)
		#return result_list1	
		result_list2=[]
		d = collections.OrderedDict()
		d["status"]="200"
		d['message'] = "Data Available"
		d['data']=result_list1
		result_list2.append(d)
		return result_list2
	else:
		result_list2=[]
		d = collections.OrderedDict()
		d["status"]="404"
		d['message'] = "Data Not Available"
		d['data']=None
		result_list2.append(d)
		return result_list2

@frappe.whitelist()
def save_sales_order_item_for_sd(sid,item_id,item_qty,rate):
	#rate=frappe.db.get("Item",{"name":item_id}).standard_rate

	item_doc=frappe.get_doc({
							"docstatus": 0,
							"doctype": "Sales Order Item",
							"name": "New Sales Order Item 1",
							"__islocal": 1,
							"__unsaved": 1,
							"owner": str(frappe.session.user),
							"parent": str(sid),
							"parentfield": "items",
							"parenttype": "Sales Order",
							"idx": 1,
							"qty": str(item_qty),
							"rate":rate,
							"item_code": str(item_id),
							"update_stock": 0,
							"delivery_date":str(today())
						})
	item_save=item_doc.insert()

@frappe.whitelist()
def getPriceList_sd(customer):
	data=frappe.db.sql("""select default_price_list from `tabCustomer` where name=%s""",customer)
	if data:
		return data[0][0]
	else:
		return "Standard Selling"

@frappe.whitelist()
def getItemRate_sd(item_id,soid):
	doc=frappe.get_doc("Sales Order",soid)
	price_list=getPriceList_sd(doc.customer)
	if price_list:
		data=frappe.db.sql("""select price_list_rate from `tabItem Price` where price_list=%s and item_code=%s""",(price_list,item_id))
		if len(data):
			return data[0][0]
		else:
			return "0"

@frappe.whitelist()
def getUserType():
	data=frappe.db.sql("""select type from `tabUser` where name=%s""",frappe.session.user)
	if data:
		return data[0][0]
	else:
		return str()






	









	
	
	

