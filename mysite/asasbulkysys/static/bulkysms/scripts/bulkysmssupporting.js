//Declaration of site global variables
var VIEWING_MODE=1;
var EDITING_MODE=2; //Editing group or campaign
var current_menu=null;
var global_group_id=""; 
var global_name="";
var contact_ids_found=0;

var user_defined_campaign_frequency_status=0;

var total_no_msg_box=0;// This variable is important when defining the number of messages to be used in a campaign

 var site="http://localhost:8000/asasbulkysys/";

$( document ).ready(function() {

    //start by clearing localStorage
     localStorage.removeItem("Contacts");
     localStorage.removeItem("AllContacts");
     localStorage.removeItem("Groups");
     localStorage.removeItem("Campaigns");
     localStorage.removeItem("SMSTemplates");

    initializeMenu();

    

   //var bootstrapButton = $.fn.button.noConflict()
   //$.fn.bootstrapBtn = bootstrapButton;
});


//This sort algorithm is for sorting templates by their categories.
var insertionSort=function (items) {

    var len = items.length,     // number of items in the array
        value,value_id,                     // the value currently being compared
        i,                          // index into unsorted section
        j;                          // index into sorted section
    
    for (i=0; i < len; i++) {
    
        // store the current value because it may shift later
        value = items[i];
        value_id=items[i]["CategoryID"];
        /*
         * Whenever the value in the sorted section is greater than the value
         * in the unsorted section, shift all items in the sorted section over
         * by one. This creates space in which to insert the value.
         */
        for (j=i-1; j > -1 && items[j]["CategoryID"] > value_id; j--) {
            items[j+1]= items[j]
        }

        items[j+1] = value;
    }
    
    return items;
}


