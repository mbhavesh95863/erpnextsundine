#copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, nowdate, cint
from frappe.model.naming import make_autoname
from frappe import throw, _, scrub
import frappe.permissions
from frappe.model.document import Document
import json
import collections
import frappe.website.render

no_cache = 1
no_sitemap = 1

@frappe.whitelist()
def get_sales_order(city_name=None, delivery_date=None, limit=50, status="To Deliver and Bill", vehicle_number=None ):
        query  = """SELECT so.*,ad.city,ad.state,ad.country,ad.address_title,ad.address_line1,ad.latitude,ad.longitude,ad.near_by_location,ad.phone  FROM `tabSales Order` so LEFT JOIN `tabAddress` ad ON  so.shipping_address_name = ad.name LEFT JOIN `tabCustomer` cu ON cu.name = so.customer WHERE so.customer != ''  """

         # search term condition
        if city_name:
                query += """ AND ad.city LIKE  %(city_name)s  """
                city_name = "%" + cstr(city_name) + "%"

        if status:
                 query += """ AND so.status LIKE  %(status)s  """
                 status  = "%" + cstr(status) + "%"

        if delivery_date:
                query += """ AND so.delivery_date LIKE %(delivery_date)s  """
                delivery_date = "%" + cstr(delivery_date) + "%"

        if vehicle_number:
                query += """ AND so.vehicle_number LIKE %(vehicle_number)s  """
                vehicle_number = "%" + cstr(vehicle_number) + "%"


        query += """ LIMIT %s  """ % (cint(limit))

        data = frappe.db.sql(query, { "city_name": city_name, "delivery_date": delivery_date,  "limit": limit, "status": status, "vehicle_number": vehicle_number }, as_dict=1)

        return data


@frappe.whitelist()
def get_item_details(item_code):
        items = frappe.get_doc("Item", item_code)

        return items;r
