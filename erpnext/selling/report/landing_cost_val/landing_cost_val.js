// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */


frappe.query_reports["Landing Cost Val"] = {
	
	"filters": [
		{
			"fieldname":"date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"sales_order",
			"label": __("Sales Order"),
			"fieldtype": "Read Only",
			"default": "Sale Price"
		}
		//,
		//{
		//	"fieldname":"purchase_order",
		//	"label": __("purchase Order"),
		//	"fieldtype": "Read Only",
		//	"default": "Latest Landing Cost"
		//}

	],
	onload: function(report) {
		
		$('input[data-fieldname="date"]').css("width","100px");
		$('input[data-fieldname="sales_order"]').css("margin-left","275px");
	//$('input[data-fieldname="purchase_order"]').css("margin-left","190px");
	}

}