//this binary serach algorithm is to check if category has already been picked, it is not inserted again.
var binarySearch=function (arr, target) {
    let left = 0;
    let right = arr.length - 1;
    while (left <= right) {
        const mid = left + Math.floor((right - left) / 2);
    
        if (arr[mid]["CategoryID"]==target) {
            
            return mid;
        }
        if (arr[mid]["CategoryID"] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1;
}



//for slider of address book

		var handleSliderNav = function () {
		$('#address-book').sliderNav();
		/*
		$('#address-book .slider-content ul li ul li a').click(function(e){
			e.preventDefault();
			var contact_card = $('#contact-card');
			//Get the name clicked on
			var name = $(this).text();
			//Set the name
			$('#contact-card .panel-title').html(name);
			$('#contact-card #card-name').html(name);
			//Randomize the image
			var img_id = Math.floor(Math.random() * (5 - 1 + 1)) + 1;
			//Set the image
			$('#contact-card .headshot img').attr('src', 'img/addressbook/'+img_id+'.jpg');
			contact_card.removeClass('animated fadeInUp').addClass('animated fadeInUp');
			var wait = window.setTimeout( function(){
				contact_card.removeClass('animated fadeInUp')},
				1300
			);
		});*/
	};

//progress bar editing

var removeLoadingCircle=function (){
 //$("#progressbar").html("");
  $("#myprogressbar").removeClass("loader");
// alert($("#progressbar").html());

};

var addLoadingCircle=function (){
 //$("#progressbar").html("");
  $("#myprogressbar").addClass("loader");
// alert($("#progressbar").html());

};


var removeLoadingCircleCampaign=function (){
 //$("#progressbar").html("");
  $("#myprogressbar_campaign").removeClass("loader");
// alert($("#progressbar").html());

};

var addLoadingCircleCampaign=function (){
 //$("#progressbar").html("");
  $("#myprogressbar_campaign").addClass("loader");
// alert($("#progressbar").html());

};


var removeLoadingCircleChart=function (){
 //$("#progressbar").html("");
  $("#myprogressbar_chart").removeClass("loader");
// alert($("#progressbar").html());

};

var addLoadingCircleChart=function (){
 //$("#progressbar").html("");
  $("#myprogressbar_chart").addClass("loader");
// alert($("#progressbar").html());

};



var typingFeedback=function(){

$("#myprogressbar").html('<b><i style=\"color:green;\">Typing...</i></b>');

};

var clearFeedback=function(status){

$("#myprogressbar").html('&nbsp;');
var msgstr=$("#addresssmsbox").val()
if((msgstr.length>0)&&(status))
   $("#myprogressbar").html('<b><i style=\"color:green;\">Message Ready? Send it!!</i></b>');
     


};
var clearDivForm=function(divElement){
         alert("ClearCalled");

          var ele = document.getElementById(divElement);

        // IT WILL READ ALL THE ELEMENTS. <p>, <div>, <input> ETC.
        for (i = 0; i < ele.childNodes.length; i++) {

            // SINCE THE <input> FIELDS ARE INSIDE A <p> TAG, 
            // I'LL USE THE "firstChild" PROPERTY TO GET THE <input> TAG.
            var child = ele.childNodes[i].firstChild;
            //console.log(child);

            // CHECK IF CHILD NOT NULL.
            // THIS IS IMPORTANT AS IT WILL RETURN A TEXT FOR EVERY "Whitespace".
            // 'Whitespace' IS A TEXT OR NODE BETWEEN <div> AND <p> AND AFTER <p>.
            if (child) {
                switch (child.type) {
                    case 'button':
                    case 'text':
                    case 'submit':
                    case 'password':
                    case 'file':
                    case 'email':
                    case 'date':
                    case 'number':
                        child.value = '';
                    case 'checkbox':
                    case 'radio':
                        child.checked = false;
                }
            }
        }
};

//This function is important when we want to check if a group has members before trying to send messages
var existGroupMembers=function (group_id)
{
 //alert(item);
 selected_group_item=group_id;//We need this incase we refresh the address book to get back to where we were last time. Fo istance when searching the user may decide to clear te search box and that can triggger the address book to be refreshed. What if the was an item displayed on the contact card, the we have to retain it
 

json_obj=JSON.parse(localStorage.getItem("Groups"));
 
 for(var y in json_obj)
 {
  x=json_obj[""+y+""]["GroupID"];
  if(x==selected_group_item)
   {

  
    //alert(json_obj[""+y+""]["first_name"]+" was clicked");
    var num_of_members=json_obj[""+y+""]["NumMembers"];
      

    return num_of_members;

    }

 }

 return -1;


};



//for sending SMS to a group
var sendGroupSMS=function(group_id)
{
     //var sms_generalization=$('input[name=smsoptradio]:checked').val(); 

     var sms_generalization=$("input[type='radio'][name='smsoptradio']:checked").val();

     var group_members=existGroupMembers(group_id);

     if(group_members==0)

     {

      alert("Error: Can't send a message to a group with no members");
      return;
     }
     else
     {
      if(group_members>0);
      else
       {

       alert("Error: The group doesn't exists"); 
       }
     

     }


     
     jsonObject={MessageBody:$("#addresssmsbox").val(),MobNo:group_id,SMSAudience:"Bulky",SMSGeneralization:sms_generalization};
     //alert($("#addresssmsbox").val());
     //return;
      $("#myprogressbar").html('');
      addLoadingCircle();
      var urlstr=site;
      urlstr=urlstr+"jsonupdate/SS/";// Send SMS to a group.
      $.ajax({
             url: urlstr,
             dataType: "jsonp",
             method: "POST",
             data:JSON.stringify(jsonObject),
             cache: false
             })
            .done(function( html ) {
             //clearInterval(display_interval);
             //$("#progresspopup").popup( "close"); // close the pop up for progress once the results are returned from the database
             //alert("Message Sent");

             removeLoadingCircle();
             $("#myprogressbar").html('<b style=\"color:blue;\">Message Sent!</b>');
             

             });


};



//Find selected message template and put into a box for composing SMS
var pickMessageTemplate=function(){
   var selected_template=$("#template_message").val();
  $("#addresssmsbox").val(selected_template);
 

};

//send one sms from the address book
var sendOneSMS=function()
{
   //var sms_generalization=$('input[name=smsoptradio]:checked').val(); 
    var sms_generalization=$("input[type='radio'][name='smsoptradio']:checked").val();
    if(sms_generalization==undefined)
      sms_generalization="Personalized";
    
    jsonObject={MessageBody:$("#addresssmsbox").val(),MobNo:$("#primarymobile").val(),SMSAudience:"Individual",SMSGeneralization:sms_generalization};
      $("#myprogressbar").html('');
      addLoadingCircle();
      var urlstr=site;
      urlstr=urlstr+"jsonupdate/SS/";// Retrieve
      $.ajax({
             url: urlstr,
             dataType: "jsonp",
             method: "POST",
             data:JSON.stringify(jsonObject),
             cache: false
             })
            .done(function( html ) {
             //clearInterval(display_interval);
             //$("#progresspopup").popup( "close"); // close the pop up for progress once the results are returned from the database
             //alert("Message Sent");

             removeLoadingCircle();
             $("#myprogressbar").html('<b style=\"color:blue;\">Message Sent!</b>');
             

             });


};

var loadToSMSTXTBox=function(){

$("#smstemplatesdialog").dialog("close"); //close the dialog box for displaying sms templates

//Take the selected template and put it inside a box for composing SMS

$("#addresssmsbox").val($("#selected_template_content").html());




};

var showSelectedSMSTemplate=function()
{


var selected_template_value=$("#selecttemplate").val();
if(selected_template_value==-1);
else
   $("#selected_template_content").html(selected_template_value);


};




//When selecting template categories then retrieve its associated SMS templates
var showSMSTemplates=function(){
  
    var selected_category=$("#selecttemplatecategory").val();
    json_obj=JSON.parse(localStorage.getItem("SMSTemplates"));
    var retrieved_category_id;
    var template_list="";
    var template_counter=0;
    
     for(var y in json_obj)
     {
        retrieved_category_id=json_obj[""+y+""]["ID"];
        
        
        if(retrieved_category_id==selected_category)
        {
              // now get all the templates for this category id
              templ_obj=json_obj[""+y+""]["Templates"];
              template_list="<option value=\"-1\" title=\"Select Template Category\">Select Template Category</option>";
              for(var x in templ_obj)
              {
                  template_counter=template_counter+1

                  template_list=template_list+"<option value=\"";
                  template_list=template_list+templ_obj[""+x+""]["TempCont"];
                  template_list=template_list+"\" title=\"";
                  template_list=template_list+templ_obj[""+x+""]["TempCont"];;
                  template_list=template_list+"\">Template ";
                  template_list=template_list+template_counter;
                  template_list=template_list+"</option>";



              }


            break; //break the for loop since all templates for this category have been found
          
        }

     }
    
     $("#selecttemplate").html(template_list);





};

var viewSMSTemplates=function(){

//open a dialog
$("#smstemplatesdialog").dialog( "open" ); 

    jsonObject={};
    var templates_categories=new Array();
    var template_details;
    var distinct_categories_counter=0;
    
      var urlstr=site;
      urlstr=urlstr+"jsondata/RMSGT/";// Retrieve
      $.ajax({
             url: urlstr,
             dataType: "jsonp",
             method: "POST",
             data:JSON.stringify(jsonObject),
             cache: false
             })
            .done(function( templateobject ) {
             //clearInterval(display_interval);
             //$("#progresspopup").popup( "close"); // close the pop up for progress once the results are returned from the database
             //alert("Message Sent");
              if (Modernizr.localstorage) {
                        //store into a local storage
                        localStorage.removeItem("SMSTemplates");
                        localStorage.setItem("SMSTemplates",JSON.stringify(templateobject));
                        //alert(addressbookobj["AD00"]["birthdate"]);
                        //alert("Local Storage Supported");
                      }

                      for(var x in templateobject)
                    {
                        //var randstr=JSON.stringify(addressbookobj);
                        //obj=templateobject[""+x+""]["Templates"];
                        template_details=new Array(2);
                        template_details["CategoryID"]=templateobject[""+x+""]["ID"];
                        template_details["CategoryName"]=templateobject[""+x+""]["CN"];
                        if(distinct_categories_counter==0){
                         //we have encountered the first category id so put into the array
                         templates_categories[distinct_categories_counter]=template_details;
                      
                         distinct_categories_counter++;
                        }
                        else{
                            //The is atleast one element in the array

                            //first do insertion sort ensure the array is in ascending order
                            insertionSort(templates_categories);
                            
                             //alert(template_details["CategoryID"]);
                            //secondly use binary search to check if the new element to be appended in an array already exists. If it exists then we choose to ignore the category.
                            //This way we can know all unique categories that have templates
                            if(binarySearch(templates_categories,template_details["CategoryID"])>=0)
                            {
                            
                                continue;
                            }
                            else{

                                templates_categories[distinct_categories_counter]=template_details;
                               
                                
                            }
                        
                          distinct_categories_counter++;

                        }
                        //alert(templateobject[""+x+""]["ID"]);

                       /*for(var y in obj){
                          alert(""+y+"");
                         //alert(obj[""+y+""]["TempCont"]);

                        }*/
                    }

                  var selected_template_category="<option value=\"-1\" title=\"Select Template Category\">Select Template Category</option>";
                 for(var start=0;start<distinct_categories_counter;start++)
                   {
                      selected_template_category= selected_template_category+"<option value=\"";
                      selected_template_category=selected_template_category+templates_categories[start]["CategoryID"];
                      selected_template_category=selected_template_category+"\" title=\"";
                      selected_template_category=selected_template_category+templates_categories[start]["CategoryName"];
                      selected_template_category=selected_template_category+"\">";
                      selected_template_category=selected_template_category+templates_categories[start]["CategoryName"];
                      selected_template_category=selected_template_category+"</option>";
                      //alert(templates_categories[start]["CategoryName"]);


                    } 
            
                    $("#selecttemplatecategory").html(selected_template_category);

             });



//$('foo').dialog({dialogClass:'dialog_style1'});

};

//bind to either group or individual SMS


var openProfile=function(owner){
var position =  $(owner).position();

//$("#profiledialog").dialog("option", "position", [position.right, position.top]);
//$("#profiledialog").dialog("option", "position", [200, position.top]);

//$("#profiledialog").dialog('option', 'position', [x,y]);
$('#profiledialog').dialog("option", "position", {my: "right top", of: $(owner)});

$("#profiledialog" ).dialog( "open" );



};


var closeProfile=function(owner){


//$("#profiledialog" ).dialog("close");
      jsonObject={};


      var urlstr=site;
      urlstr=urlstr+"jsondata/LGT/";// 
      $.ajax({
             url: urlstr,
             dataType: "jsonp",
             method: "POST",
             data:JSON.stringify(jsonObject),
             cache: false
             })
            .done(function(obj) {
              if (Modernizr.localstorage)
                   
              //now clear local storage within the scope of this application
              localStorage.removeItem("Contacts");
              localStorage.removeItem("AllContacts");
              localStorage.removeItem("Groups");
              localStorage.removeItem("Campaigns");
              localStorage.removeItem("SMSTemplates");
                  

              
              window.location=site;
            
     
         
             });




};





var bindSMSBroadCaster=function(recipient_type,option1,option2){


var r_type=parseInt(recipient_type); // 1 is for individual SMS, 2 is for groupbinSMS
if(r_type==1)
 {
  $("#smsgeneralization").hide();
  $("#instantsmsbtn").unbind( "click" );

 $(".startsmspopup").unbind( "click" ); //unbind any previous event
  $(".startsmspopup").bind('click',function(){
   $("#smsdialog" ).dialog( "open" );
         
  });

  $("#instantsmsbtn").bind('click',function(){
    sendOneSMS();
       
  });
  $("#viewsmstemplatesbtn").bind('click');

}
else
{
  //simplesmscomposerid
  $("#smsgeneralization").show();
  global_group_id=option1;
  option2="'<i>"+option2+"</i>' group";
  $("#simplesmscomposerid").html(option2);
 
  $("#instantsmsbtn").unbind( "click" );

  $("#instantsmsbtn").bind('click',function(){
   sendGroupSMS(global_group_id);
     
  });
 $("#smsdialog" ).dialog( "open" ); 



}

  $("#viewsmstemplatesbtn").bind('click',function(){
    viewSMSTemplates();
       
  });


};
var contact_card_hidden=true;
var selected_address_item="";

//For retrieving individual address item from local storage
var retrieveAddressItem=function (item)
{
 
 selected_address_item=item;//We need this incase we refresh the address book to get back to where we were last time. Fo istance when searching the user may decide to clear te search box and that can triggger the address book to be refreshed. What if the was an item displayed on the contact card, the we have to retain it
 json_obj=JSON.parse(localStorage.getItem("Contacts"));
 
 for(var y in json_obj)
 {
  if(y==item)
   {

     var physical_address="";
     var phone_numbers="";
     var count_mobiles=0;
    //alert(json_obj[""+y+""]["first_name"]+" was clicked");
    var nameofcontact=json_obj[""+y+""]["first_name"];
    nameofcontact=nameofcontact+" ";
    nameofcontact=nameofcontact+json_obj[""+y+""]["last_name"]; 
    $("#nameofcontact_1" ).html(nameofcontact);
    $("#card-name" ).html(nameofcontact);

    physical_address=physical_address+json_obj[""+y+""]["ward"];
    physical_address=physical_address+", "+json_obj[""+y+""]["district"];
    physical_address=physical_address+",<br></br>\n "+json_obj[""+y+""]["region"];
    physical_address=physical_address+", "+json_obj[""+y+""]["country"];
    
    $("#physical-address" ).html(physical_address);
     $("#simplesmscomposerid" ).html(nameofcontact);
    
    var mobile_object=json_obj[""+y+""]["mobiles"];
    
    var total_no_mobiles=Object.keys(mobile_object).length;
    //incase we have more than one phone number we use a list to display them
    var list_item_open_tag="";
    var list_item_close_tag="";

    var ul_list_open_tag="";
    var ul_list_close_tag="";
    var marker_description="";
    if (total_no_mobiles>1)
     {
      //create a tag for unordered list of phone numbers
      ul_list_open_tag="\n<ul>";
      ul_list_close_tag="\n</ul>"
      list_item_open_tag="\n   <li>";
      list_item_close_tag="\n   </li>";
      marker_description="\n<p>[<span class=\"chargedescr\">*</span>] primary (for Bulky SMS)</p>\n";
      marker_description=marker_description+"<p>[<span class=\"chargedescr\">**</span>] others</p>\n";
      
      
      
   
     }

    phone_numbers=phone_numbers+ul_list_open_tag;
    for(var m in mobile_object)
    {
    
     phone_numbers=phone_numbers+list_item_open_tag+mobile_object[""+m+""];
     var mobile_no=mobile_object[""+m+""];
     
     if (count_mobiles==0)
        {
        phone_numbers=phone_numbers+"<span class=\"charge\">*</span>"+list_item_close_tag;
        //set the primary mobile number
        $("#primarymobile" ).attr( "value",mobile_no);
        
       
        }
     else
        phone_numbers=phone_numbers+"<span class=\"charge\">**</span>"+list_item_close_tag;
     count_mobiles=count_mobiles+1;
   


    }
    
    if(total_no_mobiles>0)
    {
     
     //append an option for sending sms 
    //ul_list_close_tag= ul_list_close_tag+"\n<br></br><a href=\"#popupaddressbooksms\" data-rel=\"popup\"><img id=\"startsmspopup\" src=\"http://localhost:8000/static/bulkysms/images/smsicon.jpg\"></a>";  

ul_list_close_tag= ul_list_close_tag+"\n<br></br><a href=\"#\" style=\"cursor:pointer;\" data-rel=\"popup\"><img class=\"startsmspopup\" src=\"http://localhost:8000/static/bulkysms/images/smsicon.jpg\"></a>";  

    }

    ul_list_close_tag= ul_list_close_tag+marker_description;
    phone_numbers=phone_numbers+ul_list_close_tag;
    $("#phone-numbers").html(phone_numbers);
    //alert(phone_numbers);
    
    //now check if contact card is hidden

    if(contact_card_hidden){
     $("#contact-card").show();
       contact_card_hidden=false;


    }
    break;

    }

 }

setTimeout(function(){
initiateSMSDialog('1');

},500);

};

//This box is for filtering contacts
var searchContacts=function(filterstr){

  
 json_obj=JSON.parse(localStorage.getItem("Contacts"));

 var contact_names = [];
 var name_counter=0;
 var address_objects=[];
 var current_alphabet=filterstr.charAt(0);
 var current_alphabet_id="#";
                      
            //Do twice because ids have two letters of the same alphabet
 current_alphabet_id=current_alphabet_id+current_alphabet;
 current_alphabet_id=current_alphabet_id+current_alphabet;

 for(var y in json_obj)
 {

    let first_name=json_obj[""+y+""]["first_name"];
    let last_name=json_obj[""+y+""]["last_name"];
    //Now lets create a regular expression that we can use to match the filtered string

    //put the OR part incase the user types only the firstname
    let reg_str="";
    let strchar="^\\s*";


    //Consider all strings that are part of the first name alone.
    
    for(var i=0;i<first_name.length;i++)
    {
        strchar=strchar+first_name[i];
        if(i>0)
        {
        reg_str=reg_str+"|";

        } 
        else
        {
         reg_str=reg_str+"";

        } 
       
        
         reg_str=reg_str+strchar;
         
         reg_str=reg_str+"\\s*$";
         //reg_str=reg_str+"$";

    }
    

    strchar=strchar+"\\s+";

    //Now Consider all strings that are part of the first name and last name .
    
    for(var i=0;i<last_name.length;i++)
    {


        strchar=strchar+last_name[i];
    
        reg_str=reg_str+"|";

        
      
        
         reg_str=reg_str+strchar;
         reg_str=reg_str+"\\s*$";

    }
    


    let pattern=new RegExp(reg_str,"i"); //We want the matching to be case insensitive


    let outcome = pattern.test(filterstr)

        
        if(outcome) //Check if true: Meaning if the searched string matches the pattern.
        {
        //then consider this contact name as one of the matches to be displayed in the address book 
           contact_names[name_counter]="";
           contact_names[name_counter]=contact_names[name_counter]+json_obj[""+y+""]["first_name"];
           contact_names[name_counter]=contact_names[name_counter]+ " ";
           contact_names[name_counter]=contact_names[name_counter]+json_obj[""+y+""]["last_name"];
           address_objects[name_counter]=""+y+"";
           name_counter++;
        }



    

  }

        var inner_html="";
        for(var j=0;j<name_counter;j++)
        {
           contact_name=contact_names[j].toUpperCase()
           var posn=contact_name.indexOf(current_alphabet.toUpperCase());
           if(posn==0){
              inner_html=inner_html+"\n<li onclick=\"retrieveAddressItem('";
              inner_html=inner_html+address_objects[j];
              inner_html=inner_html+"')\"";
              inner_html=inner_html+" style=\"cursor:pointer\"><a>";
              inner_html=inner_html+contact_names[j];
              inner_html=inner_html+"</a></li>\n";
              }
                         
                        
        }


                      
      $(current_alphabet_id).html(inner_html);


}

var filterAddressBookContent=function(group_id,option,keyword){
 

 var alpha_str="";
 var first_alphabet="a";
 var current_alphabet="";
 var last_alphabet="z";

 var filterContacts=$("#filterContacts").val();

 
   //for(var i = first_alphabet.charCodeAt(0); i <= last_alphabet.charCodeAt(0); i++)
 var posn=0

        //current_alphabet=( eval("String.fromCharCode(" + i + ")") );
        //first display only the characters that start with the first typed later of the key world
    if(filterContacts.length>0)
      {
        current_alphabet=filterContacts.charAt(posn);

        while((current_alphabet==" ")&&(posn<filterContacts.length)){
 
         
         current_alphabet=filterContacts.charAt(posn);

         if(current_alphabet!==" ")
            break; //break if we have found first alphabet.
         posn++;
        
        }
        if(posn==filterContacts.length)
           {
            
            //$("#addressbook_names").html('Error: Index not found!');
            //return;
            //clear what has been typed if it is preceded with white spaces
            $("#filterContacts").val("");
             $("#filterContacts").focus();//move focus at the begining
             return;

           }
        filterContacts=filterContacts.substring(posn,(filterContacts.length));
        
        alpha_str=alpha_str+"<li id='";
        alpha_str=alpha_str+current_alphabet;
        alpha_str=alpha_str+"' class=''>";
        alpha_str=alpha_str+"<a name='";
        alpha_str=alpha_str+current_alphabet;
        alpha_str=alpha_str+"' class='title'>";
        alpha_str=alpha_str+current_alphabet;
        alpha_str=alpha_str+"</a>\n";
        alpha_str=alpha_str+"     <ul id='";

        alpha_str=alpha_str+current_alphabet;
        alpha_str=alpha_str+current_alphabet;
        alpha_str=alpha_str+"'>\n";
        alpha_str=alpha_str+"           <li><a>&nbsp;</a></li>\n";
        alpha_str=alpha_str+"     </ul>"
        alpha_str=alpha_str+"</li>";
        
       $("#addressbook_names").html(alpha_str);
        searchContacts(filterContacts);

      }
      else{
        retrieveAddressBookTemplate();
        //alert(selected_address_item);
        if(selected_address_item=="");
        else
        {
          //it means there was an item being displayed on the contact card there fore we need to put it back after refreshing the address page
          setTimeout(function(){
          retrieveAddressItem(selected_address_item);

        },100);
       

          setTimeout(function(){

          $("#contact-card").show();
          contact_card_hidden=false;

          },200);
       

        }
        //hide the contact card
        //$("#contact-card").hide();
         //contact_card_hidden=true;


      }



       

   //Now append 
  

};

//Retrieve address Book from Django Python App via our defined REST API
var retrieveAddressBookContent=function (group_id,option)
{     
     
      var urlstr=site;
      urlstr=urlstr+"jsondata/RABC/";

      
      if (typeof option === 'undefined') {
       // the variable is not defined
        option="-1";
       }

      var jsonObjects={GroupID:group_id,Option:option};
     
      var request = $.ajax({
                            url:urlstr,
                            method: "POST",
                            data: JSON.stringify(jsonObjects),
                            dataType: "jsonp"
                    });
 
      request.done(function( addressbookobj ) {
                    //$( "#log" ).html( msg );
                  
                    var contact_names = [];
                    //var contact_ids = [];
                    var address_objects=[];
                    var name_counter=0;
                    if (Modernizr.localstorage) {
                        //store into a local storage
                        localStorage.removeItem("Contacts");
                        localStorage.setItem("Contacts",JSON.stringify(addressbookobj));
                        //alert(addressbookobj["AD00"]["birthdate"]);
                        //alert("Local Storage Supported");
                      }

                    //addressbookobj1=JSON.parse(localStorage.getItem("Contacts"))
                    for(var x in addressbookobj)
                    {
                        var randstr=JSON.stringify(addressbookobj);
                       
                        contact_names[name_counter]="";
                        contact_names[name_counter]=contact_names[name_counter]+addressbookobj[""+x+""]["first_name"];
                        contact_names[name_counter]=contact_names[name_counter]+ " ";
                        contact_names[name_counter]=contact_names[name_counter]+addressbookobj[""+x+""]["last_name"];
                        //contact_ids[name_counter]=addressbookobj[""+x+""]["ContactID"];
                        address_objects[name_counter]=""+x+"";
                        name_counter=name_counter+1;
                    }

                  //now iterate through the 26 alphabets and put names to their respective alphabetical groups when displaying
                  var first_alphabet="a";
                  var last_alphabet="z";

             
                  for(var i = first_alphabet.charCodeAt(0); i <= last_alphabet.charCodeAt(0); i++) {
	                     var current_alphabet=( eval("String.fromCharCode(" + i + ")") );
                     //now search all names that start with the current alphabet
                      var inner_html="";
                      for(var j=0;j<name_counter;j++)
                      {
                       contact_name=contact_names[j].toUpperCase()
                       var posn=contact_name.indexOf(current_alphabet.toUpperCase());
                       if(posn==0){
                        inner_html=inner_html+"\n<li onclick=\"retrieveAddressItem('";
                        inner_html=inner_html+address_objects[j];
                        inner_html=inner_html+"')\"";
                        inner_html=inner_html+" style=\"cursor:pointer\"><a>";
                        inner_html=inner_html+contact_names[j];
                        inner_html=inner_html+"</a></li>\n";
                        }
                       
                      
                      }
                      
                      if(inner_html.length>0) //Then it means we have atleast one name to append for names that start with the current alphabet
                      {
                       var current_alphabet_id="#";
                       //Do twice because ids have two letters of the same alphabet
                       current_alphabet_id=current_alphabet_id+current_alphabet;
                       current_alphabet_id=current_alphabet_id+current_alphabet;
                       $(current_alphabet_id).html(inner_html);


                      }

                  }
            
         



         var address_book_ready=$("#address_book_page").attr("id");
         //alert(address_book_ready);
         if (address_book_ready!=null)
         { 
          
          //setTimeout(function(){handleSliderNav();},10000);
          //alert("Got here");
          handleSliderNav();

         //setTimeout(function(){handleSliderNav();},10000);
         }
         else
          {

          setTimeout(function(){

		      handleSliderNav();


		},20);

           

          }







      }); 



  }

  var createSendAddressFileEvent=function(){

  $('#uploadaddressbtn').on('click', function() {
     var jsonObjects={GroupID:"Bobo"};
     
      var urlstr=site;
      urlstr=urlstr+"jsonupdate/UAF/";

        var request = $.ajax({
                            url:urlstr,
                            method: "POST",
                            data: new FormData($('#addressuploadfileform')[0]), // The form with the file inputs.
                            processData: false,
                            contentType: false,
                            //data: JSON.stringify(jsonObjects),
                             dataType: "jsonp"
                    });
 
      request.done(function( obj ) {
             alert(obj.status);

      });

        request.fail(function( obj) {
         alert("Fail");

      });


  });
  


};


var retrieveBalanceTemplate=function(){


      var urlstr=site;
      urlstr=urlstr+"jsondata/RBT/";// Retrieve Balance Template
      $.ajax({
             url: urlstr,
             cache: false
             })
            .done(function( html ) {
            $("#main-content" ).html('');
            $("#main-content" ).append(html);
             });



};

var viewBalance=function(){

$("#viewbalance").show();
$("#buycredits").hide();

};

var viewBalance=function(){

$("#viewbalance").show();
$("#buycredits").hide();

      jsonObject={BundleID:$("bundleid").val()};

   
      var urlstr=site;
      urlstr=urlstr+"jsondata/GB/";// get balance
      $.ajax({
             url: urlstr,
             dataType: "jsonp",
             method: "POST",
             data:JSON.stringify(jsonObject),
             cache: false
             })
            .done(function( result ) {
            
             //alert(result.message); 
              var html_str="";
              //alert("Credits Retrieved");
               for(var key in result){

                  html_str=html_str+'<div id="rcorners_acc_balance" align="center" valign="center">\n';
                  html_str=html_str+'<table>\n <tr>\n        <td><b><i>Bundle Name</i></b>: </td>\n         <td>'+result[""+key+""]["BundleName"]+'</td>\n  </tr>\n';
                  html_str=html_str+'<tr>\n        <td><b><i>Bundle Type</i></b>: </td>\n         <td>SMS</td>\n  </tr>\n';
                  html_str=html_str+'<tr>\n        <td><b><i>Balance</i></b>: </td>\n         <td>'+result[""+key+""]["Credits"]+'</td>\n  </tr>\n';
                  html_str=html_str+'<tr>\n        <td><b><i>Expiry Date</i></b>: </td>\n         <td>'+result[""+key+""]["ExpiryDate"]+'</td>\n  </tr>\n';

                       
                  html_str=html_str+" </table>\n</div>";
                  



              }
              
              $("#viewbalancecontent").html(html_str);


             });

};



var retrieveBundleDetails=function(bundle_id){

	bundleObj=JSON.parse(localStorage.getItem("Bundles"));
        var found=false;
	for(var key in bundleObj){
          
          if(bundleObj[""+key+""]["BundleID"]==bundle_id)
           {
            //We have found the bundle picked by user, now find its details
            $("#bundle_descr").html(bundleObj[""+key+""]["BundleDescr"]);
            $("#bundle_no_sms").html(bundleObj[""+key+""]["Units"]);
            $("#bundle_price").html(bundleObj[""+key+""]["BundlePrice"]);
            $("#bundle_days").html(bundleObj[""+key+""]["BundleValidityPeriod"]);
            
            found=true;
            break;


           }


	}
        if(found){
          $("#buystep1").unbind("click");//remove previous bind
           $("#buystep1").bind("click", function(event){
           
              choosePaymentMethod();

            })


         }
        else{
            $("#bundle_descr").html("");
            $("#bundle_no_sms").html("");
            $("#bundle_price").html("");
            $("#bundle_days").html("");
            $("#buystep1").unbind("click");//remove any existing bind to click
             $("#buystep1").bind("click",function(event){
              alert("You have to select a bundle first!!"); //You can't proceed to payments without selecting a valid bundle
             });


         }


};

var buyCredits=function(paymentmethod){

  var transnumber="1234";
  var receipt= "Bought using "+paymentmethod+" with Transaction Number "+transnumber;
  
     
      jsonObject={BundleID:parseInt($("#bundle_id").val()),TransReceipt:receipt};
   
   
      var urlstr=site;
      urlstr=urlstr+"jsonupdate/BYC/";// Buy Credits
      $.ajax({
             url: urlstr,
             dataType: "jsonp",
             method: "POST",
             data:JSON.stringify(jsonObject),
             cache: false
             })
            .done(function( result ) {

              alert(result.descr);
                  

             });



};


var prevloadBuyCreditCont="";
var prev_bundle_id;
var choosePaymentMethod=function()
{
prev_bundle_id=$("#bundle_options").val();

prevloadBuyCreditCont=$("#buycreditcontainer").html(); //store this content incase you want to go back to selecting which bundle to buy
var payment_methods_str="<table class='table-forms'>   \
                              <tr>  \
                                 <td><img src='/static/bulkysms/images/airtelmoney_logo.png' style='cursor:pointer' alt='Select Payment Method' id='airtel_pay'></td>\
                                 <td><img src='/static/bulkysms/images/mpesa_logo.png' style='cursor:pointer' alt='Select Payment Method' id='mpesa_pay' ></td>\
                                 <td><img src='/static/bulkysms/images/tigo_pesa_logo.png' style='cursor:pointer' alt='Select Payment Method' id='tigopesa_pay' ></td>\
                              </tr>  \
                             <tr><td colspan=3 align='center'><button type='button' class='btn btn-info' id='movebackstep1'>Previous</button></td></tr> \
                         </table> \
                         <input type=hidden id='bundle_id' value=";
     payment_methods_str=payment_methods_str+$("#bundle_options").val();
     payment_methods_str=payment_methods_str+">";




 $("#buycreditcontainer").html(payment_methods_str);

 $("#movebackstep1").unbind("click");//remove previous bind
  $("#movebackstep1").bind("click", function(event){
                         
    $("#buycreditcontainer").html(prevloadBuyCreditCont); 
    $("#movebackstep1").unbind("click");//remove previous bind 
    $("#airtel_pay").unbind("click");//remove previous bind
    $("#mpesa_pay").unbind("click");//remove previous bind
    $("#tigopesa_pay").unbind("click");//remove previous bind

  

    $('#bundle_options option[value='+prev_bundle_id+']').attr('selected','selected');
    prev_bundle_id=null; 

   //now unbind and bind pay button  

    $("#buystep1").unbind("click");//remove previous bind

     $("#buystep1").bind("click", function(event){
           
      choosePaymentMethod();

       });    

 });


 $("#airtel_pay").unbind("click");//remove previous bind
  $("#airtel_pay").bind("click", function(event){

   buyCredits("AIRTEL");
   });

 $("#mpesa_pay").unbind("click");//remove previous bind
  $("#mpesa_pay").bind("click", function(event){

   buyCredits("MPESA");
   });

 $("#tigopesa_pay").unbind("click");//remove previous bind
  $("#tigopesa_pay").bind("click", function(event){

   buyCredits("TIGOPESA");
   });





};


var loadBuyCredits=function(){
  $("#viewbalance").hide();
  $("#buycredits").show();
  


      var urlstr=site;
      urlstr=urlstr+"jsondata/RBO/";// Retrieve Bundle Options
      $.ajax({
             url: urlstr,
             dataType: "jsonp",
             method: "POST",
             data:JSON.stringify(jsonObject),
             cache: false
             })
            .done(function( bundleObj ) {
              
              if(bundleObj.BL00.BundleID<0)
                {

                  alert("There are no available bundles to buy");
                }
               else
                  {
                    
                      if (Modernizr.localstorage) {
                        //store into a local storage
                        localStorage.removeItem("Bundles");

                        localStorage.setItem("Bundles",JSON.stringify(bundleObj));
               

                      }
                      //next populate options with all available bundles
                      var select = $('#bundle_options');
                      $('option', select).remove();


                      $('#bundle_options')
                       	  .append($("<option id='select_bundle' name='select_bundle_name'></option>")
                          .attr("value",'0')
                          .text("Select a bundle to buy"));


                        //get all bundle ID and their names to be included in Bundle options
                        var newOptions={};
			for(var x in bundleObj)
			{
			  let bid=""+bundleObj[""+x+""]["BundleID"];
			  let bname=""+bundleObj[""+x+""]["BundleName"];
			  newOptions[""+bid]=bname;
			

			}


			$.each(newOptions, function(key, value) {
			      let option_str= "<option class='bundleoption' id='bid_";
			      option_str=option_str+key;
			      option_str=option_str+"'></option>";
			     $('#bundle_options')
				 .append($(option_str)
				 .attr("value",key)
				 .text(value));
			});
                         $("#buystep1").unbind("click");//remove any existing bind to click so tha
                          $("#buystep1").bind("click",function(event){
                            alert("You have to select a bundle first!!");
                        });


                         $("#bundle_options").unbind("change");//remove previous bind
                         $("#bundle_options").bind("change", function(event){
                         
                           var selected_bundle_id=$(this).val();
                           retrieveBundleDetails(selected_bundle_id);

                        });


                     //clear all previos content 

                              $("#bundle_descr").html("");
                             $("#bundle_no_sms").html("");
                            $("#bundle_price").html("");
                             $("#bundle_days").html("");

     





                  }//end of else statement



             });



};





var retrieveAddressBookTemplate=function ()
{     
     
      var urlstr=site;
      urlstr=urlstr+"jsondata/RABT/";// Retrieve
      $.ajax({
             url: urlstr,
             cache: false
             })
            .done(function( html ) {
            $("#main-content" ).html('');
            $("#main-content" ).append(html);
            $("#filterContacts").focus();



            
                           //$(document).ready(function () {
                           // Action after append is completly done
                           //Now work on the slider
                           //handleSliderNav();
                            //});

             retrieveAddressBookContent('-1');

             //attach events to on upload file box
             setTimeout(function(){


                     createSendAddressFileEvent();

                    $('#addressfile').on('change', function() {
                      let fileName=$('#addressfile').val();
                      let ext = fileName.split('.').pop();
                      let split_str=fileName.split('\\');
                      let split_str_len=split_str.length;
                      if(split_str_len>1){
                       //Just get the name without path name 
                      fileName=split_str[split_str_len-1];


                      }
                      if(ext!=="xls"){
                        alert("Wrong file with extension '"+ext+"'. Only files with '.xls' extension are allowed.");
                        $('#addressfile').val('');
                        $('#addfilename').html('<b>File</b>: No File');

                      }
                      else{
                      
                        $('#addfilename').html('<b>File</b>: '+fileName+'');


                      }
                     /*var file = this.files[0];
                      if (file.size > 1024) {
                          alert('max upload size is 1k')
                     }*/


                     });

                    },20);
 
             
             });




  };



var showAddressBook=function(){
$("#update_address").hide();
$("#view_address_book").show();
$("#view_search_contact").show();
$("#viewaddressbtn" ).prop( "disabled", true );
$("#updateaddressbtn" ).prop( "disabled", false);

$("#addressbookstatus").html("Viewing Address Book");



};


var updateAddressBook=function(){

$("#update_address").show();
$("#view_address_book").hide();
$("#view_search_contact").hide();
$("#viewaddressbtn" ).prop( "disabled", false);
$("#updateaddressbtn" ).prop( "disabled", true);
$("#addressbookstatus").html("Updating Address Book");

};


var downloadUpdateTemplate=function(){
     var urlstr=site;
    urlstr=urlstr+"jsondata/ADD/";
     window.open(urlstr);
      /*
      alert("Demo");
      var urlstr=site;
      urlstr=urlstr+"jsondata/ADD/";// Retrieve
      $.ajax({
             url: urlstr,
             cache: false
             })
            .done(function( html ) {
              
             });

            */

};



var downloadReminderTemplate=function(opid){
      var urlstr=site;
     //choose whether a template should contain existing data or not.
      var extra_json=""; //This is meant to be used to differentiate template that have existing reminders and templates that
     
      urlstr=urlstr+"jsondata/RDDN/";
 
      if(opid==1){
               var targeted_audience=null;
         var hidden_campaign_id= $("#hiddencampaignid").val();
       
        extra_json={Existing:1,CampaignID:hidden_campaign_id}; //if Existing is 1; the it means this campaign may have existing indidualized reminders

      }
      else{
           extra_json={Existing:0,CampaignID:-1};
         }

      serializedJson=JSON.stringify($("#campaigntargetsms").serializeArray());
      extra_json=JSON.stringify(extra_json);
    
      if(jQuery.isEmptyObject(serializedJson)) //Check if we have at least one target group for the individualized reminders.
     {
       alert("Can't download template. No target group was selected");
       return;

      }
    
 
     window.open(urlstr + '?jsonObj=' + serializedJson+'&extraJson='+extra_json);
    
};



//user interface for selecting members to assign
var assignMembersToGroupIAddressBookTenterface=function(group_id){



};


var saveGroupMembers=function(group_id){



};


var retrieveGroupAllocatioTemplate=function(){

      jsonObject={};
      var urlstr=site;
      urlstr=urlstr+"jsondata/RGAT/";// Retrieve Group Allocation Template
      $.ajax({
             url: urlstr,
             cache: false
             })
            .done(function(html) {
          
            $( "#main-content" ).html('');
            $( "#main-content" ).append(html);
            
            //alert(html);
               //Now append that interface
            
                           //$(document).ready(function () {
                           // Action after append is completly done
                           //Now work on the slider
                           //handleSliderNav();
                            //});
             //retrieveAllContacts();
         
             })
             .fail(function(html) {alert("Fail")});


};
var retrieveGroupMembers=function(group_id){

retrieveAllContacts(group_id);

};

var retrieveNonGroupMembers=function(group_id){

retrieveAllContacts('-1',group_id);//This means we retrieve all contacts, excluding all members of the group
setTimeout(function(){

$('#groupandmembers').DataTable();

},500);

};


var addGroupMember=function(contact_id,group_id){

      jsonObject={ContactID:contact_id,GroupID:group_id};

   
      var urlstr=site;
      urlstr=urlstr+"jsonupdate/AGM/";// Add Group Member
      $.ajax({
             url: urlstr,
             dataType: "jsonp",
             method: "POST",
             data:JSON.stringify(jsonObject),
             cache: false
             })
            .done(function( result ) {
            
             //alert(result.message); 

             $("#allcontacts").html('');
              
             retrieveGroupAllocatioTemplate();
             setupGroupAllocationInterface(2); 


             });



};


var removeGroupMember=function(contact_id,group_id){

        jsonObject={ContactID:contact_id,GroupID:group_id};

   
      var urlstr=site;
      urlstr=urlstr+"jsonupdate/RGM/";// Remove Group Member
      $.ajax({
             url: urlstr,
             dataType: "jsonp",
             method: "POST",
             data:JSON.stringify(jsonObject),
             cache: false
             })
            .done(function( result ) {
            
              //alert(result.message);

              $("#allcontacts").html('');
             retrieveGroupAllocatioTemplate();
             setupGroupAllocationInterface(1);
    
              

             });



};

var retrieveAllContacts=function(group_id,option){

      var urlstr=site;
      urlstr=urlstr+"jsondata/RABC/";

      
      var html_str="";
      if (typeof option === 'undefined') {
    // the variable is not defined
       option=-1;
       }
      //alert("GID="+group_id+" and Option="+option);
      var jsonObjects={GroupID:group_id,Option:option};
      var request = $.ajax({
                            url:urlstr,
                            method: "POST",
                            data: JSON.stringify(jsonObjects),
                            dataType: "jsonp"
                    });
 
      request.done(function(contactsobj ) {
                    
                  
                    $("#allcontacts").html('');     
                  
                    var contacts_counter=0;
                    if (Modernizr.localstorage) {
                        //store into a local storage
                        localStorage.removeItem("AllContacts");

                        localStorage.setItem("AllContacts",JSON.stringify(contactsobj));
                       

                      }


                       if(contactsobj["AD00"]["ContactID"]==-1){
                           contact_ids_found=0;
                          
                             
                        }
                        else
                        {
                          contact_ids_found=1;
                          

                        }


                    
                       for(var x in contactsobj)
                       {
                         
                        if(!contact_ids_found)
                              break;  
                           
                       
                        var contact_names="";
                        var contact_ward="";
                        var contact_district="";

                        var contact_region="";
                        var contact_country="";


                        //Get name
                        contact_names=contact_names+contactsobj[""+x+""]["first_name"];
                        contact_names=contact_names+ " ";
                        contact_names=contact_names+contactsobj[""+x+""]["last_name"];
                       

                        //get ward
                         contact_ward=contact_ward+contactsobj[""+x+""]["ward"];

                        //get district

                         contact_district=contact_district+contactsobj[""+x+""]["district"];

                        //get region

                         contact_region=contact_region+contactsobj[""+x+""]["region"];


                         //get country
                         contact_country=contact_country+contactsobj[""+x+""]["country"];

                     
                         
           
                         html_str=html_str+"\n<tr>\n";
                         if(group_id==-1){
                         html_str=html_str+"    <td style=\"text-align:center;\">";
                         html_str=html_str+"         <i class=\"fa fa-plus\" style=\"font-size:20px;color:blue;cursor:pointer\" onclick=addGroupMember('";
                         html_str=html_str+contactsobj[""+x+""]["ContactID"];
                         html_str=html_str+"','";
                         html_str=html_str+global_group_id;
                         html_str=html_str+"')></i>";

                        html_str=html_str+"    </td>\n";
                         //

                         }
                         else{

                         html_str=html_str+"    <td style=\"text-align:center;\">";
                         html_str=html_str+"         <i class=\"fa fa-minus\" style=\"font-size:20px;color:blue;cursor:pointer\" onclick=removeGroupMember('";
                         html_str=html_str+contactsobj[""+x+""]["ContactID"];
                         html_str=html_str+"','";
                         html_str=html_str+global_group_id;
                         html_str=html_str+"')></i>";
                         html_str=html_str+"    </td>\n";


                         }


                         html_str=html_str+"    <td>";
                         html_str=html_str+contact_names;

                         html_str=html_str+"    </td>\n";


                         html_str=html_str+"    <td>\n";
                         html_str=html_str+contact_ward;
                         html_str=html_str+"    </td>\n";


                         html_str=html_str+"    <td>\n";
                         html_str=html_str+contact_district;
                         html_str=html_str+"    </td>\n";

          
                         html_str=html_str+"    <td>\n";
                         html_str=html_str+contact_region;
                         html_str=html_str+"    </td>\n";

                         html_str=html_str+"    <td>\n";
                         html_str=html_str+contact_country;
                         html_str=html_str+"    </td>\n";
                         
                         if(group_id==-1){


                         //html_str=html_str+"    <td>\n";
                         //html_str=html_str+contact_country;
                         //html_str=html_str+"    </td>\n";

                           

                         }
                         

                         html_str=html_str+"\n</tr>\n";
                         

                       

                         
                        }
                   //(html_str);
                       $("#allcontacts").html(html_str);

             });

  

};

var saveGroup=function(group_id,menu_id,save_type){

 var record_id=menu_id+"";
 record_id=record_id+group_id;
 if(save_type=='1')
      jsonObject={GroupID:group_id,GroupName:$("#group_name").val(),GroupDescr:$("#group_descr").val()};
else
    jsonObject={GroupID:group_id,GroupName:$("#group_name_edit").val(),GroupDescr:$("#group_descr_edit").val()};

   
      var urlstr=site;
      urlstr=urlstr+"jsonupdate/SGD/";// Retrieve
      $.ajax({
             url: urlstr,
             dataType: "jsonp",
             method: "POST",
             data:JSON.stringify(jsonObject),
             cache: false
             })
            .done(function( result ) {
             //clearInterval(display_interval);
             //$("#progresspopup").popup( "close"); // close the pop up for progress once the results are returned from the database
              //alert(result["message"]);

            
             

             });





 
 


setTimeout(function(){

displayGroupsContent(VIEWING_MODE);


},10);

if(save_type=="0"){
    //alert("I am here");
                //retain the previous search
                setTimeout(function(){
                searchGroupTable();



},200);

}

//Now retrieve group content for editing
current_menu=record_id;

};

var editGroup=function(group_id,menu_id){

 var record_id=menu_id+"";
 record_id=record_id+group_id;
 
//now call a function to save records

displayGroupsContent(EDITING_MODE,group_id);


setTimeout(function(){
           searchGroupTable();
          },100);
//Now retrieve group content for editing


};


var deleteGroup=function(group_id,menu_id){
 var record_id=menu_id+"";
 record_id=record_id+group_id;
 //if(current_menu==record_id)
  //   return;
//alert("Delete Group.."+group_id);
current_menu=record_id;

};

var setupGroupAllocationInterface=function(interface_choice)
{

    if(interface_choice==1){

      setTimeout(function(){

        retrieveGroupMembers(global_group_id);
        var members_str="<h3>Members of '<i>"+global_group_name+"</i>' group</h3>";
        $("#group_members_header").html(members_str);

        $('#groupandmembers').DataTable().destroy();//
        setTimeout(function(){
            $('#groupandmembers').DataTable();

            },20);



      },20);

    }
    else
    { 
      if(interface_choice==2){

      setTimeout(function(){

        retrieveNonGroupMembers(global_group_id);
        var members_str="<h3>Contacts not in '<i>"+global_group_name+"</i>' group</h3>";
        $("#group_members_header").html(members_str);

        $('#groupandmembers').DataTable().destroy();//

         setTimeout(function(){
            $('#groupandmembers').DataTable();

            },20);



      },20);

       
        }
        else
            setTimeout(function(){retrieveGroupMembers(global_group_id);},20);



    }
       
   
    setTimeout(function(){

   // $('#groupandmembers').DataTable();

   /* var members_str="<h3>Members of '<i>"+global_group_name+"</i>' group</h3>";
    $("#group_members_header").html(members_str);*/

    },20);
    

    //add click event handler for viewing current members
    setTimeout(function(){
    $("#groupmembers").unbind("click");
    $("#groupmembers").bind("click", function(event){

    retrieveGroupMembers(global_group_id);
    $('#groupandmembers').DataTable().destroy();//destroy the old data table

    var members_str="<h3>Members of '<i>"+global_group_name+"</i>' group</h3>";
    $("#group_members_header").html(members_str);
    setTimeout(function(){
    $('#groupandmembers').DataTable();

    },20);
    });


    },20);


    //add click event handler for viewing non members. This is important when adding new members to a group
    setTimeout(function(){
    $("#newmembership").unbind("click");
    $("#newmembership").bind("click", function(event){

    retrieveNonGroupMembers(global_group_id);
    //alert("Gote gete");
    $('#groupandmembers').DataTable().destroy(); //destroy the old data table
    var members_str="<h3>Contacts not in '<i>"+global_group_name+"</i>' group</h3>";
    $("#group_members_header").html(members_str);
    setTimeout(function(){
    $('#groupandmembers').DataTable();

    },20);

    });




    },20);
    




};


var expandGroup=function(group_id,menu_id,group_name){
 

 var record_id=menu_id+"";
 record_id=record_id+group_id;
 if(current_menu==record_id)
     return;
 global_group_id=group_id;
 global_group_name=group_name;

retrieveGroupAllocatioTemplate();

setupGroupAllocationInterface(1);
//$.noConflict();
current_menu=record_id;


};


var checkGroupsForCampaign=function(){


groupsobj=localStorage.getItem("Groups");

if(groupsobj==undefined)
{
  retrieveGroupsContent();
  groupsobj=localStorage.getItem("Groups");


  if(groupsobj==undefined) //
      alert("Failed to retrieve groups hence can't proceed ");
       return -1;



}




return 1;



};

//Retrieve Content for groups
var retrieveGroupsContent=function ()
{     
     
     jsonObject={Empty:""};
     
      var urlstr=site;
      urlstr=urlstr+"jsondata/RGC/";// Retrieve Group Content
      $.ajax({
             url: urlstr,
             dataType: "jsonp",
             method: "POST",
             data:JSON.stringify(jsonObject),
             cache: false
             })
            .done(function( resjson ) {
               

              //return resjson;
              if (Modernizr.localstorage) {
                        //store into a local storage
                        localStorage.removeItem("Groups");
                        localStorage.setItem("Groups",JSON.stringify(resjson));
                        //alert("Local Storage Supported");
                      }



                

                   

          

             });



  };

 var displayGroupsContent=function(display_type,group_id){
  //display type, 1 -- Viewing Mode,  2 -- Editing Mode
  //group_id is NULL in Viewing Mode
 
  retrieveGroupsContent();
  setTimeout(function(){

  //alert("Group Content Loaded"+resjson["AD00"]["group_description"]);
                    //var contact_ids = [];
                    var group_objects=[];
                    var group_counter=0;
                    var html_str="\n";
                    
              
                    var resjson=JSON.parse(localStorage.getItem("Groups"));
                    //alert("Group Content Loaded"+resjson["AD00"]["group_description"]);
                    for(var x in resjson)
                    {
                        if(resjson.AD00<0)
                         {
                          break;

                         }
                        var retrieved_group_id=resjson[""+x+""]["GroupID"];
                        
                        var retrieved_group_name="";
                        var retrieved_group_descr="";
                        var no_members=0;




                        //deciding on displaying mode whether the content should be viewing in editing mode or just normal viewing mode
                        if((display_type==EDITING_MODE)&&(group_id==retrieved_group_id)){
                         //alert("Got here");
                          // this is editing mode so it should be viewed in text box ready for editing
                           retrieved_group_name="<input type=\"text\" value=\""+resjson[""+x+""]["GroupName"]+"\" id=\"group_name_edit\" maxlength=\"50\">" ;
                          //retrieved_group_descr=resjson[""+x+""]["group_description"]; 
                          retrieved_group_descr="<textarea id=\"group_descr_edit\"  rows=\"5\" cols=\"20\" maxlength=\"200\">"+resjson[""+x+""]["group_description"]+"</textarea>" ;



                        }
                        else{
                          retrieved_group_name=resjson[""+x+""]["GroupName"];  ;
                          retrieved_group_descr=resjson[""+x+""]["group_description"];  
                          no_members=resjson[""+x+""]["NumMembers"]; 

                        }

                        //retrieved_group_name=resjson[""+x+""]["group_name"];  ;
                        //retrieved_group_descr=resjson[""+x+""]["group_description"];  


                        html_str=html_str+"<tr>\n";

                        html_str=html_str+"\n  <td>";


                        html_str=html_str+retrieved_group_name;
                   
                        html_str=html_str+"\n  </td>";

                        //var long_str=resjson[""+x+""]["group_description"];

                        //now divide the string into 

                        //var n = long_str.length; 
                        
                        
                        html_str=html_str+"\n  <td style=\"overflow:hidden; width:200px;\">"
                        html_str=html_str+retrieved_group_descr;
                        html_str=html_str+"\n  </td>";

                        html_str=html_str+"\n  <td align='center'>"
                        html_str=html_str+no_members;
                        html_str=html_str+"\n  </td>";



                        if((display_type==EDITING_MODE)&&(group_id==retrieved_group_id)){



                        html_str=html_str+"\n <td class=\"iconbuttons\">";

              
                    
                        html_str=html_str+"\n   <a href=\"#\" class=\"btn btn-info btn-lg\" style=\"font-size:15px;color:white;background-color:5bc0de;\" onclick=\"saveGroup('";
                        html_str=html_str+resjson[""+x+""]["GroupID"];
                        html_str=html_str+"','SAVEGROUPEDIT','0')\"><span class=\"glyphicon glyphicon-ok\">Save</span></a>";
                        html_str=html_str+"\n   </td>";

                     

                        //html_str=html_str+"\n</tr>\n";


                       }
                       else
                        {



                        html_str=html_str+"\n <td class=\"iconbuttons\">";

                        html_str=html_str+"\n   <br><button style=\"font-size:24px;color:orange;\" title=\"Send SMS to this group\" onclick=\"initiateSMSDialog('2','";
                        html_str=html_str+resjson[""+x+""]["GroupID"];
                        html_str=html_str+"','";
                        html_str=html_str+resjson[""+x+""]["GroupName"];
                        html_str=html_str+"')\"><i class=\"glyphicon glyphicon-envelope\"></i></button>"; 

                        html_str=html_str+"\n   <button style=\"font-size:24px;color:blue\" title=\"Edit this group\" onclick=\"editGroup('";
                        html_str=html_str+resjson[""+x+""]["GroupID"];
                        html_str=html_str+"','EDITGROUP')\"><i class=\"fa fa-pencil\"></i></button>";


                        html_str=html_str+"\n   <button style=\"font-size:24px;color:red;\" title=\"Delete this group\" onclick=\"deleteGroup('";
                        html_str=html_str+resjson[""+x+""]["GroupID"];
                        html_str=html_str+"','DELETEGROUP')\"><i class=\"fa fa-trash-o\"></i></button>";
                    
                        html_str=html_str+"\n   <button style=\"font-size:24px;color:green;\" title=\"Edit Group Members\" onclick=\"expandGroup('";
                        html_str=html_str+resjson[""+x+""]["GroupID"];
                        html_str=html_str+"','EXPANDGROUP','";
                        html_str=html_str+resjson[""+x+""]["GroupName"];
                        html_str=html_str+"')\"><i class=\"glyphicon glyphicon-expand\"></i></button>";
                        html_str=html_str+"\n   </td>";

                     
                        //html_str=html_str+"\n</tr>\n";
                        }

                       html_str=html_str+"\n</tr>\n";
                    
                        //group_objects[group_counter]=""+x+"";
                        //group_counter=group_counter+1;
                    }
                   // alert(html_str);
                   //alert(html_str);
                   $("#groups").html(html_str);




  },100);

  





 };


 


 //Retrieve Template for settings
var retrieveSettingsTemplate=function ()
{     
     
      var urlstr=site;
      urlstr=urlstr+"jsondata/RSTT/";// Retrieve
      $.ajax({
             url: urlstr,
             cache: false
             })
            .done(function( html ) {
            //$( "#main-content" ).html( html );
              //handleSliderNav();
              //alert("Done");
             $("#main-content").html(html);
            //retrieveAddressBookContent();
             });



  };//end of retrieveAddressBookTemplate 

//Retrieve Template for groups
var retrieveGroupsTemplate=function ()
{     
     
      var urlstr=site;
      urlstr=urlstr+"jsondata/RGT/";// Retrieve
      $.ajax({
             url: urlstr,
             cache: false
             })
            .done(function( html ) {
            //$( "#main-content" ).html( html );
              //handleSliderNav();
              //alert("Done");
             $("#main-content").html(html);
            //retrieveAddressBookContent();
             });



  };//end of retrieveAddressBookTemplate 

//Display campaigns

//Retrieve Content for campaigns
var retrieveCampaignsContent=function ()
{     
     
     jsonObject={Empty:""};
     
      var urlstr=site;
      urlstr=urlstr+"jsondata/RCC/";// Retrieve Campaign Content
      $.ajax({
             url: urlstr,
             dataType: "jsonp",
             method: "POST",
             data:JSON.stringify(jsonObject),
             cache: false
             })
            .done(function( resjson ) {
               //alert(resjson.AD00.messagestxt.MTXT00);

              //return resjson;
              if (Modernizr.localstorage) {
                        //store into a local storage
                        localStorage.removeItem("Campaigns");
                        localStorage.setItem("Campaigns",JSON.stringify(resjson));
                        //alert("Local Storage Supported");
                      }

                

                   

          

             });





  };


var chartData;
var report_displayed;
var createPieChart=function(){


	var chart = new CanvasJS.Chart("chartContainer", {
		theme: "white",
		exportFileName: "Doughnut Chart",
		exportEnabled: true,
		animationEnabled: true,
		title:{
			text: report_displayed
		},
		legend:{
			cursor: "pointer",
			itemclick: explodePie
		},
		data: [{
			type: "doughnut",
			innerRadius: 90,
			showInLegend: true,
			toolTipContent: "<b>{name}</b>: No of messages: {y} (#percent%)",
			indexLabel: "{name} - #percent%",
			dataPoints: chartData
		}]
	});

//now render chart


	chart.render();




	function explodePie (e) {
		if(typeof (e.dataSeries.dataPoints[e.dataPointIndex].exploded) === "undefined" || !e.dataSeries.dataPoints[e.dataPointIndex].exploded) {
			e.dataSeries.dataPoints[e.dataPointIndex].exploded = true;
		} else {
			e.dataSeries.dataPoints[e.dataPointIndex].exploded = false;
		}
		e.chart.render();
	}



};


var createBarChart=function(){

var chart = new CanvasJS.Chart("chartContainer", {
	animationEnabled: true,
	theme: "light2", // "light1", "light2", "dark1", "dark2"
	title: {
		text: report_displayed
	},
	subtitles: [{
		text: "In Number of Messages Sent",
		fontSize: 16
	}],
	axisY: {
		prefix: ""
		/*scaleBreaks: {
			customBreaks: [{
				startValue: 10000,
				endValue: 35000
			}]
		}*/
	},
	data: [{
		type: "column",
		//yValueFormatString: "$#,##0.00",
		dataPoints: chartData
	}]
});
chart.render();


};

var createLineChart= function () {

var chart = new CanvasJS.Chart("chartContainer", {
	animationEnabled: true,
        theme: "light3",
	title:{
		text: report_displayed
	},
	axisX:{
		valueFormatString: "DD MMM",
                crosshair: {
			enabled: true,
			snapToDataPoint: true
		 }
	},
	axisY: {
		title: "Number of Messages",
		includeZero: false
	},
	data: [{
		type: "area",
		xValueFormatString: "DD MMM",
		//color: "orange2",
		dataPoints: chartData
	}]
});
chart.render();

}

var getTodayDate=function(){
var today = new Date();
var dd = today.getDate();
var mm = today.getMonth() + 1; //January is 0!

var yyyy = today.getFullYear();
if (dd < 10) {
  dd = '0' + dd;
} 
if (mm < 10) {
  mm = '0' + mm;
} 
var today = yyyy  + '-' + mm + '-' + dd;
return today;

};


//begining of a month
var getFirstDateCurrentMonth=function(){
var today = new Date();
var dd = '01';
var mm = today.getMonth() + 1; //January is 0!

var yyyy = today.getFullYear();

if (mm < 10) {
  mm = '0' + mm;
} 
var first_day_of_month_date = yyyy  + '-' + mm + '-' + dd;
return first_day_of_month_date;

};


var getFirstDateCurrentWeek=function(){

  var d = new Date();
  var n = d.getDay();//get day of a week
 

  d.setDate(d.getDate() - n);//subtract to get the date of the first day of a week

 var dd = d.getDate();

 var mm = d.getMonth() + 1; //January is 0!

 var yyyy = d.getFullYear();
 if (dd < 10) {
  dd = '0' + dd;
} 
if (mm < 10) {
  mm = '0' + mm;
} 
var first_week_day = yyyy  + '-' + mm + '-' + dd;

return first_week_day;

};


var content_type;
var displayDashboard=function(type)
{
content_type=type;
//alert("startContentDownloading");
//Make sure you get all campaigns
retrieveCampaignsContent();

$("#chartContainer").html('');//clear the container
//Make sure you get groups

retrieveGroupsContent();
 
addLoadingCircleChart();
$(".progressboxchart").show();
//alert("Content ready") ;       
//delay execution of this 
setTimeout(function(){


        $(".progressboxchart").hide();
        removeLoadingCircleChart();
	var resmessages=JSON.parse(localStorage.getItem("AllMessages"));

	var rescampaigns=JSON.parse(localStorage.getItem("Campaigns"));

	var resgroups=JSON.parse(localStorage.getItem("Groups"));
	var data_array=new Array()
	var array_items_counter=0;
	var array_posn=0;
        var checked_not_group_nor_campaign=true;//for keeping track the number of outside iterations for group or campaign
        var message_counter=0;
        var not_for_group_or_camp_counter=0;
	//var array_pos_init=false; //This checks if the counter for a campaign has already 


                var interval_choice=$('input[name=visualizationinterval]:checked').val(); //important in knowing the dates to be used in filtering
                 var chart_type=$('input[name=visualizationtype]:checked').val();
                var start_date,end_date;

                switch(interval_choice)
                {
                 case "Today":start_date=getTodayDate();end_date=start_date;break;
                 case "ThisWeek":start_date=getFirstDateCurrentWeek();end_date=getTodayDate();break;
                 case "ThisMonth":start_date=getFirstDateCurrentMonth();end_date=getTodayDate();break;
                 case "Specify":start_date=$("#hidden_dashboard_date_picker_1").val();end_date=$("#hidden_dashboard_date_picker_2").val();break;
                 default:alert("The Interval you have specified is invalid");return;



               }
                if((start_date=="")||(end_date=="")||(start_date==undefined)||(end_date==undefined))
                {
                  alert("Error: No dates specified!!");
                  return;

                 }
               var dd1=new Date(start_date);
               var dd2=new Date(end_date);
               if(dd1.getTime()>dd2.getTime()){

                 alert("Invalid Date: The Start Date has to be before The End Date");
                 return;




                }
                  

                if(type=="Trend")
                {
                 var dates_array=new Array();
                 var date_counter=0;
                 var date1=new Date(start_date)
                 var date2=new Date(end_date)
                 while(true){
		         

		         if(date1.getTime()>date2.getTime())
		         {
		          break; //stop the loop

		         }
                         
                         //now iterate through all messages to count the number of times date 1 appears. That is the number of messages sent on date1
                         date_messages_counter=0;
                         for(var y in resmessages){
		                 
		         
		                 message_scheduled_date=new Date(resmessages[""+y+""]["ScheduledDate"]);
                                 //console.log(date1+"--"+message_scheduled_date)
                                 if(date1.getTime()==message_scheduled_date.getTime())
                                  {//count a message.
                                   date_messages_counter++;
                                   message_counter++;
                                   
                                  }
                                

                          }
                         
                         jsonObj={x:new Date(date1),y:date_messages_counter};
                         data_array[array_posn]=jsonObj; 
                         array_posn++;
		         
		         date1.setDate(date1.getDate()+1);//add one day to date
		         
                 

                 }//end of while loop

                 //now iterate through dates array
                   d1=new Date(start_date);
                   d2=new Date(end_date);

                   report_displayed="General Trend for Messages: Total="+message_counter+". From "+(d1.getDate()<10? "0"+d1.getDate():d1.getDate())+"-"+(d1.getMonth()+1)+"-"+d1.getFullYear()+" To "+(d2.getDate()<10? "0"+d2.getDate():d2.getDate())+"-"+(d2.getMonth()+1)+"-"+d2.getFullYear(); 
                   //console.log(data_array[8]["x"]);
                   chartData=data_array;
                   
                   createLineChart();
                
                  
                 

                }
               
		else if(type=="Campaigns")
		{
                   d1=new Date(start_date);
                   d2=new Date(end_date);

                 
		   
                          report_displayed="Campaigns : Total=";
			  for(var x in rescampaigns){
		            
		           array_items_counter=0; 
                              
		            var campaign_name=rescampaigns[""+x+""]["CampaignName"];
		            // now count the number messages in this campaign. If there are no messages ignore it
		              for(var y in resmessages){
		                 
		                 message_camp_name=resmessages[""+y+""]["CampaignName"];
		                 message_scheduled_date=resmessages[""+y+""]["ScheduledDate"];
		                 if((campaign_name==message_camp_name)&&(message_scheduled_date>=start_date)&&(message_scheduled_date<=end_date))
		                   {
		                    array_items_counter++;
                                    message_counter++;

		                   }
                                    else
                                      {
                                         if ((message_camp_name=="Not for Campaign")&&(message_scheduled_date>=start_date)&&(message_scheduled_date<=end_date)&&(checked_not_group_nor_campaign))//We only check in the first round. When moving to the next campaign in the out loop we don't check again. Also ensure it with specified date range
                                           {
                                           
                                             not_for_group_or_camp_counter++;
                                             message_counter++;
                                      

                                           }



                                      }
                                  

		                } //end inner for loop
		                if(array_items_counter>0)
		                {
		                  //then this campaign has some messages

                                  //now
                                  if(chart_type=="piechart")
		                      jsonObj={ y: array_items_counter, name: campaign_name};
                                  else if(chart_type=="barchart") 
                                       jsonObj={label: campaign_name, y: array_items_counter};
                                  else
                                      jsonObj={ y: array_items_counter, name: campaign_name};
		                  data_array[array_posn]=jsonObj;//here we are initializing data to be used during plotting
		                  
		                  array_posn++; //increment position by one
		                  
		                }
                                checked_not_group_nor_campaign=false; //Check only once for messages not belonging to campaign
	                   

			 }//end outer for loop


                         //Now check not for campaign and if it exists add to the array
                         if(not_for_group_or_camp_counter>0)
                           {
                                  
                                  if(chart_type=="piechart")
                                        jsonObj={ y: not_for_group_or_camp_counter, name:"Messages not belonging to Campaigns"};
                                  else if(chart_type=="barchart") 
                                         jsonObj={label:"Non-Campaign Messages", y: not_for_group_or_camp_counter};
                                  else
                                       jsonObj={ y: not_for_group_or_camp_counter, name:"Messages not belonging to Campaigns"};

		                  data_array[array_posn]=jsonObj;//here we are initializing data to be used during plotting
                              array_posn++;

                           }

		     //now check possibility of plotting if we have at some data

		       if(array_posn>=1){
                           report_displayed=report_displayed+message_counter+". From "+(d1.getDate()<10? "0"+d1.getDate():d1.getDate())+"-"+(d1.getMonth()+1)+"-"+d1.getFullYear()+" To "+(d2.getDate()<10? "0"+d2.getDate():d2.getDate())+"-"+(d2.getMonth()+1)+"-"+d2.getFullYear();


		         chartData=data_array;
		        

		         if(chart_type=="piechart")
                             createPieChart();
                         else if(chart_type=="barchart")
                            createBarChart();
                         else
                            createPieChart();
		         

		       }
                       else
                          {
                           $("#chartContainer").html("<h1 style='color:#4588cc;'>No data to be visualized in the specified period:"+(d1.getDate()<10? "0"+d1.getDate():d1.getDate()) +"-"+(d1.getMonth()+1)+"-"+d1.getFullYear()+" <i>to</i> "+(d2.getDate()<10? "0"+d2.getDate():d2.getDate())+"-"+(d2.getMonth()+1)+"-"+d2.getFullYear() +"</h1>");

                          }

                
		}//end if statement for checking if type is campaign
		else if(type=="Groups"){


                   d1=new Date(start_date);
                   d2=new Date(end_date);

                 
		   
                          

		       report_displayed="Groups: Total=";
			  for(var x in resgroups){
		            
		           array_items_counter=0;    
		            var group_name=resgroups[""+x+""]["GroupName"];
		            // now count the number messages in this campaign. If there are no messages ignore it
		              for(var y in resmessages){
		                 
		                 message_group_name=resmessages[""+y+""]["GroupName"];
                                 //console.log(message_group_name);
                                 message_scheduled_date=resmessages[""+y+""]["ScheduledDate"];
		                 
		                 if((group_name==message_group_name)&&(message_scheduled_date>=start_date)&&(message_scheduled_date<=end_date))
		                   {
		                    array_items_counter++;
                                      //console.log("Scheduled: "+message_scheduled_date+". Start: "+start_date+". End: "+end_date);
                                    message_counter++;

		                   }
                                    else
                                      {
                                         if ((message_group_name=="Not for Group")&&(message_scheduled_date>=start_date)&&(message_scheduled_date<=end_date)&&(checked_not_group_nor_campaign))//We only check in the first round. When moving to the next campaign in the out loop we don't check again
                                           {
                                             not_for_group_or_camp_counter++;
                                             //console.log("Scheduled: "+message_scheduled_date+". Start: "+start_date+". End: "+end_date);
                                             message_counter++;

                                           }



                                      }
                                  

		                } //end inner for loop
		                if(array_items_counter>0)
		                {
		                  //then this campaign has some messages
                                  if(chart_type=="piechart")
		                        jsonObj={ y: array_items_counter, name: group_name};
                                  else if(chart_type=="barchart")
                                        jsonObj={ label: group_name,y: array_items_counter};
                                  else
                                        jsonObj={ y: array_items_counter, name: group_name};
		                  data_array[array_posn]=jsonObj;//here we are initializing data to be used during plotting

                                  
		                  //console.log(""+campaign_name+""+array_posn);
		                  array_posn++; //increment position by one

                                   //Now check not for group but only once
		                  
		                }
                                checked_not_group_nor_campaign=false; //check only once for messages not belonging to any group
	                  

			 }//end outer for loop

                         //Now check not for group and if it exists add to the array
                         if(not_for_group_or_camp_counter>0)
                           {      if(chart_type=="piechart")
                                       jsonObj={ y: not_for_group_or_camp_counter, name:"Messages not belonging to groups"};
                                  else if(chart_type=="barchart")
                                        jsonObj={label :"Non-Group Messages", y: not_for_group_or_camp_counter};
                                  else
                                        jsonObj={ y: not_for_group_or_camp_counter, name:"Messages not belonging to groups"};
		                  data_array[array_posn]=jsonObj;//here we are initializing data to be used during plotting
                            array_posn++;

                           }

		     //now check possibility of plotting if we have at least one campaign

		       if(array_posn>=1){
                          report_displayed=report_displayed+message_counter+". From "+(d1.getDate()<10? "0"+d1.getDate():d1.getDate())+"-"+(d1.getMonth()+1)+"-"+d1.getFullYear()+" To "+(d2.getDate()<10? "0"+d2.getDate():d2.getDate())+"-"+(d2.getMonth()+1)+"-"+d2.getFullYear();
                         
		         chartData=data_array;
		        

		         if(chart_type=="piechart")
                             createPieChart();
                         else if(chart_type=="barchart")
                            createBarChart();
                         else
                            createPieChart();
		         

		       }
                       else{
                           $("#chartContainer").html("<h1 style='color:#4588cc;'>No data to be visualized in the specified period:"+(d1.getDate()<10? "0"+d1.getDate():d1.getDate()) +"-"+(d1.getMonth()+1)+"-"+d1.getFullYear()+" <i>to</i> "+(d2.getDate()<10? "0"+d2.getDate():d2.getDate())+"-"+(d2.getMonth()+1)+"-"+d2.getFullYear() +"</h1>");

                          }





		}
               else{//for category



                      d1=new Date(start_date);
                      d2=new Date(end_date);

                 
		   
                         

                         report_displayed="Campaigns Categories: Total=";
                          campaign_categories=["Personalized Reminders","Birthday Greetings","General Reminders","Holidays Greetings and Wishes","Holidays Deals","General Deals, and Discounts"];
			  for(var i=0;i<campaign_categories.length;i++){
		            
		           array_items_counter=0; 
                              
		            var campaign_category=campaign_categories[i];
                             
		            // now count the number messages in this campaign. If there are no messages ignore it
		              for(var y in resmessages){
		                 
		                 message_category_name=resmessages[""+y+""]["CampaignCategory"];
		                 message_scheduled_date=resmessages[""+y+""]["ScheduledDate"];
                                 //console.log("Scheduled: "+message_scheduled_date+". Start: "+start_date+". End: "+end_date);
		                 if((campaign_category==message_category_name)&&(message_scheduled_date>=start_date)&&(message_scheduled_date<=end_date))
		                   {
		                    array_items_counter++;
                                    message_counter++;

		                   }
                                   else if ((message_category_name=="Not Belonging to Campaign")&&(message_scheduled_date>=start_date)&&(message_scheduled_date<=end_date)&&(checked_not_group_nor_campaign))//We only check in the first round. When moving to the next campaign in the out loop we don't check again. Also ensure it with specified date range
                                           {
                                           
                                             not_for_group_or_camp_counter++;
                                             message_counter++;
                                      

                                           }





                      
                                   

                             
                                  

		                } //end inner for loop
		                if(array_items_counter>0)
		                {
		                  //then this campaign has some messages
                                  if(chart_type=="piechart")
		                       jsonObj={ y: array_items_counter, name: campaign_category};
                                  else if(chart_type=="barchart")
                                       jsonObj={ label: campaign_category, y: array_items_counter};
                                  else
                                      jsonObj={ y: array_items_counter, name: campaign_category};
		                  data_array[array_posn]=jsonObj;//here we are initializing data to be used during plotting
		                  
		                  array_posn++; //increment position by one
		                  
		                }
                               
	                   checked_not_group_nor_campaign=false;
                         
			 }//end outer for loop

                         // incase you have message not tied to any campaign
                         if(not_for_group_or_camp_counter>0)
                           {
                                  if(chart_type=="piechart")
                                      jsonObj={ y: not_for_group_or_camp_counter, name:"Messages not belonging to Campaigns"};
                                  else if(chart_type=="barchart")
                                       jsonObj={label:"Non-Campaign Messages", y: not_for_group_or_camp_counter};
                                  else
                                       jsonObj={ y: not_for_group_or_camp_counter, name:"Messages not belonging to Campaigns"};
		                  data_array[array_posn]=jsonObj;//here we are initializing data to be used during plotting

                            array_posn++;
                           }

		     //now check possibility of plotting if we have at least one campaign

		       if(array_posn>=1){
                         report_displayed=report_displayed+message_counter+". From "+(d1.getDate()<10? "0"+d1.getDate():d1.getDate())+"-"+(d1.getMonth()+1)+"-"+d1.getFullYear()+" To "+(d2.getDate()<10? "0"+d2.getDate():d2.getDate())+"-"+(d2.getMonth()+1)+"-"+d2.getFullYear(); 



                         chartData=data_array;
		         

		         if(chart_type=="piechart")
                             createPieChart();
                         else if(chart_type=="barchart")
                            createBarChart();
                         else
                            createPieChart();
		         

		       }
                       else{
                           $("#chartContainer").html("<h1 style='color:#4588cc;'>No data to be visualized in the specified period:"+(d1.getDate()<10? "0"+d1.getDate():d1.getDate()) +"-"+(d1.getMonth()+1)+"-"+d1.getFullYear()+" <i>to</i> "+(d2.getDate()<10? "0"+d2.getDate():d2.getDate())+"-"+(d2.getMonth()+1)+"-"+d2.getFullYear() +"</h1>");

                          }






                 }

    },2000);


};


//Retrieve All messages
var retrieveAllMessages=function ()
{     
     
     jsonObject={Empty:""};
     
      var urlstr=site;
      urlstr=urlstr+"jsondata/RAM/";// Retrieve All Sent Messages
      $.ajax({
             url: urlstr,
             dataType: "jsonp",
             method: "POST",
             data:JSON.stringify(jsonObject),
             cache: false
             })
            .done(function( resjson ) {
               //alert(resjson.AD00.messagestxt.MTXT00);
                  //alert("Messages Retrieved")
              //return resjson;
              if (Modernizr.localstorage) {
                        //store into a local storage
                        localStorage.removeItem("AllMessages");
                        localStorage.setItem("AllMessages",JSON.stringify(resjson));
                      
                      }

                

                   

          

             });





  };



//Activate or deactivate campaign

var changeCampaignStatus=function(campaign_id,status){

   if(status.checked){
     action="Activate";


   }
   else
    {
     action="Deactivate";

    }

    /*
    if("#togBtn").is(":checked"){
      alert("Checked");


    }
    else
    {
      alert("Not Checked");

    }*/

    

     jsonObject={CampaignID:campaign_id,Action:action};
     
      var urlstr=site;
      urlstr=urlstr+"jsonupdate/CCS/";// Change Campaign Status. i.e Active to Inactive or Inactive to Active
      $.ajax({
             url: urlstr,
             dataType: "jsonp",
             method: "POST",
             data:JSON.stringify(jsonObject),
             cache: false
             })
            .done(function(resjson) {
            alert(resjson["message"]);
 

             });




};


var displayCampaignsContent=function(display_type,campaign_id){
  //display type, 1 -- Viewing Mode,  2 -- Editing Mode
  //campaign_id is NULL in Viewing Mode, while in Editing Mode it will contain an id of a campaign to be edited
 
  //alert("Got here");
  retrieveCampaignsContent();
  
  /*if(display_type==EDITING_MODE)
    {
    retrieveEditingCampaignTemplate(campaign_id);

    }*/
   //alert("Got here");
  setTimeout(function(){

                       $(".progressboxcampaign").hide();
                       removeLoadingCircleCampaign();
   
                    var counter=-1;

                    var campaign_objects=[];
                    var campaign_counter=0;
                    var html_str="\n"
              
                    var resjson=JSON.parse(localStorage.getItem("Campaigns"));
                    
                    //alert("Group Content Loaded"+resjson["AD00"]["group_description"]);
                    for(var x in resjson)
                    {//start for loop
                      //counter++;
                        //if(counter==100)
                        //{
                         //  alert("got here");
                         // break;
                        //}

                         if(resjson.AD00<0)
                         {
                          break;

                         }
                        var retrieved_campaign_id=resjson[""+x+""]["CampaignID"];
                        var retrieved_campaign_name="";
                        var retrieved_campaign_descr="";
                        retrieved_campaign_name=resjson[""+x+""]["CampaignName"];  ;
                        retrieved_campaign_descr=resjson[""+x+""]["campaign_description"];  

                       
                        {
                     
                        html_str=html_str+"<tr>\n";

                        html_str=html_str+"\n  <td align='center'>";

                        if(resjson[""+x+""]["CampaignActive"]==1)
                        {


                        
                            html_str=html_str+ "<label class='switch'> \
                            A<input type='checkbox' class='togBtn' checked onchange='";
                            html_str=html_str+"changeCampaignStatus(";
                            html_str=html_str+retrieved_campaign_id;
                            html_str=html_str+ ",this)";
                            html_str=html_str+"'>";

                            html_str=html_str+"<div class='sliderswitch round'>\
                            <span class='on'>Active</span><span class='off'>Inactive</span>\
                            </div>\
                            </label>";
                        }
                        else
                        {

                            html_str=html_str+ "<label class='switch'> \
                            I<input type='checkbox' id='togBtn' onchange='";
                            html_str=html_str+"changeCampaignStatus(";
                            html_str=html_str+retrieved_campaign_id;
                            html_str=html_str+ ",this)";
                            html_str=html_str+"'>";

                            html_str=html_str+"<div class='sliderswitch round'>\
                            <span class='on'>Active</span><span class='off'>Inactive</span>\
                            </div>\
                            </label>";


                        }
                   
                        html_str=html_str+"\n  </td>";



                        //html_str=html_str+"<tr>\n";

                        html_str=html_str+"\n  <td align='center'>";


                        html_str=html_str+retrieved_campaign_name;
                   
                        html_str=html_str+"\n  </td>"

                           
                        
                        html_str=html_str+"\n  <td align='center' style=\"overflow:hidden; width:200px;\">"
                        html_str=html_str+retrieved_campaign_descr;
                        html_str=html_str+"\n  </td>";


                        html_str=html_str+"\n  <td align='center'>"
                        html_str=html_str+resjson[""+x+""]["DateCreated"];
                        html_str=html_str+"\n  </td>";

                        html_str=html_str+"\n  <td align='center'>"
                        html_str=html_str+resjson[""+x+""]["TotalMessages"];
                        html_str=html_str+"\n  </td>";


                        html_str=html_str+"\n <td align='center' class=\"iconbuttons\">";

                      
                        html_str=html_str+"\n   <button style=\"font-size:24px;color:blue\" title=\"Edit this campaign\" onclick=\"editCampaign('";
                        html_str=html_str+resjson[""+x+""]["CampaignID"];
                        html_str=html_str+"','EDITCAMPAIGN')\"><i class=\"fa fa-pencil\"></i></button>";


                        html_str=html_str+"\n   <button style=\"font-size:24px;color:red;\" title=\"Delete this CAMPAIGN\" onclick=\"deleteCampaign('";
                        html_str=html_str+resjson[""+x+""]["CampaignID"];
                        html_str=html_str+"','DELETECAMPAIGN')\"><i class=\"fa fa-trash-o\"></i></button>";
                    
                        

                        html_str=html_str+"\n</tr>\n";
                        $("#campaigns").html(html_str); 
                    
                      
                         }
                  
                   

                     }

                     //$("#campaignstable").DataTable();
                     setTimeout(function(){
          
                   $("#campaignstable").DataTable();

            },20);

                      

  },2000);

  





 };

 var showHideCampaignEnd=function(showstatus){

      if(showstatus)
      {
       $("#campaignenddate").show();

      }
      else{

        $("#campaignenddate").hide();

      }

 };

 var hideShowCampaignTargets=function(){

  if($("#deliverymedium").val()=="SMS")
  {
   $("#campaigntargetsms").show();
    $("#campaigntargetwhatsapp").hide();

  }
  else
  {

      if($("#deliverymedium").val()=="Whatsapp")
      {
        $("#campaigntargetsms").hide();
        $("#campaigntargetwhatsapp").show();

      }
      else
      {
        alert("Email Campaign Functionality will be implemented in the future")
        $("#campaigntargetsms").show();
        $("#campaigntargetwhatsapp").hide();

      }



  }



 }



 var showExistingCampaigns=function(){

$("#managecampaigns").show();
$("#createcampaign").hide();
$("#createcampaignbtn" ).prop( "disabled", false );
$("#viewcampaignsbtn" ).prop( "disabled", true);

//$("#managecampaignstatus").html("Viewing Address Book");



};


var createNewCampaign=function(mode){

if(mode=='NEW')// Then clear the form
{

 
 //$('#campaignForm').trigger("reset");
 //$("#campaignForm")[0].reset()

 $("#savingcampaignheader").html('Create New Campaign');
 
 $('#campaignForm').find('input:text').val('');   
 $('#campaignForm').find('textarea').val('');

 //Next hide any boxes that are meant to be hidden

 $("#numOfGroups").hide();
 $("#campaigntargetwhatsapp").hide();


 $(".remindertemplates").hide().hide();
 $("#campaignenddate").hide();
 
 $("input[name=lifeofcampaign][value=1]").prop("checked",true);

 $("#category1").prop('selected', true);
       

 $("#hiddencampaignid").val(-1); //Put this to -1 so that the server side script can be able to distinguish between new campaign and an old campaign.
   removeMsgBoxes();

}
else{

  $("#savingcampaignheader").html('Update Existing Campaign');
} 





$("#managecampaigns").hide();
$("#createcampaign").show();

$("#createcampaignbtn" ).prop( "disabled", true);
$("#viewcampaignsbtn" ).prop( "disabled", false);

//now find existing groups
  if(checkGroupsForCampaign()>=0)
  {

     //Now populate existing groups into the campaign editing form

      populateGroupsForCampaign();
      //displayTimeOfRunningBoxes(1);//By Default only one option should be displayed
      attachEventToGroupsCampaign();





  }
  else{


    $('#campaigntargetsms')
         .append($("<option id='campaigntargetallsms' name='campaigntargetallsms'></option>")
         .attr("value",'0')
         .text("All")); //just provide only one option 
  } 
  

displayTimeOfRunningBoxes(1);//By Default only one option should be displayed. What time of the day a campaign will be running




//$("#addressbookstatus").html("Updating Address Book");

};


var bindEventsToCampaignDateFields=function(){

  //$("#campaignstartdate").off( "change" ); // unbind this event
   //$("#campaignstartdate").on('change',function(e){ // bind this event

    $(".dates").off("change"); // unbind this event
    $(".dates").on('change',function(e){ // bind this event
    // Modify date to a more user friendly format
    e.preventDefault();
    var picked_date=""+$(this).val();
    
    picked_id=$(this).attr("id");

    campaign_date_extra_id="#"+picked_id+"extra";
    //$(campaign_date_extra_id).val(picked_date);
    $(campaign_date_extra_id).val(picked_date);


    var first_slash=picked_date.indexOf("/");
    var second_slash=picked_date.lastIndexOf("/");
  
    var mm=picked_date.substring(0,first_slash);
    var month=mm;
    switch(mm)
    {
    case "01":mm="January";break;
    case "02":mm="February";break;
    case "03":mm="March";break;
    case "04":mm="April";break;
    case "05":mm="May";break;
    case "06":mm="June";break;
    case "07":mm="July";break;
    case "08":mm="August";break;
    case "09":mm="September";break;
    case "10":mm="October";break;
    case "11":mm="November";break;
    case "12":mm="December";break;
    
    }
    var dd=picked_date.substring(first_slash+1,second_slash);
    var yyyy=picked_date.substring(second_slash+1,picked_date.length);
    $(this).val(dd+" "+mm+" "+yyyy);

  

   });





};

//Retrieve Template for groups
var retrieveCampaignsTemplate=function ()
{     
     
      var urlstr=site;
      urlstr=urlstr+"jsondata/RCT/";// Retrieve campaign template
      $.ajax({
             url: urlstr,
             cache: false
             })
            .done(function( html ) {
            //$( "#main-content" ).html( html );
              //handleSliderNav();
              //alert("Done");
             $("#main-content").html(html);
             $("#campaignstartdate" ).datepicker();
             $("#campaignenddate").datepicker();


              bindEventsToCampaignDateFields();



              setTimeout(function(){



                  $('#reminderfile').on('change', function() {
                      let fileName=$('#reminderfile').val();
                      let ext = fileName.split('.').pop();
                      let split_str=fileName.split('\\');
                      let split_str_len=split_str.length;
                      if(split_str_len>1){
                       //Just get the name without path name 
                        fileName=split_str[split_str_len-1];


                      }

                      if(ext!=="xls")
                      {
                        alert("Wrong file with extension '"+ext+"'. Only files with '.xls' extension are allowed.");
                        $('#reminderfile').val('');
                        $('#addreminderfilename').html('<b>File</b>: No File');
                      }
                      else
                      {
                      
                        $('#addreminderfilename').html('<b>File</b>: '+fileName+'');


                      }
                     /*var file = this.files[0];
                      if (file.size > 1024) {
                          alert('max upload size is 1k')
                     }*/


                     });

                    },20);

              //for sms
              /*
             $('#campaigntargetsms option').mousedown(function(e) {
                e.preventDefault();

                if($(this).val()=='0'){

                if(!$(this).prop('selected'))
                     $(".campaigngroupssms").prop('selected',false);


                }
                else
                {
                 $("#campaigntargetallsms").prop('selected',false);

                }
                $(this).prop('selected',!$(this).prop('selected'));
                return false;
                });
                */



             //for whatsapp

             $('#campaigntargetwhatsapp option').mousedown(function(e) {
                e.preventDefault();

                if($(this).val()=='0'){

                if(!$(this).prop('selected'))
                     $(".campaigngroupswhatsapp").prop('selected',false);


                }
                else
                {
                 $("#campaigntargetallwhatsapp").prop('selected',false);

                }
                $(this).prop('selected',!$(this).prop('selected'));
                return false;
                });

            //retrieveAddressBookContent();
             });



  };//end of retrieveAddressBookTemplate 


var retrieveEditingCampaignTemplate=function (campaign_id)
{     
      
      var urlstr=site;
      urlstr=urlstr+"jsondata/ROCT/";// Retrieve one campaign editing template
      $.ajax({
             url: urlstr,
             cache: false
             })
            .done(function( html ) {
            
              $("#main-content").html(html);
              $("#savecampaignbtn").unbind( "click" ); // Remove the previous click handlers.
              $("#savecampaignbtn").bind('click',function(){
                //saveCampaign(campaign_id,'SAVECAMPAIGN','2');
                saveCampaign();

              
                });
           
             });



  };//end of retrieveAddressBookTemplate 

//end of  displaying campaigns


var retrieveDashBoardTemplate=function(){


      var urlstr=site;
      urlstr=urlstr+"jsondata/RDBT/";// Retrieve dash board template
      $.ajax({
             url: urlstr,
             cache: false
             })
            .done(function( html ) {
            
              $("#main-content").html(html);


                $("#dashboard_date_picker_1" ).datepicker();
                $("#dashboard_date_picker_2" ).datepicker();

                $("#dashboard_date_picker_1" ).prop( "disabled", true);
                 $("#dashboard_date_picker_2" ).prop( "disabled", true);
                 //
                 //By default General Trend is disabled

                 $("#viewbycampaigncategory" ).prop( "disabled", false);
                 $("#viewbycampaign" ).prop( "disabled", false);
                 $("#viewbygroup" ).prop( "disabled", false);
                 $("#generaltrend" ).prop( "disabled", true);


       


              $(".messages_interval_class").unbind( "change" ); // Remove the previous click handlers.
              $(".messages_interval_class").bind('change',function(){
              var selected_radio_id=$(this).attr('id');
              if(selected_radio_id=="specifyinterval"){
                // if(("#dashboard_date_picker_1").val()=="")
                //        $("#hidden_dashboard_date_picker_1").val("");//reset

                 $("#dashboard_date_picker_1" ).prop( "disabled", false);
                 $("#dashboard_date_picker_2" ).prop( "disabled", false);
                 
               }
              else
                 {
                 $("#dashboard_date_picker_1" ).prop( "disabled", true);
                 $("#dashboard_date_picker_2" ).prop( "disabled", true);
                

                  $("#dashboard_date_picker_1" ).val( "");
                 $("#dashboard_date_picker_2" ).val( "");
                 }


              });




              $(".vizualization").unbind( "change" ); // Remove the previous click handlers.
              $(".visualization").bind('change',function(){
              selected_radio_id=$(this).attr('id');
              if(selected_radio_id=="linechart"){
                 $("#viewbycampaigncategory" ).prop( "disabled", true);
                 $("#viewbycampaign" ).prop( "disabled", true);
                 $("#viewbygroup" ).prop( "disabled", true);
                 $("#generaltrend" ).prop( "disabled", false);
                 
               }
              else
                 {
                 $("#viewbycampaigncategory" ).prop( "disabled", false);
                 $("#viewbycampaign" ).prop( "disabled", false);
                 $("#viewbygroup" ).prop( "disabled", false);
                 $("#generaltrend" ).prop( "disabled", true);
                  
                 }


              });

	
	$('#main-content').delegate(".datepickers", "change", function () {
       
	  
		var picked_date=""+$(this).val();
		var first_slash=picked_date.indexOf("/");
		var second_slash=picked_date.lastIndexOf("/");
		
		var mm=picked_date.substring(0,first_slash);
		var month=mm;
		switch(mm)
		{
		case "01":mm="Jan";break;
		case "02":mm="Feb";break;
		case "03":mm="Mar";break;
		case "04":mm="Apr";break;
		case "05":mm="May";break;
		case "06":mm="June";break;
		case "07":mm="July";break;
		case "08":mm="Aug";break;
		case "09":mm="Sept";break;
		case "10":mm="Oct";break;
		case "11":mm="Nov";break;
		case "12":mm="Dec";break;
		
		}
		var dd=picked_date.substring(first_slash+1,second_slash);
		var yyyy=picked_date.substring(second_slash+1,picked_date.length);
		$(this).val(dd+" "+mm+" "+yyyy);
                var id_hidden="#hidden_"+$(this).attr('id')

		$(id_hidden).val(yyyy+"-"+month+"-"+dd);
		
		
	});









              $("#viewbycampaign").unbind( "click" ); // Remove the previous click handlers.
              $("#viewbycampaign").bind('click',function(){
              
                

                setTimeout(function(){

	       
                displayDashboard('Campaigns');
            

               },100);

              
                });


              $("#viewbygroup").unbind( "click" ); // Remove the previous click handlers.
              $("#viewbygroup").bind('click',function(){
              
                

                setTimeout(function(){

	   
                displayDashboard('Groups');

               },100);

              
                });


              $("#viewbycampaigncategory").unbind( "click" ); // Remove the previous click handlers.
              $("#viewbycampaigncategory").bind('click',function(){
              
                

                setTimeout(function(){

	   
                displayDashboard('Category');

               },100);

              
                });


              $("#generaltrend").unbind( "click" ); // Remove the previous click handlers.
              $("#generaltrend").bind('click',function(){
              
                

		        setTimeout(function(){

		       
		        displayDashboard('Trend');
		    

		       },100);

              
                });


              $("#viewbygroup").unbind( "click" ); // Remove the previous click handlers.
              $("#viewbygroup").bind('click',function(){
              
                

		        setTimeout(function(){

		   
		        displayDashboard('Groups');

		       },100);

              
                });
           
             });







};
var resetToHome=function(menu_id)
{

 if(current_menu==menu_id)
     return; 
 var homeStr="<h2 style=\"color:green;\"><i>Yote Messaging</i> uses SMS and Whatsapp: from handling relationship with your customers to communicating with your various teams such as sales and marketing</h2>\n<!--Declare pop up for sending message-->";

$("#main-content").html(homeStr);
 
current_menu=menu_id;  



}


var manageAddressBook=function(menu_id)
{


 if(current_menu==menu_id)
     return; 
retrieveAddressBookTemplate();
current_menu=menu_id;

};

var manageBalance=function(menu_id){

 if(current_menu==menu_id)
     return; 
retrieveBalanceTemplate();
current_menu=menu_id;



};

var viewDashboards=function(menu_id)
{



if(current_menu==menu_id)
     return; 

retrieveDashBoardTemplate();

retrieveAllMessages();


current_menu=menu_id;
};

var manageSettings=function(menu_id)
{


if(current_menu==menu_id)
     return; 
 retrieveSettingsTemplate();  
current_menu=menu_id;
};

var manageGroups=function(menu_id)
{


if(current_menu==menu_id)
     return; 
retrieveGroupsTemplate();
displayGroupsContent(VIEWING_MODE);
current_menu=menu_id;


};

var manageCampaigns=function(menu_id)
{

 

//alert("Manage Campaigns");
if(current_menu==menu_id)
     return; 
//Reset previosly defined campaign messages to Zero.
total_no_msg_box=0;

retrieveCampaignsTemplate();
//Now display progress bar.






setTimeout(function(){

//$('#campaignstable').DataTable();
   $("#myprogressbar_campaign").html('');
   $(".progressboxcampaign").show();
   addLoadingCircleCampaign();
   displayCampaignsContent(VIEWING_MODE);



},100);

current_menu=menu_id;
};


var initialized=false;

//provide links to menus
var initializeMenu=function(){
 
   
if(!initialized)//check if the menu has note been prviously initialized
    {
  
           initialized=true;
           current_menu="Home";

          
       
          $(".menuimage").on("click", function(event){

             var item=$(this).attr("value");
             $( "#smsdialog").dialog( "close" );//close if the dialog was left open.
            
        


		       
       
			 switch(item)

			  {
                          case "Home":resetToHome(item);break;
			  case "AddressBook":contact_card_hidden=true;manageAddressBook(item);break;
		          case "DashBoard":viewDashboards(item);break;
                          case "Settings":manageSettings(item);break;
                          case "Grouping":manageGroups(item);break;
			  case "Campaign":manageCampaigns(item);break;
                          case "RechargeAccount":manageBalance(item);viewBalance();break;

			         //case "MainPage":$.mobile.changePage( "#pageone", { transition: "slide", changeHash: false });break;
               
			 	      
				

			

			   

			   default: alert("Functionality Under Construction");current_menu=null;

			   }

			   

			   $("img").toggle();

			   $("img").show();

			   

            });
  
  }

//end function initialize
}

var searchGroupTable=function(){

var value=$("#searchablegrouptable").val();
value=value.toLowerCase();
$("#groups tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
     
          

    });

};


//no longer used. 
var searchCampaignTable=function(){

var value=$("#searchablecampaigntable").val();
value=value.toLowerCase();
$("#campaigns tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
     
          

    });

};

