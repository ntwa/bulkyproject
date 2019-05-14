//First check if the string is separated by a white space

 var white_space_posn=filterstr.indexOf(" ");
 //Now check if there are any characters coming after white space. 


 if(white_space_posn>=0)
 {
   white_space_posn=white_space_posn+1;
   //Now check if the position after the discovery of white space is the same as the lenght of the string. If it is it means the user is yet to type the second part of the searched keyword 
   if (white_space_posn==filterstr.length)
      //get rid of white space 
      {
        white_space_posn=white_space_posn-1;
        filterstr=filterstr.substring(0,white_space_posn);
        white_space_posn=-1;

        
      }
    else{

      //do spliting of string into two separate parts so that we can search using both first name and last name.
        var fname_part = filterstr.split(" ")[0];
        var lname_part = filterstr.split(" ")[1];
        var split_str=filterstr.split(" ")
        var split_counter=1
        while((lname_part=="") && (split_counter<split_str.length)) // if it is blank then only consider first name while searching
        {
        
         lname_part=split_str[split_counter];
        alert(lname_part);

         split_counter++;
        //white_space_posn=white_space_posn-1;
        //filterstr=fname_part;
        //white_space_posn=-1;

        }
        if(split_counter<split_str.length)
        {
         //it means we have encountered some text after at least one white space. We can consider that text as part  of the last name
         //do nothing

         

        }
        else
        {//It means the white spaces are throughout for the last name. Therefore only consider first name
        
          filterstr=fname_part;
          white_space_posn=-1; //We reset this to -1 so that we only conider first namew

        }
        //else
        //{ // then consider both first name and last name
        //  fname_part=fname_part.toUpperCase();
        //  lname_part=lname_part.toUpperCase();

       // }




    }


 }
  