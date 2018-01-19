jQuery.noConflict();

jQuery( document ).ready(function() {

	// http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
	function getParameterByName(name) {
		name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
		var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
			results = regex.exec(location.search);
		return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
	}

	if(getParameterByName("code") != "") {
		popupMessage("Google contacts imported!");
	}
	
	jQuery(".infopopup").click(function() {
		jQuery(this).css("display","none");
		window.location.replace("/");
	});

	jQuery("#noticediv").click(function() {
		jQuery(this).css("display","none");
	});
	
	jQuery.ajax({
			url: '/googleimportlink',
			type: 'get',
			data: { },
			success: function(results) {
				jQuery("#googleimport").attr("href", results);
			}
	});
	
	jQuery(document).on('click', ".addButton", function(){

		var inputNum = checkInput();

		if (inputNum != 4) {
			var alertdiv = jQuery('<div />').addClass("alert alert-danger");
			var pElement = jQuery('<p />');
			pElement.text("You should enter all required parameters to add a contarct");

			alertdiv.append(pElement);
			jQuery("#noticediv").html(alertdiv).css("display","block");
		}
		else {
			var data = { 
				name : jQuery(document).find('input[name="name"]').val(),
				phone : jQuery(document).find('input[name="phone"]').val(),
				address : jQuery(document).find('input[name="address"]').val(),
				email : jQuery(document).find('input[name="email"]').val()
			}
			ajaxCall("put", data, addModifyContact, this);
		}
	});

	jQuery(document).on('click', ".searchButton", function () {
		var searchString 	= jQuery(document).find('input[name="searchInput"]').val();
		var query 			=  { searchword : searchString };
		ajaxCall("get", query, showcontactDetail, this);
	});

	jQuery(document).on('click', "#contactlink", function(){
		var query =  { searchword : "" };
		ajaxCall("get", query, refreshContactList, this);
	});

	jQuery(document).on('click', "#addlink", function() {
		editPanel();
	});

	jQuery(document).on('click', "#modifylink", function() {
		modifyPanel();
	});

	jQuery(document).on('click', "#removelink", function() {
		modifyPanel();
	});

	jQuery(document).on('click', "#aboutlink", function() {
		var data = { };
		ajaxCall("options", data, versionPanel, this);	
	});

	jQuery(document).on('click', ".modifyButton", function() {

		var modify_name = jQuery(this).parent().find('input[name="modifyname"]').val();
		if (!modify_name) {
			modify_name = jQuery(this).parent().find('p[name="contactname"]').attr("id");
		}

		var modify_phone = jQuery(this).parent().find('input[name="modifyphone"]').val();
		if (!modify_phone) {
			modify_phone = jQuery(this).parent().find('p[name="contactphone"]').attr("id");
		}

		var modify_address = jQuery(this).parent().find('input[name="modifyaddress"]').val();
		if (!modify_address) {
			modify_address = jQuery(this).parent().find('p[name="contactaddress"]').attr("id");
		}

		var modify_email = jQuery(this).parent().find('input[name="modifyemail"]').val();
		if (!modify_email) {
			modify_email = jQuery(this).parent().find('p[name="contactemail"]').attr("id");
		}

		var dataWithId = {
			id: jQuery(this).parent().find('p[name="contactid"]').attr("id"),
			name: modify_name,
			phone: modify_phone,
			address: modify_address,
			email: modify_email
		};
		ajaxCall("post", dataWithId, addModifyContact, this);
	});

	jQuery(document).on('click', ".deleteButton", function() {
		var data = {
			id: jQuery(this).parent().find('p[name="contactid"]').attr("id")
		}
		ajaxCall("delete", data, removeContact, this);
	});

	function checkInput()
	{
		var inputnames = ["name", "phone", "address", "email"];
		var inputNum = 0;
		jQuery.each(inputnames, function(i, inputname) {
			var value 		= jQuery(document).find('input[name="'+ inputname + '"]').val();
			var trim_value 	= jQuery.trim(value);

			if (trim_value.length > 0) {
				inputNum++;
			}
		});
		return inputNum;
	}

	function popupMessage(message) {
		jQuery(".infopopup").css("display","block").html(message);
	}
	
	function removeContact(results, buttonElement) {
		popupMessage("Contact succesfully removed!");
	}		
		
	function addModifyContact(results, buttonElement)
	{
		popupMessage("Contact succesfully added/changed!");
	}

	function createTable(results)
	{
		var div 		= jQuery('<div />').addClass("panel panel-danger");
		var paneldiv 	= jQuery('<div />').addClass("panel-heading text-center").css("font-size", "20px");
		var strong 		= jQuery('<strong />');
		strong.text("Contact list");
		paneldiv.append(strong);
		div.append(paneldiv);

		var table = jQuery('<table></table>').addClass('table table-striped text-center table-hover').css("font-size", "20px");

		var thead	= jQuery('<thead />').css("font-weight", "bold");
		var tr 		= jQuery('<tr>').append(
					jQuery('<td>').text('#'),
					jQuery('<td>').text('name'),
					jQuery('<td>').text('phone'),
					jQuery('<td>').text('address'),
					jQuery('<td>').text('email')
		);
		thead.append(tr);
		table.append(thead);

		var tbody = jQuery('<tbody >');

		jQuery.each(results, function(i, result) {
			if (result.name) {
				var row =
				jQuery('<tr>').append(
					jQuery('<td>').text(i),
					jQuery('<td>').text(result.name),
					jQuery('<td>').text(result.phone),
					jQuery('<td>').text(result.address),
					jQuery('<td>').text(result.email)
				);
				tbody.append(row);
			}
		});
		table.append(tbody);

		div.append(table);
		jQuery("#tablediv").html(div);
	}

	function refreshContactList(results, buttonElement)
	{
		results = JSON.parse(results);

		if (results) {
			createTable(results);
		}
		else {
			var notice = jQuery('<p>').text("No contacts right now, want to add one?");
			jQuery("#tablediv").append(notice);
		}
	}

	function createliElenment (listName)
	{
		if (listName == "title") {
			var liElement 		= jQuery('<li />').addClass("list-group-item list-group-item-success").css("font-weight", "bold");
			liElement.append("Add contact");
			return liElement;
		}
		var liElement 		= jQuery('<li />').addClass("list-group-item").css("font-weight", "bold");
		var inputElement	= jQuery('<input />', {type: 'text', name: listName, placeholder: listName});

		liElement.append(listName + ": ");
		liElement.append(inputElement);
		return liElement;
	}

	jQuery.fn.center = function () {
		this.css("position","absolute");
		this.css("left", Math.max(0, ((jQuery(window).width() - jQuery(this).outerWidth()) / 2) + jQuery(window).scrollLeft()) + "px");
		return this;
	}

	function editPanel(results, buttonElement)
	{
		var div 		= jQuery('<div />').addClass(" text-center").css("font-size", "20px").width(800);
		div.center();
		var ulElement 	= jQuery('<ul />').addClass("list-group addNewContact");
		var listnames 	= ["title", "name", "phone", "address", "email"];
		
		jQuery.each(listnames, function(i, listname) {
			var liElement   = createliElenment (listname);
			ulElement.append(liElement);
		});

		div.append(ulElement);

		var btnElenment	= jQuery('<button />', {type: "button"}).addClass("btn btn-primary btn-lg addButton");
		btnElenment.text("Add");
		div.append(btnElenment);

		jQuery("#tablediv").html(div);
	}

	function versionPanel(results, buttonElement)
	{
		var divElement = jQuery('<div />').addClass("alert alert-success");
		var pElement   = jQuery('<p />');
		var content	= "Currently the version of our address book is: " + results + " we will keep working to improve it, so keep following us :)";
		pElement.text(content);

		divElement.append(pElement);
		jQuery("#tablediv").html(divElement);
	}

	function addsearchElement()
	{
		var divElement 		= jQuery('<div />').addClass("input-group");
		var inputElement 	= jQuery('<input />', {type: "text", name: "searchInput"}).addClass("form-control").css("font-size", "20px");
		var spanElement 	= jQuery('<span />').addClass("input-group-btn");

		var buttonElement 	= jQuery('<button />', {type: "button"}).addClass('btn btn-primary searchButton');
		var span 			= jQuery('<span />').addClass("glyphicon glyphicon-search");
		buttonElement.append(span);

		spanElement.append(buttonElement);

		divElement.append(inputElement);
		divElement.append(spanElement);
		return divElement;
	}

	function addcontact(contact)
	{
		var divElement 	= jQuery('<div />').addClass("alert alert-info col-sm-7 col-md-6");

		var pElementid 	= jQuery('<p />', {name: "contactid", id: contact._id});
		var pid    = "id:" + contact._id;	
		pElementid.text(pid);
		pElementid.append(jQuery('<br>'));
		divElement.append(pElementid);
		
		// Name
		var pElement 	= jQuery('<p />', {name: "contactname", id: contact.name});
		var span        = jQuery('<span />').css("font-weight", "bold");
		span.text("Name: ").addClass("firstRow");
		pElement.append(span);

		var span = jQuery('<span />');
		span.text(contact.name).addClass("secondRow");
		pElement.append(span);

		var span = jQuery('<span />').css("font-weight", "bold");
		span.text("New name: ").addClass("thirdRow");
		pElement.append(span);

		var inputElement = jQuery('<input />', {type: "text", name: "modifyname"}).addClass("fourthRow");
		pElement.append(inputElement);
		pElement.append(jQuery('<br>'));
		divElement.append(pElement);

		// Phone
		var pElement1 = jQuery('<p />', {name: "contactphone", id: contact.phone});
		var span      = jQuery('<span />').css("font-weight", "bold");
		span.text("Phone: ").addClass("firstRow");
		pElement1.append(span);

		var span = jQuery('<span />');
		span.text(contact.phone).addClass("secondRow");
		pElement1.append(span);

		var span = jQuery('<span />').css("font-weight", "bold");
		span.text("New phone: ").addClass("thirdRow");
		pElement1.append(span);	

		var inputElement = jQuery('<input />', {type: "text", name: "modifyphone"}).addClass("fourthRow");
		pElement1.append(inputElement);
		pElement1.append(jQuery('<br>'));
		divElement.append(pElement1);

		// Address
		var pElement2 = jQuery('<p />', {name: "contactaddress", id: contact.address});
		var span      = jQuery('<span />').css("font-weight", "bold");
		span.text("Address: ").addClass("firstRow");
		pElement2.append(span);

		var span = jQuery('<span />');
		span.text(contact.address).addClass("secondRow");
		pElement2.append(span);	

		var span      = jQuery('<span />').css("font-weight", "bold");
		span.text("New address: ").addClass("thirdRow");
		pElement2.append(span);

		var inputElement = jQuery('<input />', {type: "text", name: "modifyaddress"}).addClass("fourthRow");
		pElement2.append(inputElement);
		pElement2.append(jQuery('<br>'))
		divElement.append(pElement2);

		// E-mail
		var pElement3 = jQuery('<p />', {name: "contactemail", id: contact.email});
		var span      = jQuery('<span />').css("font-weight", "bold");
		span.text("Email: ").addClass("firstRow");
		pElement3.append(span);

		var span = jQuery('<span />');
		span.text(contact.email).addClass("secondRow");
		pElement3.append(span);	

		var span      = jQuery('<span />').css("font-weight", "bold");
		span.text("New email: ").addClass("thirdRow");
		pElement3.append(span);

		var inputElement = jQuery('<input />', {type: "text", name: "modifyemail"}).addClass("fourthRow");
		pElement3.append(inputElement);
		pElement3.append(jQuery('<br>'))
		divElement.append(pElement3);

		// Buttons
		var btnElenment = jQuery('<button />', {type: "button"}).addClass("btn btn-primary modifyButton");
		btnElenment.text("Modify").addClass("modify");
		divElement.append(btnElenment);

		divElement.append(" ");
		var btnElenment = jQuery('<button />', {type: "button"}).addClass("btn btn-danger deleteButton");
		btnElenment.text("Delete").addClass("delete");
		divElement.append(btnElenment);

		return divElement;
	}

	function modifyPanel(results, buttonElement)
	{
		var divElement = jQuery('<div />').addClass("panel panel-success panel");

		var diveElement1 = jQuery('<div />').addClass("panel-heading");
		var hElement	 = jQuery('<h3 />').addClass("panel-title text-center").css("font-weight", "bold");
		hElement.text("Modify");

		diveElement1.append(hElement);

		var diveElement2 = jQuery('<div />').addClass("panel-body");
		var panelcontent = addsearchElement();
		diveElement2.append(panelcontent);

		divElement.append(diveElement1);
		divElement.append(diveElement2);

		jQuery("#tablediv").html(divElement);
	}

	function addContactdetail (results, buttonElement)
	{
		modifyPanel(results, buttonElement);
		jQuery.each(results, function(i, contact) {
			var divElement = addcontact(contact);
			var panel      = jQuery(document).find(".panel.panel-success");
			panel.append(divElement);
		});
	}

	function showcontactDetail(results, buttonElement)
	{
		results = JSON.parse(results);

		if (results) {
			addContactdetail(results, buttonElement);
		}
	}

	function ajaxCall(method, data, callback, buttonElement)
	{
		jQuery.ajax({
				url: '/api/',
				type: method,
				data: data,
				success: function(results) {
					callback(results, buttonElement);
				}
		});
	}
});