//count remaining chars to type
var countRemaining=function(maxval,id1,id2){

var current_str=$(id1).val();
var remaining=parseInt(maxval)-current_str.length;

var current_percentage=(current_str.length*100)/parseInt(maxval);

if(current_percentage<30){
$(id2).css("color","black");

}
else{
if(current_percentage<70){
$(id2).css("color","blue");
}
else{
$(id2).css("color","red");

}
}
$(id2).html(""+remaining+" remaining");

};



//delete all boxes

var removeMsgBoxes=function()
{

$("#camp_msg_grp").html('');
$("#del_msg_boxes").hide(); 
total_no_msg_box=0;//reset the number of boxes
$("#numOfAppendedMessages").val(total_no_msg_box);
};

//append extra text boxes for defining cambaign messages
var addMessageBox=function(content)
{

var new_msg_box_id="campaignmsgbx_"+total_no_msg_box;

total_no_msg_box=total_no_msg_box+1;//increment the number of messages to be defined for a campaign

if(total_no_msg_box==1){

  $("#del_msg_boxes").show(); //hide 
}
//now create html for new message box and update the current boxes by appending a new box html

//var new_msg_box=current_boxes;
var new_msg_box="";
new_msg_box=new_msg_box+"<b>Message ";
new_msg_box=new_msg_box+total_no_msg_box;
new_msg_box=new_msg_box+"</b>: <span id=\"charcounter_"; //for counting number of characters
new_msg_box=new_msg_box+new_msg_box_id;
new_msg_box=new_msg_box+"\">0</span> <i><b>characters</b></i></br><textarea id=\""; //append id
new_msg_box=new_msg_box+new_msg_box_id;
new_msg_box=new_msg_box+"\" ";

new_msg_box=new_msg_box+"name=\""; //append name
new_msg_box=new_msg_box+new_msg_box_id;
new_msg_box=new_msg_box+"\" ";

new_msg_box=new_msg_box+" onkeyup=\"countTyped('200','#";
new_msg_box=new_msg_box+new_msg_box_id;
new_msg_box=new_msg_box+"','#charcounter_";

new_msg_box=new_msg_box+new_msg_box_id;
new_msg_box=new_msg_box+"');\"";
new_msg_box=new_msg_box+ " rows=\"3\" cols=\"40\" maxlength=\"450\">";
new_msg_box=new_msg_box+"</textarea>";
new_msg_box=new_msg_box+"<br/><br/>";

//now append with the updated html content

$("#camp_msg_grp").append(new_msg_box);

if(content==undefined){
  

}
else
{
  //put message content if editing is done on the existing campaign
 let msg_id="#"
 msg_id=msg_id+new_msg_box_id;
 $(msg_id).val(content);

}

$("#numOfAppendedMessages").val(total_no_msg_box);

};


