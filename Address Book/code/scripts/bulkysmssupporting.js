$( document ).ready(function() {
    initializeMenu();
//alert("Bingo");
});


var manageAddressBook=function()
{

alert("Manage Address Book");

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

alert("Manage Groups");

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



	
