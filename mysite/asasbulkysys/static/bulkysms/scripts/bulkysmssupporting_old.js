//Declaration of site global variables

 var site="http://localhost:8000/asasbulkysys/";

$( document ).ready(function() {
    initializeMenu();
});


var stillLoading=0; // For keeping track if there is an operation waiting to be completed by the server before returning result to the client
var display_interval=0;



var appendEmptyCanvas=function(){

	var table_str="<table>";
	table_str=table_str+"<tr><td>";
	var canvas_str="<canvas id='loadingprogress'  width='200' height='100' style='border:1px solid #d3d3d3;'>Wait Page Looading...</canvas>";
	table_str=table_str+canvas_str;
	table_str=table_str+"</td></tr>";
	table_str=table_str+"</td></tr>";
 	$("#progresspopup").html('');
 	$("#progresspopup").append(table_str);
        $("#progresspopup").popup("open");
        alert("dddd");




};



var displayDialogBox=function()
{
       
	block_horizontal_position=10;
	var c = document.getElementById("loadingprogress");
	var ctx = c.getContext("2d");
	ctx.font = "12px Arial";
	ctx.fillText("Wait!! -- While it completes!!",10,50);
	var counter=0;
	clearInterval(display_interval);
	display_interval=setInterval(function(){
try{
	var c= document.getElementById("loadingprogress");
	var ctx = c.getContext("2d");
	ctx.fillStyle = "blue";
	ctx.fillRect(block_horizontal_position,60,5,5);
	block_horizontal_position=block_horizontal_position+5;

	ctx.fillStyle = "white";
	ctx.fillRect(block_horizontal_position,60,10,10);
	block_horizontal_position=block_horizontal_position+5;


	if(counter==11){
	    clearInterval(display_interval);

	   }
	counter=counter+1;




}
catch(err){
 	clearInterval(display_interval);
	}
	},1000);


};

 var showProgressDialog=function(){

     appendEmptyCanvas();
     displayDialogBox();


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



//send one sms from the address book
var sendOneSMS=function()
{

     jsonObject={MessageBody:$("#addresssmsbox").val(),MobNo:$("#primarymobile").val()};
     //alert($("#primarymobile").val());
     //alert($("#addresssmsbox").val());
     //return;
      //showProgressDialog();
     //$( "#progresspopup" ).dialog();
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
             alert("Message Sent");
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
             //alert("Group Content Loaded"+resjson["AD00"]["group_description"]);


                
                    //var contact_ids = [];
                    var group_objects=[];
                    var group_counter=0;
                    var html_str="\n"
              
                    //addressbookobj1=JSON.parse(localStorage.getItem("Contacts"))
                    for(var x in resjson)
                    {
                        html_str=html_str+"<tr>\n";

                        html_str=html_str+"\n  <td>";
                        html_str=html_str+resjson[""+x+""]["group_name"];
                        html_str=html_str+"\n  </td>";

                        //var long_str=resjson[""+x+""]["group_description"];

                        //now divide the string into 

                        //var n = long_str.length; 
                        
                        
                        html_str=html_str+"\n  <td style=\"overflow:hidden; width:200px;\">"
                        html_str=html_str+resjson[""+x+""]["group_description"];
                        html_str=html_str+"\n  </td>";

                        html_str=html_str+"\n  <td>"
                        html_str=html_str+"N/A";
                        html_str=html_str+"\n  </td>";



                        html_str=html_str+"\n	<td class=\"iconbuttons\">";
                        html_str=html_str+"\n   <button style=\"font-size:24px;color:blue\"><i class=\"fa fa-pencil\"></i></button>";


                        html_str=html_str+"\n   <button style=\"font-size:24px;color:red;\"><i class=\"fa fa-trash-o\"></i></button>";
                    
                        html_str=html_str+"\n   <button style=\"font-size:24px;color:green;\"><i class=\"glyphicon glyphicon-expand\"></i></button>";
                        html_str=html_str+"\n   </td>";

                        //html_str=html_str+"\n  <td>"
                        //html_str=html_str+resjson[""+x+""]["GroupID"];
                        //html_str=html_str+"\n  </td>";


                        html_str=html_str+"\n</tr>\n";
                    
                    
                        //group_objects[group_counter]=""+x+"";
                        //group_counter=group_counter+1;
                    }
                   // alert(html_str);
                   $("#groups").html(html_str);

          

             });



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



  };
         
      /*
	    jQuery.ajax({
      				url: urlstr,
     				  type: "POST",
              dataType: 'jsonp',
      				contentType: "application/json",
      				data: JSON.stringify(jsonObjects),
      				success: function(result) {
     						//Write your code here
     				         //clickscounter=0;
     						//pointscounter=0;
                        //alert("Bingo");
     						        //alert(result);
     						//showMealsGoal(result);
     						
     						//updateLocalStorage("MealsGoal",result,"Goal")
     						
     						
     						 } //end of success
					});//end of jQuery.ajax
	
        */               


//};//end of retrieveAddressBook

var resetToHome=function()
{
 var homeStr="<h2 style=\"color:green;\"><i>Handle relationship with customers through SMS, email and social media</i></h2>\n<!--Declare pop up for sending message-->";

$("#main-content").html(homeStr);
   



}


var manageAddressBook=function()
{

//alert("Manage Address Book");
retrieveAddressBookTemplate();

};

var scheduleBulkyMessages=function()
{

alert("Schedule Bulky Messages");

};

var manageSettings=function()
{

alert("Manage Settings");

};

var manageGroups=function()
{

//alert("Manage Groups");
retrieveGroupsTemplate();
retrieveGroupsContent();

};

var manageCampaigns=function()
{

alert("Manage Campaigns");

};


var initialized=false;

//provide links to menus
var initializeMenu=function(){
 
   
if(!initialized)//check if the menu has note been prviously initialized
    {
  
           initialized=true;
       
          $(".menuimage").on("click", function(event){

             var item=$(this).attr("value");

        


		       

			 switch(item)

			  {
                                case "Home":resetToHome();break;
			        case "AddressBook":manageAddressBook();break;
				case "Scheduler":scheduleBulkyMessages();break;
                                case "Settings":manageSettings();break;
                                case "Grouping":manageGroups();break;
				case "Campaign":manageCampaigns();break;

			         //case "MainPage":$.mobile.changePage( "#pageone", { transition: "slide", changeHash: false });break;
               
			 	      
				

			

			   

			   default: alert("Functionality Under Construction");

			   }

			   

			   $("img").toggle();

			   $("img").show();

			   

            });
  
  }

//end function initialize
}



	