//Count how many characters have been typed into a campaign message box
var countTyped=function(maxval,id1,id2){


var current_str=$(id1).val();

var remaining=parseInt(maxval)-current_str.length;
var typed=current_str.length;
var current_percentage=(current_str.length*100)/parseInt(maxval);

if(current_percentage<30){
    $(id2).css("color","black");

}
else{
    if(current_percentage<70){
     $(id2).css("color","blue");
     }
     else{
    $(id2).css("color","red");

    }
}
$(id2).html(""+typed+"");

};

//validate if what is typed is an integer
var isNumberKey=function(evt){
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
    return true;
};

// These boxes will be used to define the time of the day when a campaign should run
var displayTimeOfRunningBoxes=function(picked_frequency){


var timeboxstr="";
for(var i=0;i<picked_frequency;i++){
   timeboxstr=timeboxstr+"Time ";
   timeboxstr=timeboxstr+(i+1);
   timeboxstr=timeboxstr+": ";
   timeboxstr=timeboxstr+"<select id=\"hour";
   timeboxstr=timeboxstr+i;
   timeboxstr=timeboxstr+"\" ";
   timeboxstr=timeboxstr+"name=\"hour";
   timeboxstr=timeboxstr+i;
   timeboxstr=timeboxstr+"\">\n";

   //now populate options for hours
   for(var j=0;j<24;j++){
     
     if(j<10){ //append a zero before a number when it less than 10
      timeboxstr=timeboxstr+"\t<option value='0";
      timeboxstr=timeboxstr+j;
      timeboxstr=timeboxstr+"'>0";
      timeboxstr=timeboxstr+j;
      timeboxstr=timeboxstr+"</option>\n";

     }
     else{

      timeboxstr=timeboxstr+"\t<option value='";
      timeboxstr=timeboxstr+j;
      timeboxstr=timeboxstr+"'>";
      timeboxstr=timeboxstr+j;
      timeboxstr=timeboxstr+"</option>\n";

     }


   }
   timeboxstr=timeboxstr+"</select>\n"; //Close the first select

   timeboxstr=timeboxstr+"<select id=\"minutes";
   timeboxstr=timeboxstr+i;
   timeboxstr=timeboxstr+"\" ";  

  timeboxstr=timeboxstr+"name=\"minutes";
   timeboxstr=timeboxstr+i; 
   timeboxstr=timeboxstr+"\">\n"; 

  //now populate options for minutess
   for(var j=0;j<60;j++){
     
     if(j<10){ //append a zero before a number when it less than 10
      timeboxstr=timeboxstr+"\t<option value='0";
      timeboxstr=timeboxstr+j;
      timeboxstr=timeboxstr+"'>0";
      timeboxstr=timeboxstr+j;
      timeboxstr=timeboxstr+"</option>\n";

     }
     else{

      timeboxstr=timeboxstr+"\t<option value=";
      timeboxstr=timeboxstr+j;
      timeboxstr=timeboxstr+">";
      timeboxstr=timeboxstr+j;
      timeboxstr=timeboxstr+"</option>\n";

     }


   }


  timeboxstr=timeboxstr+"</select>\n<br/>"; //Close the second  select and break so that each time group is displayed on its own line


}

$("#timeofrunning").html('');

$("#timeofrunning").html(timeboxstr);




};


