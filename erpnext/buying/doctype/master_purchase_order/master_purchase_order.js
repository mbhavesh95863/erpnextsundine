// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Master Purchase Order', {
	refresh: function(frm) {
		
		frappe.require([
			"assets/erpnext/js/myTables.js",
			"assets/erpnext/css/myTable.css",
		]);
		
		document.querySelector('div[data-fieldname="numbers_boxes"] .clearfix').style.display = "none";
		document.querySelector('div[data-fieldname="numbers_pallets"] .clearfix').style.display = "none";
		document.querySelector('div[data-fieldname="numbers_gross"] .clearfix').style.display = "none";
		document.querySelector('div[data-fieldname="lbs_boxes"] .clearfix').style.display = "none";
		document.querySelector('div[data-fieldname="kgs_boxes"] .clearfix').style.display = "none";
		document.querySelector('div[data-fieldname="lbs_pallets"] .clearfix').style.display = "none";
		document.querySelector('div[data-fieldname="kgs_pallets"] .clearfix').style.display = "none";
		document.querySelector('div[data-fieldname="lbs_gross"] .clearfix').style.display = "none";
		document.querySelector('div[data-fieldname="kgs_gross"] .clearfix').style.display = "none";
		
		$('.indicator').css('display','none');
		$( "button[data-fieldname*='save_order']" ).removeClass( "btn-default" ).addClass( "btn-primary" );
		$( "button[data-fieldname*='save_order']" ).css('padding','8px');

		$( "button[data-fieldname*='update_order']" ).removeClass( "btn-default" ).addClass( "btn-primary" );
		$( "button[data-fieldname*='update_order']" ).css('padding','8px');
		$.ajax({
			url: '/api/resource/Master Purchase Order/' + frm.doc.name,
			type: 'get',
			dataType: "json",
			success: function( data ) {
				//console.log(data.data);
				if(data.data.master_purchase_order_item.length > 0) 
				{
					var TableArray = [];
					TableArray.push({'name':frm.doc.name});
					var ItemArray = [];
					ItemArray.push({'name':frm.doc.name});
					//console.log(data.data.master_purchase_order_item.length);
					for (var i = 0; i < data.data.master_purchase_order_item.length; i++) 
					{
						var dta = data.data.master_purchase_order_item[i];
						var gw = dta.gross_weight;
						if(isNaN(gw)) { gw = 0; }
						var itmcd = { 'item_name': dta.item_name , 'row_number': dta.row_number, 'item_code': dta.item_code, 'weight': dta.weight, 'weight_per_unit': dta.weight_per_unit,  'uom': dta.uom,  'gross_weight': gw, 'description': dta.description, 'purchase_pallets': dta.purchase_pallets, 'col_number': "0", isuppliers: [] };				
						var splcd = {'name': dta.name, 'qty': dta.qty, 'received_qty': dta.received_qty, 'price': dta.price, 'supplier_name': dta.supplier_name, 'supplier': dta.supplier , 'default_currency': dta.default_currency , 'col_number' : dta.col_number};
				
				 
						if( ItemArray.length > 1 ) 
						{
							if(typeof ItemArray[dta.row_number] != "undefined") {
					 TableArray[dta.row_number].push(splcd);
						}
						else {
ItemArray[dta.row_number] = [];							
ItemArray[dta.row_number].push(itmcd);
							itmcd.isuppliers.push(splcd);
TableArray[dta.row_number] = []; 						
TableArray[dta.row_number].push(itmcd);
						TableArray[dta.row_number].push(splcd);
							}
						}
						else {
ItemArray[dta.row_number] = [];	
						ItemArray[dta.row_number].push(itmcd);
						TableArray[dta.row_number] = []; 						
						TableArray[dta.row_number].push(itmcd);
						TableArray[dta.row_number].push(splcd);
						}
		
					}	
					
				}
//console.log(ItemArray); 
//console.log(TableArray);
				var table = '<tr data-row="0"><td data-row="0" data-col="0"></td><td data-row="0" data-col="1"> </td><td data-row="0" data-col="2"></td><td data-row="0" data-col="3"></td><td data-row="0" data-col="4"></td>'; 
				var dataCol = 5;
				var dataCol1 = dataCol;
				var t1 = '<tr data-row="1"><td data-row="1" data-col="0"></td><td data-row="1" data-col="1"> </td><td data-row="1" data-col="2"></td><td data-row="1" data-col="3"></td><td data-row="1" data-col="4"></td>'; 
				var t2 = '<tr data-row="2"><td data-row="2" data-col="0"></td><td data-row="2" data-col="1">Items</td><td data-row="2" data-col="2">Item Name</td><td data-row="2" data-col="3"><div class="text-span">Pallets </div></td><td data-row="2" data-col="4">Lbs/Box</td>';
				var titems = '';
				var dataRow = 3; var spcol = 0; var ttlcol = 1; var colStart = 5;
				var tlCols = ''; //alert(TableArray.length);
				for(var v=1; v < TableArray.length; v++) {
					
					TableArray[v].sort(function(obj1, obj2) {
						return obj1.col_number - obj2.col_number;
					});
					
			titems = titems + '<tr class="item-row" data-row="'+dataRow +'"><td data-row="'+dataRow +'" data-col="0"><a href="javascript:;" class="del" onClick="myTable_DelRow('+dataRow +')"></a></td><td data-row="'+dataRow +'" data-col="1"><div class="autocomplete"><input type="hidden" class="uom" name="uom" value="' +TableArray[v][0].uom + '"><input type="hidden" class="sitemsid" name="sitemsid" value="' +TableArray[v][0].item_code + '"><input type="hidden" class="item_code" name="item_code" value="' +TableArray[v][0].item_code + '"><input type="text" class="sitems" id="sitems'+dataRow +'" name="sitems" value="' +TableArray[v][0].item_name + '"></div></td><td data-row="'+dataRow +'" data-col="2"><input type="text" class="idesc" name="idesc" value="' +TableArray[v][0].description+ '" /></td><td data-row="'+dataRow +'" style="" data-col="3"><input type="text" class="purchase_pallets"  name="purchase_pallets" value="' +TableArray[v][0].purchase_pallets+ '"><input type="text" class="gross_weight"  name="gross_weight" value="' +TableArray[v][0].gross_weight+ '"></td><td data-row="'+dataRow +'" data-col="4"><input type="text" class="weight" name="weight" value="' +TableArray[v][0].weight_per_unit+ '"></td>';	
			
			for(var k=1; k < TableArray[v].length; k++)
			{
				if(spcol == 0 )
				{
				
				t1 = t1 + '<td data-row="1" data-col="'+ dataCol1 +'"><div class="autocomplete"><input type="hidden" class="isupplierid" name="isupplierid" value="'+ TableArray[1][k].supplier +'"><input type="hidden" class="default_currency" name="default_currency" value="'+ TableArray[1][k].default_currency +'"><input type="text" id="isupplier'+ dataCol1 +'" class="isupplier"  name="isupplier'+ dataCol1 +'" value="'+ TableArray[1][k].supplier +'"></div></td>';

table = table + '<td data-row="0" data-col="'+dataCol1 +'"><a href="javascript:;" class="delCol" onClick="myTable_DelCol('+ dataCol1 +')"></a></td>';
					
					t2 = t2 + '<td data-row="2" data-col="'+ dataCol1 +'"><div class="text-span">Qty </div><div class="text-span"> Price</div></td>';
				}
				titems = titems  + '<td data-row="'+ dataRow +'" data-col="' + dataCol1 + '"><input type="hidden" class="iname' + dataCol1 + '" id="iname" name="iname' + dataCol1 + '" value="'+ TableArray[v][k].name +'"><input type="hidden" class="rqty' + dataCol1 + '" id="rqty" name="rqty' + dataCol1 + '" value="'+ TableArray[v][k].received_qty +'"><input type="text" class="iqty' + dataCol1 + '" id="iqty" name="iqty' + dataCol1 + '" value="'+ TableArray[v][k].qty +'"><input type="text" name="iprice' + dataCol1 + '" class="iprice' + dataCol1 + '" value="'+ TableArray[v][k].price +'"  id="iprice"></td>';
						
				if(spcol == 0) {
	tlCols = tlCols + '<td data-row="'+ (TableArray.length + 2) +'" data-col="'+ dataCol1 +'"><p id="qtotal" class="qtotal'+ dataCol1 +'">0</p><p id="stotal" class="stotal'+ dataCol1 +'">0.0</p></td>';		ttlcol  = colStart + k;
				}
			dataCol1 = dataCol1 + 1;			
					//console.log(TableArray[v][k]);
				} spcol = spcol + 1;
					titems = titems  + '<td data-row="'+dataRow +'" data-col="'+dataCol1+'"><span class="itotal">0.0</span></td><td data-row="'+dataRow +'" data-col="'+ (dataCol1 + 1 )+'"><span class="avgitotal">0.0</span></td><td data-row="'+dataRow +'" data-col="'+ (dataCol1 + 2 )+'"><span class="qtytotal">0.0</span></td><td data-row="'+dataRow +'" data-col="'+ (dataCol1 + 3 )+'"><span class="pltitotal">0.0</span></td><td data-row="'+dataRow +'" data-col="'+ (dataCol1 + 4 )+'"><span class="wgtitotal">0.0</span><span class="gwgtitotal">0.0</span></td></tr>';
		
		dataCol1 = 5;
		dataCol  = dataCol + 1;	
		dataRow = dataRow + 1;		
				}
				table  = table + '<td data-row="0" data-col="'+ttlcol+'"></td><td data-row="0" data-col="'+ (ttlcol + 1) +'"></td><td data-row="0" data-col="'+ (ttlcol + 2) +'"></td><td data-row="0" data-col="'+ (ttlcol + 3) +'"></td><td data-row="0" data-col="'+ (ttlcol + 4) +'"></td></tr>';
				
t1 = t1 + '<td data-row="1" data-col="'+ttlcol +'"></td><td data-row="1" data-col="'+(ttlcol+ 1)+'"></td><td data-row="1" data-col="'+(ttlcol+ 2)+'"></td><td data-row="1" data-col="'+(ttlcol+ 3)+'"></td><td data-row="1" data-col="'+(ttlcol+ 4)+'"></td></tr>'
;
t2 = t2 + '<td data-row="2" data-col="'+ttlcol +'">Actual Cost</td><td data-row="2" data-col="'+(ttlcol + 1)+'">Average Cost</td><td data-row="2" data-col="'+(ttlcol + 2)+'">Boxes</td><td data-row="2" data-col="'+(ttlcol + 3)+'">Pallets</td><td data-row="2" data-col="'+(ttlcol + 4)+'">Ttl Weight</td></tr>';
				table = table  + t1;
				table = table + t2;
				table = table + titems;
table = table + '<tr class="item-row" data-row="'+dataRow+'"><td data-row="'+dataRow+'" data-col="0"></td><td data-row="'+dataRow+'" data-col="1"></td><td data-row="'+dataRow+'" data-col="2"></td><td data-row="'+dataRow+'" data-col="3"></td><td data-row="'+dataRow+'" data-col="4"></td>'+tlCols+'<td data-row="'+dataRow+'" data-col="'+ ttlcol + '"><span class="itotal_total">0.0</span></td><td data-row="'+dataRow+'" data-col="'+ (ttlcol + 1 )+'"><span class="avgitotal_total">0.0</span></td><td data-row="'+dataRow+'" data-col="'+ (ttlcol + 2 )+'"><span class="qtytotal_total">0.0</span></td><td data-row="'+dataRow+'" data-col="'+ (ttlcol + 3 )+'"><span class="pltitotal_total">0.0</span></td><td data-row="'+dataRow+'" data-col="'+ (ttlcol + 4 )+'"><span class="wgtitotal_total">0.0</span></td></tr>';
				
				var $wrapper = $("div[data-fieldname='supplieritems']").empty();
	$wrapper.html('<div style="overflow-x:auto;"><table id="myTable"  border="1" class="display nowrap dataTable dtr-inline">'+table+'</table><script type="text/javascript">$("#myTable").on("click", ".isupplier", function() { var idd = $(this).attr("id"); autocompletesupplier(idd); }); $("#myTable").on("change", "input", function() { $(this).updatedata(); }); $("#myTable").on("click", ".sitems", function() { var row = $(this).parents(".item-row"); var idd = row.find(".sitems").attr("id"); autocomplete(idd); }); $("#myTable").find(".sitems").each( function(){ $(this).updatedata(); });</script></div>');
				//$('#myTable').html(table);
				
				$("#myTable").find(".sitems").each( function(){ 
					$(this).updatedata();
				});
			}
			});

		if(!frm.doc.__islocal) {

			frm.add_custom_button(__("Recieving Mode"), function() {
				 frappe.call({
					method:'erpnext.api2.makeReceivingSheet',
					args: {
						master_purchase_order: frm.doc.name
					},
					callback: function(r) {
						console.log(r.message);
						frappe.set_route("Form", "Receiving Sheet", r.message);
						//location.reload();
					}
				}); 
					
			});


			frm.add_custom_button(__("Landing Cost"), function() {
				frappe.call({
					method:'erpnext.api2.makeLandingCost',
					args: {
						master_purchase_order: frm.doc.name
					},
					callback: function(r) {
						console.log(r.message);
						frappe.set_route("Form", "Master PO Landing Cost", r.message);
						//location.reload();
					}
				}); 
			});
			
			frm.add_custom_button(__("Update Order"), function() {
				var MasterPOItems = { 'shipping_date': frm.doc.shipping_date, 'arrival_date': frm.doc.arrival_date, 'cad': frm.doc.cad,  'usd': frm.doc.usd,  'pallet_weight': frm.doc.pallet_weight, 'total_boxes': '0', 'total_pallets': '0', 'total_weight': '0', 'total_actual_cost': 0, 'total_actual_cost_usd': 0,'name':frm.doc.name, 'order_type':frm.doc.order_type, 'master_purchase_order_item' : [] };

				var vindex = 0;
				var col_number = 0; var validate_items ="";
				$("#myTable").find(".sitems").each( function()
				{
					var row = $(this).parents('.item-row');
					if(row.find('.sitems').val() != '' && row.find('.item_code').val() == '') 
					{
					validate_items = validate_items + "#" +row.find('.sitems').attr('id') + ", ";
					}
					if(row.find('.item_code').val() != '') 
					{
						var myTable = $('#myTable');
						var colCount = myTable.find('td[data-row=0]').length;
						
						vindex = vindex+1;
						var weight = parseFloat(row.find('.weight').val());
						var purchase_pallets = parseFloat(row.find('.purchase_pallets').val());
						var gross_weight = parseFloat(row.find('.gross_weight').val());
							
						if(isNaN(weight)) { row.find('.weight').val(0);  }
						if(isNaN(purchase_pallets)) { row.find('.purchase_pallets').val(0.0); }
						if(isNaN(gross_weight)) { row.find('.gross_weight').val(0.0); }
						
						
						for(var i = 5; i < (colCount - 5); i++) 
						{
							var sidcell = $("#isupplier"+i).parents('td');
							if($('#isupplier'+i).val() != '' && sidcell.find('.isupplierid').val() == '') 
							{
								validate_items = validate_items + "#isupplier"+i + ", ";
							}
							if($('#isupplier'+i).val() != '') {
							col_number  = col_number + 1;
							var iqty = parseFloat(row.find('.iqty'+i).val());
							var rqty = parseFloat(row.find('.rqty'+i).val());
							var iprice = parseFloat(row.find('.iprice'+i).val());
							var iname = row.find('.iname'+i).val();
							
							if(isNaN(iqty)) { row.find('.iqty'+i).val(0);  }
							if(isNaN(rqty)) { row.find('.rqty'+i).val(0);  }
							if(isNaN(iprice)) { row.find('.iprice'+i).val(0.0); }
							
							var listitm = {'name': iname, 'qty': iqty, 'price': iprice, 'weight': row.find('.weight').val(), 'weight_per_unit': row.find('.weight').val(), 'gross_weight': row.find('.gross_weight').val(), 'uom': row.find('.uom').val(), 'description': row.find('.idesc').val(), 'purchase_pallets': row.find('.purchase_pallets').val(), 'item_code': row.find('.item_code').val(), 'item_name': row.find('.sitems').val(),'received_qty' : rqty, 'supplier_name': $('#isupplier'+i).val(), 'supplier': $('#isupplier'+i).val(), 'default_currency': sidcell.find('.default_currency').val(), 'row_number': vindex , 'col_number': col_number};
							MasterPOItems['master_purchase_order_item'].push(listitm);
							}
						}
						col_number = 0;
					}	
				});

			if(validate_items != '') { $(validate_items +' .abc').css('border','1px solid red'); msgprint("Please Select Item and Supplier from Dropdown list"); return false; }
			//console.log(MasterPOItems);
			var TableArray = [];
								var ItemArray = [];
								for (var i = 0; i < MasterPOItems.master_purchase_order_item.length; i++) 
								{
									var dta = MasterPOItems.master_purchase_order_item[i];
			var dt_col_num = dta.col_number - 1;
									var itmcd1 = { 'supplier_name': dta.supplier_name, 'supplier': dta.supplier ,'arrival_date': MasterPOItems.arrival_date ,'shipping_date': MasterPOItems.shipping_date , 'cad': MasterPOItems.cad,  'usd': MasterPOItems.usd, 'row_number': dta.row_number, 'col_number':  dta.col_number, items: [] };				
									var splcd = { 'item_name': dta.item_name ,  'item_code': dta.item_code, 'weight': dta.weight, 'weight_per_unit': dta.weight_per_unit, 'weight_lbs': dta.weight_per_unit, 'description': dta.description, 'purchase_pallets': dta.purchase_pallets, 'qty': dta.qty, 'price': dta.price, 'rate': dta.price, 'schedule_date': MasterPOItems.arrival_date,  'row_number' : dta.row_number,  'col_number' : dta.col_number};
							
									
									if( ItemArray.length > 0 ) 
									{
										if(typeof ItemArray[dt_col_num] != "undefined") {
											
											TableArray[dt_col_num][0]["items"].push(splcd);
										}
										else {
											ItemArray[dt_col_num] = [];							
											ItemArray[dt_col_num].push(itmcd1);
											TableArray[dt_col_num] = [];
											itmcd1["items"].push(splcd);
											TableArray[dt_col_num].push(itmcd1);
										}
									}
									else {
			ItemArray[dt_col_num] = [];	
									ItemArray[dt_col_num].push(itmcd1);
									TableArray[dt_col_num] = [];
									itmcd1["items"].push(splcd);
									TableArray[dt_col_num].push(itmcd1);
									}
					
								}
			var TableArray1 = {'name': frm.doc.name, 'details': TableArray};
			//console.log(TableArray1); return false;
				 frappe.call({
					method:'erpnext.api2.updateMasterPoOrder',
					args: {
						po: MasterPOItems,
						ps: TableArray1
					},
						callback: function(r) {
						console.log(r.message);
						frappe.show_alert(r.message+ ' - update successfully ', 5);
						frappe.set_route("Form", "Master Purchase Order", r.message);
						//location.reload();
					}
				});  
			});
			
			
			
		}
		else 
		{
				frm.add_custom_button(__("Save Order"), function() {
					//console.log(frm.doc);
					var shd = '';
					var MasterArray = [];
					var MasterPOItems = { 'shipping_date': frm.doc.shipping_date, 'arrival_date': frm.doc.arrival_date, 'cad': frm.doc.cad,  'usd': frm.doc.usd,  'pallet_weight': frm.doc.pallet_weight, 'total_boxes': '0', 'total_pallets': '0', 'total_weight': '0', 'total_actual_cost': 0, 'total_actual_cost_usd': 0,'name':frm.doc.name, 'order_type':frm.doc.order_type, 'master_purchase_order_item' : [] };

					MasterArray.push({
						'name':frm.doc.name,
						'shipping_date': frm.doc.shipping_date,    
						'arrival_date': frm.doc.arrival_date,    
						'cad': frm.doc.cad,  
						'usd': frm.doc.usd,
						'total_boxes': '0',
						'total_pallets': '0',
						'total_weight': '0',
						'total_actual_cost': 0,
						'total_actual_cost_usd': 0
					});
					var ItemsArray = [];
					var vindex = 0;
					var col_number = 0; var validate_items = "";
					$("#myTable").find(".sitems").each( function()
					{
						var row = $(this).parents('.item-row');
						if(row.find('.sitems').val() != '' && row.find('.item_code').val() == '') 
						{
							validate_items = validate_items + "#" +row.find('.sitems').attr('id') + ", ";
						}
						if(row.find('.item_code').val() != '') 
						{
							var myTable = $('#myTable');
							var colCount = myTable.find('td[data-row=0]').length;
							shd = shd + row.find('.sitems').val();
							shd = shd + 'Description: ' + row.find('.idesc').val();
							
							vindex = vindex+1;
							var arrr = 'array'+vindex;
							MasterArray[arrr] = [];
							var weight = parseFloat(row.find('.weight').val());
							var purchase_pallets = parseFloat(row.find('.purchase_pallets').val());
							var gross_weight = parseFloat(row.find('.gross_weight').val());
								
							if(isNaN(weight)) { row.find('.weight').val(0);  }
							if(isNaN(purchase_pallets)) { row.find('.purchase_pallets').val(0.0); }
							if(isNaN(gross_weight)) { row.find('.gross_weight').val(0.0); }
							
							var itmcd = {'item_code': row.find('.item_code').val(), 'weight': weight, 'purchase_pallets': purchase_pallets, 'gross_weight': gross_weight};
							MasterArray[arrr].push(itmcd);
							
							var total_boxes = 0; 
							var total_pallet = 0;
							var total_net_weight = 0;
							var total_gross_weight_lbs = 0;
							var total_weight_kg = 0;
							
							for(var i = 5; i < (colCount - 5); i++) 
							{
								var sidcell = $("#isupplier"+i).parents('td');
								if($('#isupplier'+i).val() != '' && sidcell.find('.isupplierid').val() == '') 
								{
									validate_items = validate_items + "#isupplier"+i + ", ";
								}
								if($('#isupplier'+i).val() != '') {
								col_number  = col_number + 1;
								var iqty = parseFloat(row.find('.iqty'+i).val());
								var iprice = parseFloat(row.find('.iprice'+i).val());
								
								if(isNaN(iqty)) { row.find('.iqty'+i).val(0);  }
								if(isNaN(iprice)) { row.find('.iprice'+i).val(0.0); }
								
								shd = shd + ' Suplier'+i+': ' + $('#isupplier'+i).val();
								shd = shd + ' Qty'+i+': ' + iqty;
								shd = shd +  ' Price'+i+': ' + iprice;
								
								
								var qty = $('.iqty' + i);
								var price = $('.iprice' + i);

								for (var k = 0; k < qty.length; k++) {
									total_boxes = total_boxes + parseFloat(qty[k].value);
									if(row.find('.purchase_pallets').val() > 0) 
									{
										total_pallet = total_pallet + (parseFloat(qty[k].value) / parseFloat(row.find('.purchase_pallets').val()));
									}
									total_net_weight = total_net_weight + parseFloat(qty[k].value * row.find('.weight').val());
									total_gross_weight_lbs = total_gross_weight_lbs +  parseFloat(qty[k].value * row.find('.gross_weight').val());
									total_weight_kg = total_weight_kg +  parseFloat(total_gross_weight_lbs * 0.45359237);
								} 
								
								
								var itmsp = {'supplier': $('#isupplier'+i).val(),'qty': iqty,'rate': iprice};
									MasterArray[arrr].push(itmsp);	
								var listitm = {'qty': iqty, 'price': iprice, 'weight': row.find('.weight').val(),  'gross_weight': row.find('.gross_weight').val(),  'uom': row.find('.uom').val(), 'weight_per_unit': row.find('.weight').val(), 'description': row.find('.idesc').val(), 'purchase_pallets': row.find('.purchase_pallets').val(), 'item_code': row.find('.item_code').val(), 'item_name': row.find('.sitems').val(),'received_qty' : 0, 'supplier_name': $('#isupplier'+i).val(), 'supplier': $('#isupplier'+i).val(), 'default_currency': sidcell.find('.default_currency').val(), 'row_number': vindex , 'col_number': col_number, 'total_boxes': total_boxes, 'total_pallet': total_pallet, 'total_net_weight': total_net_weight, 'total_gross_weight_lbs': total_gross_weight_lbs, 'total_weight_kg': total_weight_kg};
								MasterPOItems['master_purchase_order_item'].push(listitm);
								
								total_boxes = 0; 
								total_pallet = 0;
								total_net_weight = 0;
								total_gross_weight_lbs = 0;
								total_weight_kg = 0;
								}
							}
							col_number = 0;
						}	
					});

				if(validate_items != '') { $(validate_items +' .abc').css('border','1px solid red'); msgprint("Please Select Item and Supplier from Dropdown list"); return false; }
				//console.log(MasterPOItems);
				var TableArray = [];
									var ItemArray = [];
									for (var i = 0; i < MasterPOItems.master_purchase_order_item.length; i++) 
									{
										var dta = MasterPOItems.master_purchase_order_item[i];
										var dt_col_num = dta.col_number - 1;
										var conversion_rate = 1;
										var plc_conversion_rate = 1;
										if(dta.default_currency == "USD") { 
											if(frm.doc.usd > 0) {
												conversion_rate = parseFloat(1 / frm.doc.usd);
												plc_conversion_rate = parseFloat(1 / frm.doc.usd);
											}
										}
										
										var itmcd1 = { 'supplier_name': dta.supplier_name, 'supplier': dta.supplier ,'arrival_date': MasterPOItems.arrival_date ,'shipping_date': MasterPOItems.shipping_date , 'cad': MasterPOItems.cad,  'usd': MasterPOItems.usd, 'conversion_rate': conversion_rate, 'plc_conversion_rate': plc_conversion_rate, 'order_type':frm.doc.order_type, 'row_number': dta.row_number, 'col_number':  dta.col_number, 'total_boxes': dta.total_boxes, 'total_pallet': dta.total_pallet, 'total_net_weight': dta.total_net_weight, 'total_gross_weight_lbs': dta.total_gross_weight_lbs, 'total_weight_kg': dta.total_weight_kg, items: [] };				
										var splcd = { 'item_name': dta.description ,  'item_code': dta.item_code, 'weight': dta.weight, 'weight_per_unit': dta.weight_per_unit, 'weight_lbs': dta.weight_per_unit, 'gross_weight_lbs': dta.gross_weight, 'description': dta.description, 'purchase_pallets': dta.purchase_pallets, 'boxes_pallet_for_purchase': dta.purchase_pallets, 'qty': dta.qty, 'box': dta.qty, 'uom': dta.uom, 'price': dta.price, 'rate': dta.price, 'box_unit_rate': dta.price, 'schedule_date': MasterPOItems.arrival_date,  'row_number' : dta.row_number,  'col_number' : dta.col_number};
								
								 
										if( ItemArray.length > 0 ) 
										{
											if(typeof ItemArray[dt_col_num] != "undefined") {
												
												TableArray[dt_col_num][0]["items"].push(splcd);
											}
											else {
												ItemArray[dt_col_num] = [];							
												ItemArray[dt_col_num].push(itmcd1);
												TableArray[dt_col_num] = [];
												itmcd1["items"].push(splcd);
												TableArray[dt_col_num].push(itmcd1);
											}
										}
										else {
				ItemArray[dt_col_num] = [];	
										ItemArray[dt_col_num].push(itmcd1);
										TableArray[dt_col_num] = [];
										itmcd1["items"].push(splcd);
										TableArray[dt_col_num].push(itmcd1);
										}
						
									}
				var TableArray1 = {'name': frm.doc.name, 'details': TableArray};
				console.log(TableArray1);
				//return false;
					frappe.call({
						method:'erpnext.api2.makeMasterPoOrder',
						args: {
							po: MasterPOItems,
							ps: TableArray1
						},
							callback: function(r) {
							console.log(r.message);
							frm.doc.__islocal = 0;
							frappe.show_alert(r.message+ ' - Created Successfully ', 5);
							frappe.set_route("Form", "Master Purchase Order", r.message);
							//location.reload();
						}
					}); 
	
				});
			
		}

	}
});


