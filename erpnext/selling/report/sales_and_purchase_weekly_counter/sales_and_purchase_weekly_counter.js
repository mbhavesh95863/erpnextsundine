// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */


frappe.query_reports["Sales And Purchase Weekly Counter"] = {
	
	"filters": [
		{
			"fieldname":"date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"blank",
			"label": __(""),
			"fieldtype": "Read Only",
			"default": ""
		},
		{
			"fieldname":"sales_order",
			"label": __(""),
			"fieldtype": "Read Only",
			"default": "Sales Order"
		},
		{
			"fieldname":"purchase_order",
			"label": __(""),
			"fieldtype": "Read Only",
			"default": "Purchase Order"
		}
	],
	onload: function(report) {
		
		$('input[data-fieldname="date"]').css("width","100px");
		$('div[data-fieldname="blank"]').css("width","300px");

	}

}