//Check if the user has picked an option to select days of the weeek in which a campaign will be running
var checkDaySelected=function(){
   var daysintervals=$("#daysintervals").val();
   //$("input[name=interview]:checked").val()
   if(daysintervals=="4")
   {
     //alert(daysintervals);
    $("#campaignselectivedays").show(); // display an interface that will allow user to pick specific days of the week

   }
   else
   {

    $("#campaignselectivedays").hide();

   }
//campaignselectivedays


};

var checkCampaignFrequency=function(){

var selectedvalue=$("#frequencyofrunningselected").val();
var picked_frequency;
if(selectedvalue==6)
   {
     
    $("#userdefinedfrequency").show();
     user_defined_campaign_frequency_status=1;//When capturing details of a campaign, this will help in knowing whether to use select box or text box for value of frequency
     picked_frequency=$("#userdefinedfrequency_box").val();
     //alert(picked_frequency);
     if((picked_frequency=='')||(picked_frequency==null)||(picked_frequency===undefined)){
       //picked_frequency=1;
    

     }
       
     else{
         parseInt(picked_frequency);
         displayTimeOfRunningBoxes(picked_frequency);

     }
    
   }
 else
  {
      $("#userdefinedfrequency").hide();
      user_defined_campaign_frequency_status=0;
      picked_frequency=$("#frequencyofrunningselected").val();
      displayTimeOfRunningBoxes(picked_frequency)
  }



};


