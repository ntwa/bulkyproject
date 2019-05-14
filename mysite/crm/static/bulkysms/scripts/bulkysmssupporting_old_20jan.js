//Declaration of site global variables
var VIEWING_MODE=1;
var EDITING_MODE=2;
var current_menu=null;

 var site="http://localhost:8000/asasbulkysys/";

$( document ).ready(function() {
    initializeMenu();
});



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

var typingFeedback=function(){

$("#myprogressbar").html('<b><i style=\"color:green;\">Typing...</i></b>');

};

var clearFeedback=function(status){

$("#myprogressbar").html('&nbsp;');
var msgstr=$("#addresssmsbox").val()
if((msgstr.length>0)&&(status))
   $("#myprogressbar").html('<b><i style=\"color:green;\">Message Ready? Send it!!</i></b>');
     


};

//send one sms from the address book
var sendOneSMS=function()
{

     jsonObject={MessageBody:$("#addresssmsbox").val(),MobNo:$("#primarymobile").val()};
      $("#myprogressbar").html('');
      addLoadingCircle();
      var urlstr=site;
      urlstr=urlstr+"jsondata/SS/";// Retrieve
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
//For retrieving individual address item from local storage
var retrieveAddressItem=function (item)
{
 //alert(item);
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
    ul_list_close_tag= ul_list_close_tag+"\n<br></br><a href=\"#popupaddressbooksms\" data-rel=\"popup\"><img id=\"startsmspopup\" src=\"http://localhost:8000/static/bulkysms/images/smsicon.jpg\"></a>";   

    }

    ul_list_close_tag= ul_list_close_tag+marker_description;
    phone_numbers=phone_numbers+ul_list_close_tag;
    $("#phone-numbers").html(phone_numbers);
    //alert(phone_numbers);
    break;
    }

 }

};

