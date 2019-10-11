#!/usr/bin/env python
import datetime
import sys,json

from sqlalchemy.orm import sessionmaker


from collections import OrderedDict

from bulkysms.database.base  import Base
from bulkysms.database.dbinit import db,dbconn

import bulkysms.database.address_book_module

import bulkysms.database.sms_feedback_module

Base.metadata.create_all(db)

from bulkysms.database.address_book_module import AddressBook,MobileDetails,EmailDetails,GroupMember
from bulkysms.database.sms_feedback_module import Campaign


class switch(object):
          value = None
          def __new__(class_, value):
                    class_.value = value
                    return True
def case(*args):
          return any((arg == switch.value for arg in args))

class AddressBookManager:
     def __init__(self,myjson):
          self.myjson=myjson


     def binary_search(self,item_list,item):
	  first = 0
	  last = len(item_list)-1
	  found = False
	  while( first<=last and not found):
               mid = (first + last)/2
	       if item_list[mid] == item :
		    found = True
	       else:
		    if item < item_list[mid]:
			 last = mid - 1
		    else:
			 first = mid + 1	
	  return found





     def insertionSort(self,alist):

   	  for i in range(1,len(alist)):

               #element to be compared
       	       current = alist[i]

               #comparing the current element with the sorted portion and swapping
               while i>0 and alist[i-1]>current:
                    alist[i] = alist[i-1]
                    i = i-1
                    alist[i] = current

               #print(alist)

          return alist
 
     def verify_country_code_format(self,country,mobile_no):
          
          mob_len=len(mobile_no)
          start_point=mob_len-9 # get the last nine digits of a mobile number
          last_nine_chars=mobile_no[start_point:mob_len]
          if mob_len>10 and mob_len==13:
	       #check if the number starts with a plus sign to see the presence of a country code
               first_two_chars=mobile_no[0:2]
               if "+" in first_two_chars:
                    return mobile_no #No need to modify the mobile number because the number already contains a country code
               else:
                    return "Error: The format of a mobile number '%s' is not recognized"%mobile_no
          elif mob_len==10:
               pass
          elif mob_len==9:
               #check if there is a preceding zero. If there isn't then probably a number was just entered without a country code and a preceding for service provider code was also ommited. This can happen for data from spreadsheets files.
               first_char=mobile_no[0:1]
               if "0" in first_char:
                    return "Error: The format of a mobile number '%s' is not recognized"%mobile_no
               else:
                    mobile_no="0%s"%mobile_no #just put the preceding zero for easier processing 
          else:
              return "Error: The format of a mobile number '%s' is not recognized"%mobile_no
                   
              
          
          country_code="+255" #default country code
          if switch(country):
                                                                    
               if case("Tanzania"):
                    
                    pass # by default the country code is set to Tanzania. No need to rest it if the country is Tanzania
                    
                                                     
               elif case("Kenya"):
                    country_code="+254"
               elif case("Uganda"):
		    country_code="+256"
               elif case("Rwanda"):
		    country_code="+250"
	       elif case("Rwanda"):
		    country_code="+260"
		    
                    
          modified_number="%s%s"%(country_code,last_nine_chars) # append the last nine digits with country code
          return modified_number




     def retrieveContactDetailsFromDB(self):
           
          #The tuples are used for definition of JSON objects
          address_tuple={}
          mobile_tuple={}
          email_tuple={}

            #These counters are important when appending address and its other details such as mobile numbers and email addresses
            #The first part of the address stay on level 1. The additional part of addresses (mobile numbers and email addresses) are expanded to level two
          level_one_json_counter=0
          level_two_json_counter=0
          key1="AD" #part of forming a key to json object for the entire contact/address
          key2="MBEA" #part of forming a key to json object to only the mobile or address parts of the address
          #key2b="EA" #part of forming a key to json object to only the email part of the address
           
	 
	  #get all contacts and their respective details from the database
          try:
               company_id=self.myjson["CompanyID"]
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               result={}    

               #result["GroupID"]=self.myjson["GroupID"]
               #result["G"]=self.myjson["Option"] 
               #return (json.JSONEncoder().encode(result))                
               # querying for a record if it exists already.

               if self.myjson["GroupID"] =='-1' and self.myjson["Option"] =='-1':
               	    res= session.query(AddressBook).filter(AddressBook.company_id==company_id).order_by(AddressBook.first_name).order_by(AddressBook.last_name).all()
               
                   
               
               	    if len(res) ==0:
                         session.close()
                         engine.dispose()
                         dbconn.close()
                         contacterror={}
                         contacterror["ContactID"]=-1
                         result["AD00"]=contacterror
                         return (json.JSONEncoder().encode(result))
	            else: 
                         for addrbk_rec in res:
			 
                              #start the second query to get mobile details
                              mob_res=session.query(MobileDetails).filter(MobileDetails.contact_id==addrbk_rec.id).order_by(MobileDetails.id).all()
                              level_two_json_counter=0 #reset counter to zero 
                              mobile_tuple={} #reset the tupple for holding phone numbers
                              for mob_rec in mob_res:
                                   mobile_tuple[key2+"%d"%level_two_json_counter]=mob_rec.mobile_number
                                   level_two_json_counter=level_two_json_counter+1



                              #start the third query to get email details
                              email_res=session.query(EmailDetails).filter(EmailDetails.contact_id==addrbk_rec.id).order_by(EmailDetails.id).all() 
                              level_two_json_counter=0 #reset counter to zero
                              email_tuple={} #Reset tuple for holding email addresses
                              for email_rec in email_res:
                                   email_tuple[key2+"%d"%level_two_json_counter]=email_rec.email_address
                                   level_two_json_counter=level_two_json_counter+1

                         
			  
                              #Now  put both mobile tuple and email tuple to the main address tuple
                              if level_one_json_counter<10:
                                   key1="AD0"# append a zero. This is important in ordering keys alphabetically
                              else:
                                  key1="AD"
                              dobstr="%s"%addrbk_rec.birth_date #convert date to string

                              address_tuple[key1+"%d"%level_one_json_counter]={"ContactID":addrbk_rec.id, "first_name":addrbk_rec.first_name, "middle_name":addrbk_rec.middle_name, "last_name":addrbk_rec.last_name, "gender":addrbk_rec.gender,"birth_date":dobstr, "ward":addrbk_rec.ward, "district":addrbk_rec.district, "region":addrbk_rec.region, "country":addrbk_rec.country, "mobiles":mobile_tuple, "emails":email_tuple}
                              level_one_json_counter=level_one_json_counter+1	
         
                         
                         session.close()  
                         engine.dispose()   
                         dbconn.close()
                         #we wind up the retrieve operation.  
                         #return json.JSONEncoder().encode(address_tuple) 
                         return(json.JSONEncoder().encode(OrderedDict(sorted(address_tuple.items(), key=lambda t: t[0]))))   
               elif self.myjson["GroupID"] =='-1' and self.myjson["Option"] <>'-1':
                   
		    group_id=int(self.myjson["GroupID"])
                    group_id_exclude=int(self.myjson["Option"])
                    contact_ids_exclude=[]
                    #first get all contacts IDs that need to be excluded
                    res= session.query(AddressBook,GroupMember).filter(AddressBook.id==GroupMember.contact_id).filter(GroupMember.group_id==group_id_exclude).filter(AddressBook.company_id==company_id).order_by(AddressBook.first_name).order_by(AddressBook.last_name).all() 
                    if len(res) ==0:
                         #The group, then get everyone else
                         res= session.query(AddressBook).order_by(AddressBook.first_name).order_by(AddressBook.last_name).all()
                         for addrbk_rec in res:
                              #                                                       
                              if level_one_json_counter<10:
                                   key1="AD0"# append a zero. This is important in ordering keys alphabetically
                              else:
                                  key1="AD"
                              dobstr="%s"%addrbk_rec.birth_date #convert date to string

                              address_tuple[key1+"%d"%level_one_json_counter]={"ContactID":addrbk_rec.id, "first_name":addrbk_rec.first_name, "middle_name":addrbk_rec.middle_name, "last_name":addrbk_rec.last_name, "ward":addrbk_rec.ward, "district":addrbk_rec.district, "region":addrbk_rec.region, "country":addrbk_rec.country}
                              level_one_json_counter=level_one_json_counter+1
                         
                         session.close()  

                         engine.dispose()   
                         dbconn.close()
                         #we wind up the retrieve operation.  
                         #return json.JSONEncoder().encode(address_tuple) 
                         return(json.JSONEncoder().encode(OrderedDict(sorted(address_tuple.items(), key=lambda t: t[0])))) 
                         
                         #session.close()
                         #engine.dispose()
                         #dbconn.close()
                         #result["AD00"]["ContactID"]=-1
                         #return (json.JSONEncoder().encode(result))
	            else: 
                         
                         for addrbk_rec,group_rec in res: 
                              contact_ids_exclude.append(addrbk_rec.id);
                              contact_ids_exclude=self.insertionSort(contact_ids_exclude)
                        
                            

                         res= session.query(AddressBook).filter(AddressBook.company_id==company_id).order_by(AddressBook.first_name).order_by(AddressBook.last_name).all()
                         for addrbk_rec in res:
                              #do a binary search to check if the retrieved id belong to the list of contact ids t be excluded
                              found=self.binary_search(contact_ids_exclude,addrbk_rec.id)
                              if found == True:
                                   continue # skip this record

                                                       
                              if level_one_json_counter<10:
                                   key1="AD0"# append a zero. This is important in ordering keys alphabetically
                              else:
                                  key1="AD"
                              dobstr="%s"%addrbk_rec.birth_date #convert date to string

                              address_tuple[key1+"%d"%level_one_json_counter]={"ContactID":addrbk_rec.id, "first_name":addrbk_rec.first_name, "middle_name":addrbk_rec.middle_name, "last_name":addrbk_rec.last_name, "ward":addrbk_rec.ward, "district":addrbk_rec.district, "region":addrbk_rec.region, "country":addrbk_rec.country}
                              level_one_json_counter=level_one_json_counter+1
                         
                         session.close()  
                         engine.dispose()   
                         dbconn.close()
                         #we wind up the retrieve operation.  
                         #return json.JSONEncoder().encode(address_tuple) 
                         return(json.JSONEncoder().encode(OrderedDict(sorted(address_tuple.items(), key=lambda t: t[0]))))   	
                    
               else:
                   
                    group_id=self.myjson["GroupID"]
                    res= session.query(AddressBook,GroupMember).filter(AddressBook.id==GroupMember.contact_id).filter(GroupMember.group_id==group_id).filter(AddressBook.company_id==company_id).order_by(AddressBook.first_name).order_by(AddressBook.last_name).all() 
                    if len(res) ==0:
                         session.close()
                         engine.dispose()
                         dbconn.close()
                         contacterror={}
                         contacterror["ContactID"]=-1
                         result["AD00"]=contacterror
                         return (json.JSONEncoder().encode(result))
	            else: 
                         for addrbk_rec,group_rec in res: 
                                                            
                              if level_one_json_counter<10:
                                   key1="AD0"# append a zero. This is important in ordering keys alphabetically
                              else:
                                  key1="AD"
                              dobstr="%s"%addrbk_rec.birth_date #convert date to string

                              address_tuple[key1+"%d"%level_one_json_counter]={"ContactID":addrbk_rec.id, "first_name":addrbk_rec.first_name, "middle_name":addrbk_rec.middle_name, "last_name":addrbk_rec.last_name, "ward":addrbk_rec.ward, "district":addrbk_rec.district, "region":addrbk_rec.region, "country":addrbk_rec.country}
                              level_one_json_counter=level_one_json_counter+1	
         
                         
                         session.close()  
                         engine.dispose()   
                         dbconn.close()
                         #we wind up the retrieve operation.  
                         #return json.JSONEncoder().encode(address_tuple) 
                         return(json.JSONEncoder().encode(OrderedDict(sorted(address_tuple.items(), key=lambda t: t[0]))))                   
          except Exception as e:
               #if we get here the entire operation has failed so we have wind up all attempts to transact and close the database and then notify the user about the failure.
               session.close()
               engine.dispose()         
               dbconn.close()

               #print "Content-type: text/html\n" 
                                   

               result["ContactID"]=-6
               result["Error"]="Error: %s."%e
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
     


       
     def saveContactInDB(self):
          firstname="" 
          middlename="" 
          lastname="" 
          dob="" #Date of Birth
          gender=""
          ward="" 
	  district=""
	  region=""
	  country=""
	  mobile1=""
	  mobile2=""
          mobile3=""
          email1=""
	  email2=""
	  email3=""
          result={}
          allow_insert=1
          
          # Get data from fields
          try:
               contact_id=self.myjson["contact_id"]             
               first_name=self.myjson["First Name"] 
               middle_name=self.myjson["Middle Name"] 
               last_name=self.myjson["Last Name"] 
               dob=self.myjson["DOB"] 
               gender=self.myjson["Gender"]
               
           
               ward=self.myjson["Ward"]
               district=self.myjson["District"]
	       region=self.myjson["Region"]
	       country=self.myjson["Country"]
                
               mobile1=self.myjson["Mobile Phone #1"] 
               mobile2=self.myjson["Mobile Phone #2"] 
               mobile3=self.myjson["Mobile Phone #3"]  
            
	       email1=self.myjson["Email Address #1"]
	       email2=self.myjson["Email Address #2"]
	       email3=self.myjson["Email Address #3"]
               company_id=self.myjson["CompanyID"]       
               
              
               
               #first_name="Ntwa"
               #middle_name="Andalwisye" 
               #last_name="Katule" 
               #dob="2013-02-23"
               #gender="Male"
               #ward="Mbuyuni"
               #district="Morogoro"
	       #region="Morogoro"
	       #country="Tanzania"
	       #mobile1="0718255585"
               #mobile2="0742340759"
               #mobile3="0656867676"
               #email1="katulentwa@gmail1.com"
	       #email2="nkatule@aru.ac.tz"
	       #email3="lucatec.ceo@gmail.com"

               #Ensure mobile numbers are appended with
               #mobile_numbers=[mobile1,mobile2,mobile3]
               mobile_numbers=[]

               #Now parse mobile numbers to know how many of them needs to be updated to te database. For instance if no number was provided then we should insert anything. The maximum number of mobile numbers is three

               if mobile1 is None:
                    pass
               else:
                    mobile_numbers.append(mobile1)


               if mobile2 is None:
                    pass
               else:
                    mobile_numbers.append(mobile2)


               if mobile3 is None:
                    pass
               else:
                    mobile_numbers.append(mobile3)

          

               current=0
               for mob_no in mobile_numbers:
		    #first_for_chars=mob_no[0:4]
                    #now check if the country code is appended
                    modified_number=self.verify_country_code_format(country,mob_no)
                    if "Error:" in modified_number:
			 result["message"]="'%s' in editing the contact details for '%s %s %s'. Check if the mobile numbers have been entered correctly. The correct format is (+ABC)(XYZ)(NNNNNN) where '+ABC' stands for country code, XYZ stands for service provider number i.e 0656,0718 etc and NNNNNN stands for the last 8 digits of the mobile phone number. If the error persists contact the developer"%(modified_number, first_name,middle_name,last_name) 
                         return (json.JSONEncoder().encode(result))
                    
                    mobile_numbers[current]=modified_number  
                    current=current+1


               email_addresses=[]

               #Now parse mobile numbers to know how many of them needs to be updated to te database. For instance if no number was provided then we should insert anything. The maximum number of mobile numbers is three

               if email1 is None:
                    pass
               else:
                    email_addresses.append(email1)


               if email2 is None:
                    pass
               else:
                    email_addresses.append(email2)


               if email3 is None:
                    pass
               else:
                    email_addresses.append(email3)                      
                                                                                
         

               
               
               
                
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["opstatus"]={"success":-1,"message":"Error: '%s' encountered in editing the 'Address Book'. If the error persists contact the developer"%e}
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          

          if(first_name=="None") and (middle_name=="None") and (last_name=="None") and (gender=="None") and (dob=="None") and (ward=="None") and (district=="None") and (region=="None") and (country=="None"):
               #print "Content-type: text/html\n" 
               result["opstatus"]={"success":-1,"message":"Error: You did not enter any details"}
               return (json.JSONEncoder().encode(result)) 
               #sys.exit()


          #check if a record exists
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
                                   
               # querying for a record if it exists already.
               res= session.query(AddressBook).filter(AddressBook.id==contact_id).filter(AddressBook.company_id==company_id).first()
               
               if res is None:
                    session.close()
                    engine.dispose()
                    dbconn.close()
               else:
                    #if it exists, then update the record in the database.
                    address_part1_record=res
                    address_part1_record.first_name=first_name
                    address_part1_record.middle_name=middle_name
                    address_part1_record.last_name=last_name
                    address_part1_record.gender=gender
                    address_part1_record.birth_date=dob
                    address_part1_record.ward=ward
                    address_part1_record.district=district
                    address_part1_record.region=region
                    address_part1_record.country=country

		    
                    contact_id=res.id
                    

                    #search all mobile phones to be updated
                    res2= session.query(MobileDetails).filter(MobileDetails.contact_id==contact_id).order_by(MobileDetails.contact_id).order_by(MobileDetails.id).all()
                   
                    
                    
                    #initialize counter to zero before start changing each mobile phone number
                    counter=len(mobile_numbers)
                   
                    if len(res2) ==0:
                         #Incase the contact existed but mobile details didn't exists then attempt to create them
                       
                         #First do the checking
                         count_mobiles=0
                         if mobile1 is None:
                              pass
                         else:
                              res.mobile_number.append(MobileDetails(mobile_numbers[count_mobiles],1))
                              count_mobiles+=1


                         if mobile2 is None:
                              pass
                         else:
                           
                              if count_mobiles==0:
                                   res.mobile_number.append(MobileDetails(mobile_numbers[count_mobiles],1))
                              else:
                                   res.mobile_number.append(MobileDetails(mobile_numbers[count_mobiles],0))
     
                              count_mobiles+=1


                         if mobile3 is None:
                              pass
                         else:
                           
                              if count_mobiles==0:
                                   res.mobile_number.append(MobileDetails(mobile_numbers[count_mobiles],1))
                              else:
                                   res.mobile_number.append(MobileDetails(mobile_numbers[count_mobiles],0))
     
                              count_mobiles+=1


                         #res.mobile_number.append(MobileDetails(mobile_numbers[0],1))
                         #res.mobile_number.append(MobileDetails(mobile_numbers[1],0))
                         #res.mobile_number.append(MobileDetails(mobile_numbers[2],0))
                         session.merge(res)
                     
			 
                    else:
                         count_mobiles=0
                         for mobile in res2:
                              mobile.mobile_number=mobile_numbers[count_mobiles]
                              if count_mobiles==0: 
                                   mobile.is_it_primary_number=1 
  
			      count_mobiles=count_mobiles+1

                             
                         if count_mobiles>2:
                              pass # It means there were three phone numbers in the database and have been updated successfully

                         else: #less than three phone number existed in the database hence add the new ones too
                             # append the new records that were not part of the previous records
                             #initialize index to the last value of counter
                             
                             for index in range(counter):
	   			   #But check this if this number arleady exists or not a duplication of an existing number
                                   mobileexist= session.query(MobileDetails).filter(MobileDetails.contact_id==contact_id).filter(MobileDetails.mobile_number==mobile_numbers[index]).first()
                                   if mobileexist is None:
                                        #Then proceed with appending
                                        res.mobile_number.append(MobileDetails(mobile_numbers[index],0))
                                
                             session.merge(res) 
                                   
                         
		    #search all email addresses to be updated
                    res2= session.query(EmailDetails).filter(EmailDetails.contact_id==contact_id).order_by(EmailDetails.contact_id).order_by(EmailDetails.id).all()
                    email_addresses=[email1,email2,email3]
                    
                    #initialize counter to zero before start changing each email address
                  
     	    	    counter=len(email_addresses)
                    if len(res2)==0:
			 
                         #Incase the contact existed but mobile details didn't exists then attempt to create them

                       
                         #First do the checking
                         count_emails=0
                         if email1 is None:
                              pass
                         else:
                              res.email_address.append(EmailDetails(email_addresses[count_emails],1))
                              count_emails+=1


                         if email2 is None:
                              pass
                         else:
                           
                              if count_emails==0:
                                   res.email_address.append(EmailDetails(email_addresses[count_emails],1))
                              else:
                                   res.email_address.append(EmailDetails(email_addresses[count_emails],0))
     
                              count_emails+=1


                         if email3 is None:
                              pass
                         else:
                           
                              if count_emails==0:
                                   res.email_address.append(EmailDetails(email_addresses[count_emails],1))
                              else:
                                   res.email_address.append(EmailDetails(email_addresses[count_emails],0))
     
                              count_emails+=1
                       
                 
                         session.merge(res)
                       
                    
                    else:
                         count_emails=0
                         for email in res2:
                              email.email_address=email_addresses[count_emails]
                              if count_emails==0: 
                                   email.is_it_primary_email=1
  
			      count_emails+=1 
                         
                         if count_emails>2:
                              pass # It means there were three email addresses in the database and have been updated successfully

                         else: #less than three phone number existed in the database hence add the new ones too
                             # append the new records that were not part of the previous records
                             #initialize index to the last value of counter
                            
                             for index in range(counter):
                                   emailexists= session.query(EmailDetails).filter(EmailDetails.contact_id==contact_id).filter(EmailDetails.email_address==email_addresses[index]).first()
                                   if emailexists is None:
                                        #Then proceed with appending
                                        res.email_address.append(EmailDetails(email_addresses[index],0))
                                



	   			   
                             session.merge(res)               
                              
                    
                                                
                    session.commit() #Now commit this session                         
                    allow_insert=0 #Reset allow_insert to zero so that the code doesn't attempt to insert a new record
                    #size=size-1 #ignore the last value because it has arleady been updated
                    
                    result["opstatus"]={"success":1,"message":"The record for '%s %s %s' already existed hence has been updated"%(first_name,middle_name,last_name)}
                    session.close()  
                    engine.dispose()   
                    dbconn.close()
                    #we wind up our update operation and notify the use of the outcome.
                    return (json.JSONEncoder().encode(result))     
                                   
          except Exception as e:
               #if we get here the entire operation has failed so we have wind up all attempts to transact and close the database and then notify the user about the failure.
               session.close()
               engine.dispose()         
               dbconn.close()

               #print "Content-type: text/html\n" 
                                   
               result["opstatus"]={"success":-1,"message":"Error: %s"%e}
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
               
          
          if allow_insert==1: 
               #If we get here it means the record doesn't exist hence we need to create it for the first time.          
               try:
                    
                
                    new_address=AddressBook(first_name,middle_name,last_name,gender,dob,ward,district,region, country,company_id)
                    new_mobiles=[]
                    count_mobiles=0

                    if mobile1 is None:
                         pass
                    else:
                         new_mobiles.append(MobileDetails(mobile_numbers[count_mobiles],1))
                         count_mobiles+=1


                    if mobile2 is None:
                         pass
                    else:
                         new_mobiles.append(MobileDetails(mobile_numbers[count_mobiles],1))
                         count_mobiles+=1


                    if mobile3 is None:
                         pass
                    else:
                         new_mobiles.append(MobileDetails(mobile_numbers[count_mobiles],1))
                         count_mobiles+=1

                    


                    #new_mobiles=[MobileDetails(mobile_numbers[0],1),MobileDetails(mobile_numbers[0],0),MobileDetails(mobile_numbers[2],0)]#packed all three mobile numbers
                    
                    if count_mobiles>0: # We only extend if we have at least one mobile number
                         new_address.mobile_number=[]
                         new_address.mobile_number.extend(new_mobiles)

                    #Now extend emails

                    new_emails=[]
                    count_emails=0

		    if email1 is None:
                         pass
                    else:
                         new_emails.append(EmailDetails(email_addresses[count_emails],1))
                         count_emails+=1


                    if email2 is None:
                         pass
                    else:
                         new_emails.append(EmailDetails(email_addresses[count_emails],1))
                         count_emails+=1


                    if email3 is None:
                         pass
                    else:
                         new_emails.append(EmailDetails(email_addresses[count_emails],1))
                         count_emails+=1

                    if count_emails>0:
                         new_address.email_address=[]
                    	 new_address.email_address.extend(new_emails)
                                                
                                 
                    
                    
                    session.add(new_address)
                    
                    
                    # commit the record the database
                    
                    
                    session.commit()
                    session.close()
                    engine.dispose()
                    dbconn.close()
                     
                    result["opstatus"]={"success":1,"message":"The contact was added sucessfully"}
                    return (json.JSONEncoder().encode(result))                 
                     
                    
               except Exception as e:
                    session.close()
                    engine.dispose()
                    result["opstatus"]={"success":-1,"message":e.message}
                    dbconn.close()
                    return (json.JSONEncoder().encode(result)) 
            

               #result["R00"]={"F1":1,"F0":"The contact was recorded sucessfully"}
               #return (json.JSONEncoder().encode(result))
     
#myjson={"contact_id":3,"First Name":"Lucas","Middle Name":"Ntwa", "Last Name":"Katule","Gender":"Male","DOB":"12 Jan 2000","Ward":"Kunduchi","District":"Kinondoni","Region":"Dar es salaam","Country":"Tanzania","Mobile Phone #1":"0718255585","Mobile Phone #2":"0742340759","Mobile Phone #3":None,"Email Address #1":"katulentwa@gmail.com","Email Address #2":"katulentwa@hotmail.com","Email Address #3":"nkatule@aru.ac.tz"}     
#myjson={"GroupID":"11","Option":"-1"}
#myjson={}
#obj=AddressBookManager(myjson)
#msg=obj.retrieveContactDetailsFromDB()
#msg=obj.saveContactInDB()
#print msg