var saveCampaign=function(){

     //var record_id=menu_id+"";
     //record_id=record_id+campaign_id;
     var jsonObject = JSON.stringify($("#campaignForm :input").serializeArray());

     var formData=new FormData($('#remindersuploadfileform')[0]);
     formData.append('json', jsonObject); 
 

      var urlstr=site;
      urlstr=urlstr+"jsonupdate/SCD/";// Save Campaign Details
    

      $.ajax({
             url: urlstr,
             dataType: "jsonp",
             method: "POST",
             //data:jsonObject,
             data:formData,
             cache: false,
             processData: false,
             contentType: false
                            
             })
            .done(function( resjson ) {
                alert(resjson.message);

                //Cache new content since there has been an update on Campaigns hence existing cache is no longer uptodate
               if (Modernizr.localstorage) {

                  localStorage.removeItem("Campaigns"); //remove campaign first before setting it again
                    
                  localStorage.setItem("Campaigns",JSON.stringify(resjson["data"]));
                        
                  }


             });





 
 


setTimeout(function(){

$(".progressboxcampaign").show();
addLoadingCircleCampaign();

displayCampaignsContent(VIEWING_MODE);


},1000);

if(save_type=="0"){
    //alert("I am here");
                //retain the previous search
                setTimeout(function(){
                searchCampaignTable();



},200);

}

//Now retrieve group content for editing
current_menu=record_id;

};