//Retrieve address Book from Django Python App via our defined REST API
var retrieveAddressBookContent=function ()
{     
     
      var urlstr=site;
      urlstr=urlstr+"jsondata/RABC/";
      var jsonObjects={Empty:"Nothing"};

      var request = $.ajax({
                            url:urlstr,
                            method: "POST",
                            data: jsonObjects,
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
                        localStorage.setItem("Contacts",JSON.stringify(addressbookobj));
                       

                        //alert("Local Storage Supported");
                      }

                    //addressbookobj1=JSON.parse(localStorage.getItem("Contacts"))
                    for(var x in addressbookobj)
                    {
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
                        inner_html=inner_html+"</a></li>\n"
                        
                      
                        }
                       
                      
                      }
                      
                      if(inner_html.length>0) //Then it means we have atleast one name to append for names that start with the current alphabet
                      {
                       var current_alphabet_id="#";

                       current_alphabet_id=current_alphabet_id+current_alphabet;
                       current_alphabet_id=current_alphabet_id+current_alphabet;
                       $(current_alphabet_id ).html(inner_html);


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
var retrieveAddressBookTemplate=function ()
{     
     
      var urlstr=site;
      urlstr=urlstr+"jsondata/RABT/";// Retrieve
      $.ajax({
             url: urlstr,
             cache: false
             })
            .done(function( html ) {
            $( "#main-content" ).html('');
            $( "#main-content" ).append(html);
            
                           //$(document).ready(function () {
                           // Action after append is completly done
                           //Now work on the slider
                           //handleSliderNav();
                            //});
             retrieveAddressBookContent();
         
             });



  };
//user interface for selecting members to assign
var assignMembersToGroupInterface=function(group_id){



};


var saveGroupMembers=function(group_id){



};


var retrieveGroupAllocatioTemplate=function(){


      var urlstr=site;
      urlstr=urlstr+"jsondata/RGAT/";// Retrieve Group Allocation Template
      $.ajax({
             url: urlstr,
             cache: false
             })
            .done(function(html) {
            $( "#main-content" ).html('');
            $( "#main-content" ).append(html);//Now append that interface
            
                           //$(document).ready(function () {
                           // Action after append is completly done
                           //Now work on the slider
                           //handleSliderNav();
                            //});
             //retrieveAllContacts();
         
             });



};

var retrieveAllContacts=function(){


      var group_id="-1";
      var urlstr=site;
      urlstr=urlstr+"jsondata/RABC/";
      var jsonObjects={GroupID:"2"};

     
      var request = $.ajax({
                            url:urlstr,
                            method: "POST",
                            data: JSON.stringify(jsonObjects),
                            dataType: "jsonp"
                    });
      
      request.done(function( contactsobj ) {
                    alert("got here");
                  
                    var contacts = new Array();
                    var html_str="";
                   
                  
                    var contacts_counter=0;
                    if (Modernizr.localstorage) {
                        //store into a local storage
                        localStorage.setItem("AllContancts",JSON.stringify(contactsobj));
                       

                        //alert("Local Storage Supported");
                      }



                    //addressbookobj1=JSON.parse(localStorage.getItem("Contacts"))
                    for(var x in contactsobj)
                    {
                        var contact_names="";
                        var contact_ward="";
                        var contact_district="";

                        var contact_region="";
                        var contact_country="";


                        //Get name
                        contact_names=contact_names+contactsobj[""+x+""]["first_name"];
                        contact_names=contact_names+ " ";
                        contact_names=contact_names+contactsobj[""+x+""]["last_name"];
                        //contact_ids[name_counter]=addressbookobj[""+x+""]["ContactID"];
                        //address_objects[name_counter]=""+x+"";

                        //get ward
                         contact_ward=contact_ward+contactsobj[""+x+""]["ward"];

                        //get district

                         contact_district=contact_district+contactsobj[""+x+""]["district"];

                        //get region

                         contact_region=contact_region+contactsobj[""+x+""]["region"];



                         contact_country=contact_country+contactsobj[""+x+""]["country"];
                         
                       
                         //contacts[contacts_counter]=new Array();
                         //contacts[contacts_counter]["Name"]=contact_names;
                         //contacts[contacts_counter]["Ward"]=contact_ward;
                         //contacts[contacts_counter]["District"]=contact_district;
                         //contacts[contacts_counter]["Region"]=contact_region;
                         //contacts[contacts_counter]["Country"]=contact_country;
                         html_str=html_str+"\n<tr>\n";
                         html_str=html_str+"    <td>";
                         html_str=html_str+contact_names;
                         html_str=html_str+"    </td>\n";


                         html_str=html_str+"    <td>\n";
                         html_str=html_str+contact_ward;
                         html_str=html_str+"    </td>\n";


                         html_str=html_str+"    <td>\n";
                         html_str=html_str+contact_district
                         html_str=html_str+"    </td>\n";

          
                         html_str=html_str+"    <td>\n";
                         html_str=html_str+contact_region;
                         html_str=html_str+"    </td>\n";

                         html_str=html_str+"    <td>\n";
                         html_str=html_str+contact_country;
                         html_str=html_str+"    </td>\n";

                         html_str=html_str+"\n</tr>\n";
                         

                       

                         
                    }
                    //alert(html_str);
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
      urlstr=urlstr+"jsondata/SGR/";// Retrieve
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
 //if(current_menu==record_id)
 //    return;  

//alert("Edit Group.."+group_id);

//now call a function to save records


displayGroupsContent(EDITING_MODE,group_id);

setTimeout(function(){
           searchGroupTable();
          },100);
//Now retrieve group content for editing
current_menu=record_id;

};


var deleteGroup=function(group_id,menu_id){
 var record_id=menu_id+"";
 record_id=record_id+group_id;
 //if(current_menu==record_id)
  //   return;
//alert("Delete Group.."+group_id);
current_menu=record_id;

};


var expandGroup=function(group_id,menu_id){

 var record_id=menu_id+"";
 record_id=record_id+group_id;
 if(current_menu==record_id)
     return;
//alert("Expand Group.."+group_id);
retrieveGroupAllocatioTemplate();
//$.noConflict();


setTimeout(function(){retrieveAllContacts();},20);

setTimeout(function(){$('#example').DataTable();},1000);
current_menu=record_id;

};

//Retrieve Content for groups
var retrieveGroupsContent=function ()
{     
     
     jsonObject={Empty:""};
     
      var urlstr=site;
      urlstr=urlstr+"jsondata/RGC/";// Retrieve
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
                    var html_str="\n"
              
                    var resjson=JSON.parse(localStorage.getItem("Groups"));
                    //alert("Group Content Loaded"+resjson["AD00"]["group_description"]);
                    for(var x in resjson)
                    {
                        var retrieved_group_id=resjson[""+x+""]["GroupID"];
                        var retrieved_group_name="";
                        var retrieved_group_descr




                        //deciding on displaying mode whether the content should be viewing in editing mode or just normal viewing mode
                        if((display_type==EDITING_MODE)&&(group_id==retrieved_group_id)){
                         //alert("Got here");
                          // this is editing mode so it should be viewed in text box ready for editing
                           retrieved_group_name="<input type=\"text\" value=\""+resjson[""+x+""]["group_name"]+"\" id=\"group_name_edit\" maxlength=\"50\">" ;
                          //retrieved_group_descr=resjson[""+x+""]["group_description"]; 
                          retrieved_group_descr="<textarea id=\"group_descr_edit\"  rows=\"5\" cols=\"20\" maxlength=\"200\">"+resjson[""+x+""]["group_description"]+"</textarea>" ;



                        }
                        else{
                          retrieved_group_name=resjson[""+x+""]["group_name"];  ;
                          retrieved_group_descr=resjson[""+x+""]["group_description"];  

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

                        html_str=html_str+"\n  <td>"
                        html_str=html_str+"N/A";
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

                        html_str=html_str+"\n   <button style=\"font-size:24px;color:blue\" onclick=\"editGroup('";
                        html_str=html_str+resjson[""+x+""]["GroupID"];
                        html_str=html_str+"','EDITGROUP')\"><i class=\"fa fa-pencil\"></i></button>";


                        html_str=html_str+"\n   <button style=\"font-size:24px;color:red;\" onclick=\"deleteGroup('";
                        html_str=html_str+resjson[""+x+""]["GroupID"];
                        html_str=html_str+"','DELETEGROUP')\"><i class=\"fa fa-trash-o\"></i></button>";
                    
                        html_str=html_str+"\n   <button style=\"font-size:24px;color:green;\" onclick=\"expandGroup('";
                        html_str=html_str+resjson[""+x+""]["GroupID"];
                        html_str=html_str+"','EXPANDGROUP')\"><i class=\"glyphicon glyphicon-expand\"></i></button>";
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

var resetToHome=function(menu_id)
{

 if(current_menu==menu_id)
     return; 
 var homeStr="<h2 style=\"color:green;\"><i>Handle relationship with customers through SMS, email and social media</i></h2>\n<!--Declare pop up for sending message-->";

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

var scheduleBulkyMessages=function(menu_id)
{


alert("Schedule Bulky Messages");
if(current_menu==menu_id)
     return; 
current_menu=menu_id;
};

var manageSettings=function(menu_id)
{

alert("Manage Settings");

if(current_menu==menu_id)
     return; 
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

 

alert("Manage Campaigns");
if(current_menu==menu_id)
     return; 
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
            
        


		       

			 switch(item)

			  {
                                case "Home":resetToHome(item);break;
			        case "AddressBook":manageAddressBook(item);break;
				case "Scheduler":scheduleBulkyMessages(item);break;
                                case "Settings":manageSettings(item);break;
                                case "Grouping":manageGroups(item);break;
				case "Campaign":manageCampaigns(item);break;

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