frappe.ui.form.on('Master PO', {
    add_supplier: function (frm, cdt, cdn) {
    	var row = locals[cdt][cdn];
    	if(row.selected_suppliers.split(/\r\n|\r|\n/).length>5){
    		alert('More Than 5')
    	}else{

    	var d = new frappe.ui.Dialog({
		    'fields': [
		        {'label': 'Supplier','fieldname': 'supplier', 'fieldtype': 'Link', 'options': 'Supplier', 'reqd': 1},
		        {'label': 'QTY','fieldname': 'qty', 'fieldtype': 'Data', 'reqd': 1},
		        {'label': 'Price','fieldname': 'price', 'fieldtype': 'Currency', 'reqd': 1}
		    ],
		    primary_action: function(){

		        d.hide();

		        var args = d.get_values();

		        var row = locals[cdt][cdn];


		        if(!args) return;
		        
				var selected_suppliers = null;
				if(row.selected_suppliers)
					selected_suppliers = row.selected_suppliers + "\n" + d.get_values()['supplier'] + '|' + d.get_values()['qty'] + '>>' + d.get_values()['price'];
				else
					selected_suppliers = d.get_values()['supplier'];
				frappe.model.set_value(cdt, cdn, "selected_suppliers", selected_suppliers);
				frappe.model.set_value(cdt, cdn, "total_price", row.total_price + d.get_values()['price']);
				frappe.model.set_value(cdt, cdn, "supplier", null);

				// console.log(row.selected_suppliers.split(/\r\n|\r|\n/)[1].split('|')[0])
				// console.log(row.selected_suppliers.split(/\r\n|\r|\n/)[1].split('|')[1].split('>>')[0])
				// console.log(row.selected_suppliers.split(/\r\n|\r|\n/)[1].split('>>')[1])


				length = row.selected_suppliers.split(/\r\n|\r|\n/).length
			    if(length > 1){
			    	for(var i=1 ; i < length ; i++){
			    		item = row.selected_suppliers.split(/\r\n|\r|\n/)[i].split('|')[0]
			    		qty = row.selected_suppliers.split(/\r\n|\r|\n/)[i].split('|')[1].split('>>')[0]
			    		price = row.selected_suppliers.split(/\r\n|\r|\n/)[i].split('>>')[1]
			    	}
			    	frappe.model.set_value(cdt, cdn, "boxes", parseInt(row.boxes) + parseInt(qty));
			    	frappe.model.set_value(cdt, cdn, "pallets", row.boxes/row.purchase_pallets);
			    	frappe.model.set_value(cdt, cdn, "weight", row.boxes*row.weight_per_unit);
			    	frappe.model.set_value(cdt, cdn, "actual_cost", parseFloat(row.actual_cost) + parseFloat(price*qty));
			    	frappe.model.set_value(cdt, cdn, "average_cost", row.actual_cost/(length-1));
			   		
			    }



		    }
		});
		d.show();


    }

    
frappe.ui.form.on("Master PO", "boxes", function(frm, cdt, cdn) {
    // code for calculate total and set on parent field.
    total = 0;
    $.each(frm.doc.master_po || [], function(i, d) {
        total += flt(d.boxes);
    });
    frm.set_value("total_boxes", total);
    frm.set_value("numbers_boxes", total);
});


frappe.ui.form.on("Master PO", "average_cost", function(frm, cdt, cdn) {
    // code for calculate total and set on parent field.
    total = 0;
    $.each(frm.doc.master_po || [], function(i, d) {
        total += flt(d.average_cost);
    });
    frm.set_value("total_actual_cost", total);
    frm.set_value("total_actual_cost_usd", total/cur_frm.doc.cad);
});


frappe.ui.form.on("Master PO", "pallets", function(frm, cdt, cdn) {
    // code for calculate total and set on parent field.
    total = 0;
    $.each(frm.doc.master_po || [], function(i, d) {
        total += flt(d.pallets);
    });
    frm.set_value("total_pallets", total);
    frm.set_value("numbers_pallets", total);
    frm.set_value("lbs_pallets", total*20);
    frm.set_value("kgs_pallets", cur_frm.doc.lbs_pallets*0.453592);
    frm.set_value("kgs_gross", cur_frm.doc.kgs_pallets+cur_frm.doc.kgs_boxes);
});


frappe.ui.form.on("Master PO", "weight", function(frm, cdt, cdn) {
    // code for calculate total and set on parent field.
    total = 0;
    $.each(frm.doc.master_po || [], function(i, d) {
        total += flt(d.weight);
    });
    frm.set_value("total_weight", total);
    frm.set_value("lbs_boxes", total);
    frm.set_value("lbs_gross", cur_frm.doc.lbs_boxes*cur_frm.doc.lbs_pallets);
    frm.set_value("kgs_boxes", cur_frm.doc.lbs_boxes*0.453592);
    frm.set_value("kgs_gross", cur_frm.doc.kgs_pallets+cur_frm.doc.kgs_boxes);
});




}

})