var populateGroupsForCampaign=function(selectedgrps){


var newOptions={};
json_obj=JSON.parse(localStorage.getItem("Groups"));
if (json_obj===undefined)
{
retrieveGroupsContent();
json_obj=JSON.parse(localStorage.getItem("Groups"));
}

for(var x in json_obj)
{
  let gid=""+json_obj[""+x+""]["GroupID"];
  let gname=""+json_obj[""+x+""]["GroupName"];
  newOptions[""+gid]=gname;
  //alert(newOptions["id_"+gid]);

}


var select = $('#campaigntargetsms');
$('option', select).remove();

//Append 'All OPtion'
$('#campaigntargetsms')
         .append($("<option id='campaigntargetallsms' name='campaigntargetallsms'></option>")
         .attr("value",'0')
         .text("All"));


if(json_obj.AD00<0)
 {
 
  return; // it means the group 
}

//var count = Object.keys(newOptions).length;

$.each(newOptions, function(key, value) {
      let option_str= "<option class='campaigngroupssms' id='gid_";
      option_str=option_str+key;
      option_str=option_str+"'></option>";
     $('#campaigntargetsms')
         .append($(option_str)
         .attr("value",key)
         .text(value));
});
//select.val("2");



};


var attachEventToGroupsCampaign=function(){

     $("#campaigntargetsms option").off( "mousedown" ); //unbind any previous event

                              
      $("#campaigntargetsms option").on('mousedown',function(e){

    
                e.preventDefault();

                if($(this).val()=='0'){

                    if(!$(this).prop('selected'))
                         $(".campaigngroupssms").prop('selected',false);


                }
                else{
                    $("#campaigntargetallsms").prop('selected',false);

                }
                $(this).prop('selected',!$(this).prop('selected'));

                var selected_groups_count = $("#campaigntargetsms :selected").length;
                $("#numOfGroups").val(selected_groups_count);
                return false;
                                 
                                       
    });


    //For Campaign category
    
    $("#campaigncategory option").off( "mousedown" ); //unbind any previous event

                              
      $("#campaigncategory option").on('mousedown',function(e){

                //Hide or Show functionality for uploading reminders file depending on whether individualized reminders' options is not chosen or it is chosen
                e.preventDefault();

                if($(this).val()=='IR'){



                $(".remindertemplates").show();


                }
                else{
                     $(".remindertemplates").hide();

                }
                
                                 
                                       
    });  


};




var formatToReadableCampaignDate=function(camp_date){

    var picked_date=""+camp_date;
    
    
    var first_dash=picked_date.indexOf("-");
    var second_dash=picked_date.lastIndexOf("-");
    if((first_dash<0)||(second_dash<0))
        return picked_date; //Most likely the date was empty therefore return the same date
  
    var dd=picked_date.substring(0,first_dash);
    var mm=picked_date.substring(first_dash+1,second_dash);
    var yyyy=picked_date.substring(second_dash+1,picked_date.length);
  
    switch(mm)
    {
    case "01":mm="January";break;
    case "02":mm="February";break;
    case "03":mm="March";break;
    case "04":mm="April";break;
    case "05":mm="May";break;
    case "06":mm="June";break;
    case "07":mm="July";break;
    case "08":mm="August";break;
    case "09":mm="September";break;
    case "10":mm="October";break;
    case "11":mm="November";break;
    case "12":mm="December";break;
    
    }

    var formarted_date=dd+" "+mm+" "+yyyy;
    return formarted_date;
};


var formatToHiddenCampaignDate=function(camp_date){

      var picked_date=""+camp_date;
    
    
    var first_dash=picked_date.indexOf("-");
    var second_dash=picked_date.lastIndexOf("-");
    if((first_dash<0)||(second_dash<0))
        return picked_date; //Most likely the date was empty therefore return the same date
  
    var dd=picked_date.substring(0,first_dash);
    var mm=picked_date.substring(first_dash+1,second_dash);
    var yyyy=picked_date.substring(second_dash+1,picked_date.length);

    var formarted_date=mm+"/"+dd+"/"+yyyy;
    return formarted_date;

};



var editCampaign=function(campaign_id,menu_id){

 var record_id=menu_id+"";
 record_id=record_id+campaign_id;
 //if(current_menu==record_id)
 //    return;  

//alert("Edit Group.."+group_id);

//now call a function to save records


createNewCampaign('EXIST'); // bring the box.





  var resjson=JSON.parse(localStorage.getItem("Campaigns"));
                    //alert("Group Content Loaded"+resjson["AD00"]["group_description"]);
  for(var x in resjson)
    {//start for loop
                  var retrieved_campaign_id=resjson[""+x+""]["CampaignID"];
                  
                  var retrieved_campaign_name=resjson[""+x+""]["CampaignName"];
                  var retrieved_campaign_descr=resjson[""+x+""]["campaign_description"];  

                  var retrieved_start_date=resjson[""+x+""]["CampaignStartDate"];
                  var retrieved_end_date=resjson[""+x+""]["CampaignEndDate"]; 
                  var retrieved_delivery_medium= resjson[""+x+""]["DeliveryMedium"]; 
                  var targeted_audience=resjson[""+x+""]["TargetedAudience"];
                  var campaign_category=resjson[""+x+""]["CampaignCategory"];

                  var campaign_hours=resjson[""+x+""]["CampaignDeliveryHours"];
                  var campaign_days_of_week=resjson[""+x+""]["CampaignDays"];
                  

                  //alert(retrieved_campaign_name);
      
                  if(campaign_id==retrieved_campaign_id){

                        $('#hiddencampaignid').val(campaign_id);
                        $("#campaign_name").val(retrieved_campaign_name);
                        $("#campaign_descr").val(retrieved_campaign_descr);
                      
                        
                         // Put dates in a format that human readerable/friendly
                        $("#campaignstartdate").val(formatToReadableCampaignDate(retrieved_start_date));
                        $("#campaignenddate").val(formatToReadableCampaignDate(retrieved_start_date));

                         // Put dates in a format that it is easier for the system to process
                        $("#campaignstartdateextra").val(formatToHiddenCampaignDate(retrieved_start_date));
                        $("#campaignenddateextra").val(formatToHiddenCampaignDate(retrieved_start_date));

                         var selectgroup = $('#campaigntargetsms');

                         var selectedgroups=[];                       
                         var deliverymediums=Array('SMS','Whatsapp','Email');
                        
                         var option_id;
                         var idposn;  
                         for(var i=0;i<deliverymediums.length;i++){
                     
                             option_id="#deliverymedium";
                             idposn=i+1;
                             option_id=option_id+idposn;
                            if(deliverymediums[i]==retrieved_delivery_medium)
                            {
                            
                             $(option_id).prop('selected', true);
       
                            }
                            else
                            {
                            
                             $(option_id).prop('selected', false);
                              
                            }
                          


                         }


                         //Find campaign category.
                         var categories=Array('GM','GR','HG','HO','IR','BW');

                        for(var i=0;i<categories.length;i++){
                     
                             option_id="#category";
                             idposn=i+1;
                             option_id=option_id+idposn;
                            if(categories[i]==campaign_category)
                            {
                            


                             $(option_id).prop('selected', true);

                             //now check if it is individual reminders

                              if(campaign_category=="IR")
                              {

                                  //Then show the option for downloading file with reminders.
                                     $(".remindertemplates").show();
                                     $("#existingremindersoption").show();

                                     $('#includeexistingreminders').prop('checked', true);

                                     //bind click event to the above checkbox

                                     //$("#downlodremindertempbtn").unbind( "click" );

                                    $("#downlodremindertempbtn").removeAttr('onclick');


                                    $("#downlodremindertempbtn").bind('click',function(){
                                        downloadReminderTemplate(1); //now download a template that include existing reminders
          
                                      });

                              }
                             else
                             {

                              $(".remindertemplates").hide();
                              $("#existingremindersoption").hide();

                              $('#includeexistingreminders').prop('checked', false);

                              $("#downlodremindertempbtn").unbind( "click" );

                              $("#downlodremindertempbtn").removeAttr('onclick');


                              $("#downlodremindertempbtn").bind('click',function(){
                                 downloadReminderTemplate(0); //now download a template that include existing reminders
          
                              });

                              
                             }


                             break;

                            //change the content for downloading reminder button to also consider existing reminder since this is an update exercise
                            //var downloader_content="<td colspan=\"2\" align=\"center\">Download a template for preparing individual reminders<br>";
                            //downloader_content=downloader_content+"<button style=\"font-size:24px;cursor:pointer" onclick="downloadReminderTemplate(0);"> <i class="fa fa-download" style="font-size:48px;color:GREEN"></i></button><br><br></td>


             

                            }
                         


                         }
                         var delivery_days=[]
                         var delivery_days_counter=0

                         //Now check all campaign days of a week
                        
                         for(var delivery_day in campaign_days_of_week)
                         {
                         
                          delivery_days[delivery_days_counter]=campaign_days_of_week[""+delivery_day+""];
                          if(delivery_days[delivery_days_counter]=="No days"){

                              break;
                            }
                          delivery_days_counter++;

                         }

                         //outside of for loop



                         if(delivery_days_counter==0)
                            {

                             $("#daysintervals").val('4');

                            }
                         else
                           {

                              if(delivery_days_counter==6)
                              {

                              $("#daysintervals").val('1');

                              }
                              else
                                 {


                                  if(delivery_days_counter==5)
                                  {
                                    //check if if it Monday to Friday, Monday is 1 and Friday is five

                                    var weekdays_counter=0;

                                    for(var i=0;i<delivery_days.length;i++){
                                       if(delivery_days[i]==(i+1))
                                           weekdays_counter++;


                                    }

                                    if(weekdays_counter==delivery_days_counter)
                                       {

                                        $("#daysintervals").val('2'); 
                                       }
                                       else
                                          { //The these days must have been picked from Specific Days in a random fashion
                                             $("#daysintervals").val('4'); 

                                             //Now show boxes for days and pick them one by one
                                             $("#campaignselectivedays").show();
                                              //next put tick  to appropriate days
                                                    //next put tick  to appropriate days
                                                    for(var i=0;i<7;i++){
                                                            day=i+1;
                                                            if(i==6)
                                                              day=0;

                                                            var box_posn=day;
                                                            var box_name="input[type='checkbox'][name='campaigndayofweek_";
                                                            box_name=box_name+box_posn;
                                                            box_name=box_name+"']";
                                                            var found=false;
                                                          
                                                   
                                                          //check if this day of the week is among delivery days 

                                                          for(var j=0;j<delivery_days_counter;j++){

                                                            
                                                            if(parseInt(delivery_days[j])==day)
                                                              {

                                                                /*
                                                                var box_posn=i+1;
                                                                var box_name="input[type='checkbox'][name='campaigndayofweek_";
                                                                box_name=box_name+box_posn;
                                                                box_name=box_name+"']";*/
                                                                found=true; 
                                                                break;// Once found just break out of the loop


                                                              }
                                                            }
                                                          //now check if this particular day should be checked or unchecked
                                                          if(found){

                                                             $(box_name).prop('checked', true);
                                                          }
                                                          else{
                                                               $(box_name).prop('checked', false);


                                                          }


                                                        }




                                          }


                                  

                                   }//end of if(delivery_days_counter==5)
                                   else{ 
                                          

                                          if((delivery_days_counter==4) || (delivery_days_counter==3) || (delivery_days_counter==1)){
                                          //Then it must come from specific days, because the pattern doesn't specifically fall on weekends (2 days), weekdays (5 days) or the entire week (7 days)
                                           
                                                   $("#daysintervals").val('4'); 


                                                   //Now show boxes for days and pick them one by one
                                                   $("#campaignselectivedays").show();

                                                  
                                                     
                                                    //next put tick  to appropriate days
                                                    for(var i=0;i<7;i++){
                                                            day=i+1;
                                                            if(i==6)
                                                              day=0;

                                                            var box_posn=day;
                                                            var box_name="input[type='checkbox'][name='campaigndayofweek_";
                                                            box_name=box_name+box_posn;
                                                            box_name=box_name+"']";
                                                            var found=false;
                                                          
                                                   
                                                          //check if this day of the week is among delivery days 

                                                          for(var j=0;j<delivery_days_counter;j++){

                                                            
                                                            if(parseInt(delivery_days[j])==day)
                                                              {

                                                                /*
                                                                var box_posn=i+1;
                                                                var box_name="input[type='checkbox'][name='campaigndayofweek_";
                                                                box_name=box_name+box_posn;
                                                                box_name=box_name+"']";*/
                                                                found=true; 
                                                                break;// Once found just break out of the loop


                                                              }
                                                            }
                                                          //now check if this particular day should be checked or unchecked
                                                          if(found){

                                                             $(box_name).prop('checked', true);
                                                          }
                                                          else{
                                                               $(box_name).prop('checked', false);


                                                          }


                                                        }



                                        

                                          }//end of -- if((delivery_days_counter==4) || (delivery_days_counter==3) || (delivery_days_counter==1))
                                          else{

                                            //if the pattern two days, check if it falls under weekend


                                                    var weekends_counter=0;

                                                    for(var i=0;i<delivery_days.length;i++){
                                                       if((delivery_days[i]==0)||(delivery_days[i]==6))
                                                           weekends_counter++;


                                                    }

                                                    if(weekends_counter==delivery_days.length){//then the two days are on weekend
                                                        $("#daysintervals").val('3'); 

                                                      } 
                                                      else{
                                                     
                                                   //The two days could be anywhere as there is no specific pattern to describe them

                                                              $("#daysintervals").val('4'); 

                                                             //Now show boxes for days and pick them one by one
                                                             $("#campaignselectivedays").show();
                                                              //next put tick  to appropriate days
                                                              for(var i=0;i<6;i++){
                                                                  if(parseInt(delivery_days[i])==i)
                                                                    {
                                                                      var box_posn=i+1;
                                                                      var box_name="input[type='checkbox'][name='campaigndayofweek_";
                                                                      box_name=box_name+box_posn;
                                                                      box_name=box_name+"']";
                                                                      $(box_name).prop('checked', true);
                                                            
                                                                    

                                                                    }


                                                                  }

                                                       }

                                                    








                                          }




                                   }



                                 }





                           }



                         // iterate through all objects inside campaign_hours
                         var delivery_hours=[];
                         var delivery_hours_counter=0;

                         for(var delivery_hour in campaign_hours ){

                            delivery_hours[delivery_hours_counter]=campaign_hours[""+delivery_hour+""];

                            if(delivery_hours[delivery_hours_counter]=="No time"){

                              break;
                            }
                            delivery_hours_counter++;


                         }

                         //Now display time boxes according to the number delivery times
                         if(delivery_hours_counter==0){
                            displayTimeOfRunningBoxes(1);
                           $("#hour00").value('00');
                           $("#minutes00").value('00');
                           $("#frequencyofrunningselected").val(1); 


                         }

                         else
                           displayTimeOfRunningBoxes(delivery_hours_counter);

                           $.each(delivery_hours, function(i,val) { 
                            var hour_key="#hour";
                            var minutes_key="#minutes";
                            var hour=delivery_hours[i].substring(0,2);
                            var minutes=delivery_hours[i].substring(3,5);
                          
                            hour_key=hour_key+i;
                            minutes_key=minutes_key+i;   

                            $(hour_key).val(hour);  
                            $(minutes_key).val(minutes); 

                            $("#frequencyofrunningselected").val(delivery_hours_counter); 

                            if(delivery_hours_counter<=5);
                            else{

                               $("#userdefinedfrequency_box").val(delivery_hours_counter);

                            }          

                       
                         
                           });





                         //Now iterate through all objects inside targeted_audience

                         var groups=[];

                         var groups_counter=0;
                         for(var grp in targeted_audience){
                           var item={};
                           item["GK"]=targeted_audience[""+grp+""]["GroupKey"];
                           item["GN"]=targeted_audience[""+grp+""]["GroupName"];
                           groups[groups_counter]=item;
                           //selectgroup.val(item[0]);
                           groups_counter++;



                         }
                         //var selected_items="Current Selecte Groups&#013;";
                         var item_counter=1;


                         $.each(groups, function(i,val) { 
                          //alert(val.GK);

                            switch(val.GK)
                            {
                              case '0': $('#campaigntargetallsms').prop("selected", true); break;
                              default: $('#gid_'+val.GK).prop("selected", true); 


                            }
                        
                           });

                         // alert(selected_items);
                          // $("#selectedGroupsTooltip").prop("title",selected_items);

                          //var selected_groups_count = $("#campaigntargetsms :selected").length;
                          var selected_groups_count =groups_counter;
                          $("#numOfGroups").val(selected_groups_count);
                         
                           //$('').prop("selected", true); 
                        
                        
                        if(retrieved_end_date=="");
                        else
                        {
                          //Toggle 

                          $("input[type='radio'][name='lifeofcampaign']").attr("checked",1);
                           showHideCampaignEnd(1);


                        }

                          msgtxtobj=resjson[""+x+""]["messagestxt"];
                          var html_str="";
                          if(total_no_msg_box>0){
                            
                            removeMsgBoxes();
                            total_no_msg_box=0;
                          }
                             
                          for(var y in msgtxtobj)
                          {
                            addMessageBox(msgtxtobj[""+y+""]);
                          //alert(msgtxtobj[""+y+""]);
                          campaign_msg_box="<textarea id=\"campaign_descr\"  rows=\"5\" cols=\"20\" id=\"";
                          campaign_msg_box=campaign_msg_box+y;
                          campaign_msg_box=campaign_msg_box+"\" maxlength=\"200\">" ;
                          campaign_msg_box=campaign_msg_box+msgtxtobj[""+y+""];
                          campaign_msg_box=campaign_msg_box+"</textarea>" ;
                            
                           html_str=html_str+"<tr>\n";
                           html_str=html_str+"\n  <td>";
                           //html_str=html_str+msgtxtobj[""+y+""];
                           html_str=html_str+campaign_msg_box;
                           html_str=html_str+"\n  </td>";
                           html_str=html_str+"<tr>\n";
                           //total_no_msg_box=total_no_msg_box+1;

                          }
                          //alert(html_str);
                          //$("#camp_msg_grp").html(html_str);
                          //$("#del_msg_boxes").show();

                          break;

                      }

    }





//displayCampaignsContent(EDITING_MODE,campaign_id);
/*
setTimeout(function(){
           searchCampaignTable();
          },100);
//Now retrieve group content for editing
current_menu=record_id;
*/

};


/*
$(document).ready(function(){
  $(".searchabletable").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $(".mysearchabletable tr").filter(function() {
      alert("");
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

*/
/*
    $( function() {
    $( "#smartsmspopup" ).dialog({
      autoOpen: false,
      show: {
        effect: "blind",
        duration: 1000
      },
      hide: {
        effect: "explode",
        duration: 1000
      }
    });
 
    $( "#smartsmspopup" ).on( "click", function() {
      alert("Got here");
      $( "#dialog" ).dialog( "open" );
    });
  } ); */

    $( function() {

    //for profile dialog

      $( "#profiledialog" ).dialog({
      autoOpen: false,
      dialogClass:'profiledialogclass',
      show: {
        effect: "blind",
        duration: 500
      },
      hide: {
        effect: "explode",
        duration: 500
      }
    });

    $( "#smsdialog" ).dialog({
      autoOpen: false,
      dialogClass:'smsdialogclass',
      show: {
        effect: "blind",
        duration: 500
      },
      hide: {
        effect: "explode",
        duration: 500
      }
    });


    $("#smstemplatesdialog" ).dialog({
      minWidth: 500,
      minHeight:500,
      autoOpen: false,
      dialogClass:'templatedialogclass',
      show: {
        effect: "blind",
        duration: 500
      },
      hide: {
        effect: "explode",
        duration: 500
      }
    });
 
  } ); 




var initiateSMSDialog=function(sms_type,option1,option2){
   
   bindSMSBroadCaster(sms_type,option1,option2);

  
  /*
    $( ".startsmspopup" ).on( "click", function() {
     
      $( "#smsdialog" ).dialog( "open" );
    });*/

};


  



	
