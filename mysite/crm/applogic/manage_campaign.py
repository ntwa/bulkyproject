#!/usr/bin/env python
import datetime,time,calendar
import sys,json
#from sqlalchemy import create_engine,desc
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
#from save_sms_feedback import QueueFeedback
from collections import OrderedDict
#from bulkysms.database.sms_feedback_module import Campaign,CampaignStartDay,CampaignEndDay,CampaignDefinedMessages,SelectedDeliveryDayofWeek,db,dbconn
#from bulkysms.database.address_book_module import Campaign,CampaignDefinedMessages,db,dbconn
import xlrd
from xlrd.sheet import ctype_text
from django.core.files.storage import FileSystemStorage
import os
import re

from bulkysms.database.base import Base
from bulkysms.database.dbinit import db,dbconn

import bulkysms.database.address_book_module
import bulkysms.database.sms_feedback_module

Base.metadata.create_all(db)



from bulkysms.database.sms_feedback_module import Campaign,CampaignStartDay,CampaignEndDay,CampaignDefinedMessages,SelectedDeliveryDayofWeek,SelectedDeliveryTime,CampaignAudienceSMS, IndividualizedReminder 
from bulkysms.database.address_book_module import Group


def searchArray(item,array):


     for i in range(len(array)):
          if item==array[i]:
               return 1
  
     return -1

class ManageCampaign:
     def __init__(self,myjson):
          self.myjson=myjson
       
     def first_day_of_month(self,d):
          return datetime.date(d.year, d.month, 1)
      
     def last_day_of_month(self,d):
          t=(calendar.monthrange(d.year,d.month))
          return datetime.date(d.year,d.month,t[1])

     def retrieveCampaignDetailsFromDB(self):
           
          #The tuples are used for definition of JSON objects
          campaign_tuple={}
    

          #important in keeping track of number of groups
          level_one_json_counter=0
         
          key1="AD" #part of forming a key to json object for the group
          key2="MTXT"
           
	 
	  #get all campaigns and their respective details 
          try:
               
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               result={}                    
               # querying for a record if it exists already.
               res= session.query(Campaign).order_by(Campaign.is_campaign_active.desc()).order_by(Campaign.campaign_name).all()
               
               if len(res) ==0:
                    session.close()
                    engine.dispose()
                    dbconn.close()
                    result["AD00"]=-1
                    result["Message"]="No campaigns present."
                    return (json.JSONEncoder().encode(result))
	       else: 
                    for campaign_rec in res:	  
                         #Now  put both mobile tuple and email tuple to the main address tuple
                         if level_one_json_counter<10:
                              key1="AD0"# append a zero. This is important in ordering keys alphabetically
                         else:
                              key1="AD" 

                         campaign_id=campaign_rec.id 
                         date_raw=campaign_rec.date_created
                         date_str=date_raw.strftime("%d-%m-%Y")
                         delivery_medium=campaign_rec.delivery_mechanism

                         #Now get all messages that are part of each campaign
                         res_campaign_messages= session.query(CampaignDefinedMessages).filter(CampaignDefinedMessages.campaign_id==campaign_id).order_by(CampaignDefinedMessages.campaign_id).all()

                         message_tuple={}
                         level_two_json_counter=0
                         count_msgs=0
                         for one_msg_rec in res_campaign_messages:
                              if level_two_json_counter<10:
                                   key2="MTXT0"# append a zero. This is important in ordering keys alphabetically
                              else:
                                   key2="MTXT" 
                              message_tuple[key2+"%d"%level_two_json_counter]=one_msg_rec.message_txt
                              level_two_json_counter=level_two_json_counter+1 
                              count_msgs=count_msgs+1






                         # Now check is a campaign targets all contacts or just specific groups

                         audience_broadness=campaign_rec.target_level

                         group_tuple={}

                         if audience_broadness=="All":
                              group_rec={}
                              group_rec["GroupKey"]= "0"
                              group_rec["GroupName"]="All"
                              group_tuple["GRP00"]=group_rec
                         elif audience_broadness=="Specific Groups":
                              #Now get all groups that are part of this campaign. But before that check iof the campaign is for all 
                              res_campaign_groups= session.query(Group,CampaignAudienceSMS).filter(CampaignAudienceSMS.campaign_id==campaign_id).filter(CampaignAudienceSMS.group_id==Group.id).order_by(Group.group_name).all()

                              
                              level_two_json_counter=0
                              count_grps=0
                              for one_grp_rec in res_campaign_groups:
                                   group_details,audience_details=one_grp_rec
                                   if level_two_json_counter<10:
                                        key2="GRP0"# append a zero. This is important in ordering keys alphabetically
                                   else:
                                        key2="GRP" 
                                   group_rec={}
                                   group_rec["GroupKey"]= "%s"%group_details.id
                                   group_rec["GroupName"]="%s"%group_details.group_name    
                                   group_tuple[key2+"%d"%level_two_json_counter]=group_rec
                                   level_two_json_counter=level_two_json_counter+1 
                                   count_grps=count_grps+1

                         campaign_category=campaign_rec.campaign_category          

                         #print campaign_rec.campaign_name, group_tuple

                         #Now get start date and enddate for a campaign
                         res_campaign_start_date=session.query(CampaignStartDay).filter(CampaignStartDay.campaign_id==campaign_id).first()
                         if res_campaign_start_date is None:
                              campaign_start_date=""
                         else:
                              campaign_start_date_raw=res_campaign_start_date.campaign_start_date
                              campaign_start_date=campaign_start_date_raw.strftime("%d-%m-%Y")

                         res_campaign_end_date=session.query(CampaignEndDay).filter(CampaignEndDay.campaign_id==campaign_id).first()
                         if res_campaign_end_date is None:
                              campaign_end_date=""
                         else:
                              campaign_end_date_raw=res_campaign_end_date.campaign_end_date
                              campaign_end_date=campaign_end_date_raw.strftime("%d-%m-%Y")



                              


                         
                         campaign_tuple[key1+"%d"%level_one_json_counter]={"CampaignID":campaign_id, "campaign_name":campaign_rec.campaign_name, "campaign_description":campaign_rec.campaign_descr,"DateCreated":date_str, "DeliveryMedium":delivery_medium, "TargetedAudience":group_tuple,"CampaignCategory":campaign_category,"TotalMessages":count_msgs,"messagestxt": message_tuple,"CampaignStartDate":campaign_start_date,"CampaignEndDate":campaign_end_date,"CampaignActive":campaign_rec.is_campaign_active}
                         level_one_json_counter=level_one_json_counter+1 # After getting the first record add 1 to the counter	
                         

         
                         
                    session.close()  
                    engine.dispose()   
                    dbconn.close()
                     
                    return(json.JSONEncoder().encode(OrderedDict(sorted(campaign_tuple.items(), key=lambda t: t[0]))))   
                                   
          except Exception as e:
               #if we get here the entire operation has failed so we have wind up all attempts to transact and close the database and then notify the user about the failure.
               session.close()
               engine.dispose()         
               dbconn.close()

               #print "Content-type: text/html\n" 
                                   

               result["AD00"]=-6
               result["message"]="Error: %s."%e
               print e      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
     



     
     def searchArray(self,item,array):


          for i in range(len(array)):
               if item==array[i]["name"]:
                    return i
  
          return -1



     

     #This has a starting posn     
     def searchArray2(self,item,array,start_posn):
          for i in range(len(array)):
               if i<start_posn:
                    continue #skip until we get to the position where we neeed to start
               if item==array[i]["name"]:
                    return i
  
          return -1


     def saveOneCampaignInDB(self,request):
         
          allow_insert=1
          result={}
          field_array=[]



          # Get data from fields
          
          try:
               #myjson=json.JSONEncoder().encode(self.myjson)
          
               arr_items=self.myjson
               

               #Get campaign name
               ret=self.searchArray("campaignname",arr_items)
               
               if ret>=0:
                    json_obj=arr_items[ret]
                    campaign_name=json_obj["value"]
               else:
                    raise ValueError("The submitted form didn't have 'Campaign Name' field")

               #Get campaign description
               ret=self.searchArray("campaign_descr",arr_items)
               
               if ret>=0:
                    json_obj=arr_items[ret]
                    campaign_descr=json_obj["value"]
               else:
                    raise ValueError("The submitted form didn't have 'Campaign Description' field")


               #Get deliverymedium
               ret=self.searchArray("deliverymedium",arr_items)
               
               if ret>=0:
                    json_obj=arr_items[ret]
                    delivery_medium=json_obj["value"]
               else:
                    raise ValueError("The submitted form didn't have 'Campaign Delivery Medium' field")


               #Get campaign category
               ret=self.searchArray("campaigncategory",arr_items)
               
               if ret>=0:
                    json_obj=arr_items[ret]
                    campaign_category=json_obj["value"]
                    #Now check if campaign caterogy is under individual reminder. If that is the case the prepare individual reminder objects from an excel file
                    if campaign_category=="IR":

                         myjson={"status": "file uploaded"}
                         individual_reminders=[] # create an empty array that will be used to store reminders from an excell file.
                         
                         msg={"message":""}
                         try:

                              if request.method == 'POST' and request.FILES['reminderfile']:
                                   reminderfile = request.FILES['reminderfile']
                                   fs = FileSystemStorage()
                                   filename = fs.save("remminders.xls", reminderfile)
                                   uploaded_file_url = fs.url(filename)
                                   path="%s/media/%s"%(os.getcwd(),filename)
                                   myjson["status"]="%s. Path=%s"%(myjson["status"],path)
                                   #fname=fname = join(dirname(dirname(abspath(__file__))), 'media/',filename)

                                   xl_workbook = xlrd.open_workbook(path)
                                   sheet_names = xl_workbook.sheet_names() 

                                   xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
                                   num_rows=xl_sheet.nrows
                                   num_columns=xl_sheet.ncols
                                   col_counter=0 # count the number of columns we have visited
                                   #max_columns=num_columns
                                   #sentinal=1
                                   strrow=""
                                   records=[]
                                   col_headers=['contact_id','First Name','Last Name','Reminder Expiry Date','Days of Running','Deadline for Action','Reason For Reminder']
                                   col_headers_order=[]
                                   header_counter_on=0
                                   col_header_counter=0

                                   str_reg_expr="^(?![\s\S])" #A regualar expression for matching empty strings
                                   #str_reg_expr2="^(?[\s\S])" #A regualar expression for matching strings with only white spaces
                                   
                                   #
                                   for row_posn in range(num_rows):

                                        row=[]
                                        col_counter=0
                                        row_content=""
                                        
                                        #print row_posn
                                        #print ""
                                        #print ""


                                        for col_posn in range(num_columns):
                                             cell= xl_sheet.cell(row_posn,col_posn)
                                             strcontent="%s"%cell.value
                                        
                                             row_content="%s%s"%(row_content,strcontent)

                                             #row_content="%s%s"%(row_content,strcontent)
                                             
                                             test_result=re.match(strcontent, str_reg_expr, re.IGNORECASE) # Now check if one cell is empty
                                             test_result2=re.match(row_content, str_reg_expr, re.IGNORECASE) # Now check if the entire row is empty
                                             
                                             if test_result and test_result2:
                                                  #print test_result2.groups(0) 
                                                  pass
                                                  #if col_posn==0:
                                                  #print "Empty encountered at cell (%s,%s) and str=%s"%(row_posn,col_posn,strcontent)
                                             else:

                                                  if searchArray(cell.value,col_headers)>0: #First check if the column is header, if it is header don't append
                                                       
                                                       if col_posn==0:
                                                            #print "Change head counter"
                                                            header_counter_on=1 #This means we have started conting headers
                                                       col_headers_order.append("%s"%cell.value) 
                                                       col_header_counter=col_header_counter+1
                                                  elif header_counter_on==0 and test_result2==None: #These are for headers that are not column heading
                                                       pass
                                         
                                                       #print "Row empty but some cells encountered at cell (%s,%s) and str=%s"%(row_posn,col_posn,strcontent)
                                                  else:  
                                                       #print "There is some content at row cell (%s,%s) and str=%s"%(row_posn,col_posn,strcontent)
                                                      #First we have to confirm that we found all necessary headers
                                                       if col_header_counter==num_columns:  
                                                           pass
                                                       else:
                                                            #print "%s=%s"%(col_header_counter,num_columns)
                                                            #just return error to the user as the naming of column headers don't conform to the ones expected.
                                                            myjson["status"]="Error. Process terminated. Not the naming of all column headers conform to the allowed ones ."
                                                            os.remove(path) #remove the file once done with it
                                                            status=json.JSONEncoder().encode(myjson)
                                                            return HttpResponse('%s(%s)' % (request.GET.get('callback'),status), content_type='application/json')



                                                       cellvalue= cell.value  

                                                        #check if a cell is empty.

                                                       if test_result:
                                                           #It means the cell was left blank therefore assine "None" to cellvalue
                                                           cellvalue=None

                                                       row.append(cellvalue)
                                                       col_counter=col_counter+1
                                                  
                                                 
                                                  #row.append(cell.value)
                                                  #col_counter=col_counter+1

                                        #check if the entire row is empty 
                                        if col_counter==num_columns: #It means there were no empty columns in this row or the columns don't represent headers.
                                             records.append(row)

                         
                                   error_detected=-1  
                                   error_value="None"   
                                   row_counter=0 
                                   #insert one record at a time
                                   fail_to_be_updated_records=[]
                               
                                   #for rec in records:
                                   #Iterate through the entire excel file
                                   for row_record in range(len(records)):
                                        #Now prep a json object
                                        columncounter=0 
                                        jsondata={}
                                        current_record="None" #This variable is important in cases of errors as it helps in knowing which record was being updated when the error occured
                                   
                   
                                        
                                        #for dataval in rec:
                                        for dataval in records[row_record]:
                                             key="%s"%col_headers_order[columncounter]
                                        
                                             if col_headers_order[columncounter]=="Reminder Expiry Date" or col_headers_order[columncounter]=="Deadline for Action":
                                                 try:
                                                       base = datetime.datetime(1899,12,30)
                                                       datetime_object = datetime.datetime.strptime(dataval, '%d %b %Y')
                                                       date_obj_str=datetime_object.strftime("%Y-%m-%d")
                                                       #datetime_object=datetime.datetime.strptime(date_obj_str, "%d/%m/%Y")
                                                       #myjson["status"]=date_obj_str
                                                       #initial_time=datetime.datetime.strptime(end_time_cluster, "%H:%M")-datetime.timedelta(hours=6)+
                                                       #jsondata[key]=(base + datetime.timedelta(int(date_obj_str))).strftime('%Y-%m-%d')
                                                       #jsondata[key]=(base + datetime.timedelta(datetime_object)).strftime('%Y-%m-%d')
                                                       jsondata[key]=date_obj_str
                                                       
                                                      
                                                 except Exception as e:
                                                       error_detected=1
                                                       error_value=e
                                                       fail_to_be_updated_records.append(row_record)
                                                       break # We just skip this record/row and move to the next
                                            
                       
                                             elif col_headers_order[columncounter]=="contact_id":
                                                 jsondata[key]=int(dataval)
                         
                                             else:
                                                 jsondata[key]=dataval
                                             columncounter=columncounter+1
                                             
                               
                                        if error_detected>0:
                                             pass
                                             if error_detected==1:
                                                 error_message="The system has encountered error(s)!: '%s'. Make sure your excel file follows the downloaded template format. "%error_value
                                                 #skip this record only and go to the next one
                                                 #raise ValueError(error_message)
                                             else:
                                                 raise ValueError("The system has encountered errors!.")
                                        else:
                                             #Now insert this reminder for a campaign. Remove the old code.
                                             contact_id=jsondata["contact_id"]
                                             reminder_end_date=jsondata["Reminder Expiry Date"]
                                             event_deadline_date=jsondata["Deadline for Action"]
                                             no_running_days=jsondata["Days of Running"]
                                             reason_for_reminder=jsondata["Reason For Reminder"]

                                             new_reminder=IndividualizedReminder(contact_id,reminder_end_date,event_deadline_date,no_running_days,reason_for_reminder)
                                             individual_reminders.append(new_reminder)
                                        
                                   


                                   #new_campaign.individual_campaign=[]
                                   #new_campaign.individual_campaign.extend(individual_reminders)
                    



                                   os.remove(path) #remove the file once done with it
                              result["message"]=campaign_category

                         except Exception as e:
                              result["message"]="%s"%e                         








                    #Now look for the value of file
               else:
                    raise ValueError("The submitted form didn't have 'Campaign Category' field")

               sms_campaign_target_groups=[]
               numOfGroups=0

               #Get campaign target sms
               if delivery_medium=="SMS":
                    #First find out how many groups were selected
                    ret=self.searchArray("numOfGroups",arr_items)
                    if ret>=0:
                         json_obj=arr_items[ret]
                         numOfGroups=int(json_obj["value"])
                    else:
                         raise ValueError("The submitted form didn't have defined field for number of groups selected")

                         
                    if numOfGroups==0:
                         raise ValueError("The submitted form didn't have the targeted campaign audience selected")


                    current_posn=0
                    for posn in range(numOfGroups):
                         ret=self.searchArray2("campaigntargetsms",arr_items,current_posn)
                         if ret>=0:
                              json_obj=arr_items[ret]
                              sms_campaign_target_groups.append(int(json_obj["value"]))
                              current_posn=ret+1 #Go one extra posn from where the current element was found
                         else:
                              break

               
                    #else:
                    #     raise ValueError("The submitted form didn't have the targeted campaign audience field")
               #Get campaign target whatsapp
               elif delivery_medium=="Whatsapp":
                    raise ValueError("Sorry!! The Whatsapp campaigns are not yet supported at the moment but will be integrated later.")
                    ret=self.searchArray("campaigntargetwhatsapp",arr_items)
               
                    if ret>=0:
                         json_obj=arr_items[ret]
                         campaign_target_sms=json_obj["value"]
                    else:
                         raise ValueError("The submitted form didn't have the targeted campaign audience field")
                              #Get campaign target sms
               elif delivery_medium=="Email":
                    raise ValueError("Sorry!! The Email campaigns are not yet supported at the moment but will be integrated later")


               #Get campaign start date
               ret=self.searchArray("campaignstartdateextra",arr_items)
               
               if ret>=0:
                    json_obj=arr_items[ret]
                    campaign_start_date=json_obj["value"]
                    #campaign_start_date=json_obj["value"]
               else:
                    raise ValueError("The submitted form didn't have 'Campaign Start Date' field")


               #Get campaign life of  campaingn status
               ret=self.searchArray("lifeofcampaign",arr_items)
               
               if ret>=0:
                    json_obj=arr_items[ret]
                    life_of_campaign=int(json_obj["value"])
               else:
                    raise ValueError("The submitted form didn't have 'Life of Campaign' field")

               
 
               if life_of_campaign==1:
                    campaign_end_date=""
               elif life_of_campaign==0:
                    #Get campaign life of  campaign end date
                    ret=self.searchArray("campaignenddateextra",arr_items)
                    
                    if ret>=0:
                         json_obj=arr_items[ret]
                         campaign_end_date=json_obj["value"]
                    else:
                         raise ValueError("The submitted form didn't have 'Campaign End Date' field")


               #Get Days Interval
               ret=self.searchArray("daysintervals",arr_items)
               
               if ret>=0:
                    json_obj=arr_items[ret]
                    days_intervals=int(json_obj["value"])
               else:
                    raise ValueError("The submitted form didn't have 'Days of Weeks of where campaign will run' field")
               
               specific_campaign_days=[]
               
               if days_intervals==4: #it means the user has picked specific days
                    for i in range(7): #iterate through seven days of the week to find out which ones were picked
            
                         jsonkey="campaigndayofweek_%s"%i
                         ret=self.searchArray(jsonkey,arr_items)
                         if ret>=0:
                              json_obj=arr_items[ret]
                              picked_day=int(json_obj["value"])
                              specific_campaign_days.append(picked_day)
                    if len(specific_campaign_days)==0:
                         raise ValueError("The submitted form didn't have any 'Selected Campaign Days' field")
               elif days_intervals==1:
                    for i in range(7): #iterate through seven days of the week to find out which ones were picked
                         picked_day=i
                         specific_campaign_days.append(picked_day)
               elif days_intervals==2:
                    for i in range(6): #iterate through seven days of the week to find out which ones were picked
                         if i==0:
                              continue #Skip Sunday as it is not part of the weekend
                         picked_day=i
                         specific_campaign_days.append(picked_day)
               elif days_intervals==3:
                    specific_campaign_days.append(6)
                    specific_campaign_days.append(0)
               else:
                    raise ValueError("The submitted 'Selected Campaign Days' value is not recognized")
               





               #Get Number of times a campaign run in a day
               ret=self.searchArray("frequencyofrunningselected",arr_items)
               
               if ret>=0:
                    json_obj=arr_items[ret]
                    frequency_of_running_selected=json_obj["value"]
               else:
                    raise ValueError("The submitted form didn't have 'Number of time the campaign will run during a day' field")


               #Get Number of times a campaign run in a day
               ret=self.searchArray("frequencyofrunningselected",arr_items)
               
               if ret>=0:
                    json_obj=arr_items[ret]
                    frequency_of_running_selected=int(json_obj["value"])
               else:
                    raise ValueError("The submitted form didn't have 'Number of time the campaign will run during a day' field")


               if frequency_of_running_selected==6:
                    #Get the defined number of times a campaign need to run during the day
                    ret=self.searchArray("userdefinedfrequency_box",arr_items)
                    
                    if ret>=0:
                         json_obj=arr_items[ret]
                         frequency_of_running_selected=int(json_obj["value"]) # pick this value
                    else:
                         raise ValueError("The submitted form didn't have 'Number of time the campaign will run during a day' field")





               
               target_level=""
               
               if numOfGroups>1:
                    target_level="Specific Groups"
               elif numOfGroups==1:
                    if sms_campaign_target_groups[0]==0:
                         target_level="All"
                    else:
                         target_level="Specific Groups"

               
               frequency_in_days=int(days_intervals)

               #Time for campaigm
               hours=[]
               minutes=[]
               counter=0
               scheduled_times=[]
               for i in range(frequency_of_running_selected):
                    #time="%s%s:00"%()
                    key_hour="hour%s"%counter
                    key_minutes="minutes%s"%counter
                    #hours.append(key_hour)
                    #minutes.append(key_minutes)
                    #counter=counter+1

                    #Now lets retrieve times:
                    ret=self.searchArray(key_hour,arr_items)
               
                    if ret>=0:
                         json_obj=arr_items[ret]
                         hour=json_obj["value"]
                    else:
                         raise ValueError("Hour not set")

                    ret=self.searchArray(key_minutes,arr_items)
                    if ret>=0:
                         json_obj=arr_items[ret]
                         minutes=json_obj["value"]
                    else:
                         raise ValueError("Minutes not set")
                    
                    scheduled_time="%s:%s:00"%(hour,minutes)
                    scheduled_times.append(scheduled_time)
                    counter+=1
               



               #Get Number of appended messages
               ret=self.searchArray("numOfAppendedMessages",arr_items)
               
               if ret>=0:
                    json_obj=arr_items[ret]
                    num_messages=int(json_obj["value"])  #Number of messages defined for this campaign
               else:
                    raise ValueError("The submitted form didn't have 'Number of campaign messages' field")

               
               msglst=[] #An array to hold text messages extracted from a JSON object
               for i in range(num_messages):
                    jsonkey="campaignmsgbx_%s"%i
                    ret=self.searchArray(jsonkey,arr_items)
                    if ret>=0:
                         json_obj=arr_items[ret]
                         msgvalue = json_obj["value"]
                         msglst.append(msgvalue)
                    else:
                         errorvalue="The submitted form didn't have '%s' field"%jsonkey
                         raise ValueError(errorvalue)
               

               


              
               #userdefinedfrequency_box



                    
               #result["Text"]="Submitted Json"
               #return (json.JSONEncoder().encode(result)) 
  

               '''
               campaign_name=self.myjson["CampaignName"]

               campaign_descr=self.myjson["CampaignDescr"]
              
               campaign_category=self.myjson["CampaignCategory"]
               target_level=self.myjson["TargetLevel"]
               frequency_in_days=self.myjson["Frequency_in_Days"]
               is_it_life_time=int(self.myjson["is_it_life_time"])
               is_annual_delivery_date_constant=int(self.myjson["is_annual_delivery_date_constant"])
               msglstjson=self.myjson["Messages"]

               num_messages=int(self.myjson["NumMessages"]) #Number of messages defined for this campaign
               msglst=[] #An array to hold text messages extracted from a JSON object
               if num_messages>0:
               		for msgkey in msglstjson:
               			 msgvalue = msglstjson[msgkey]
               			 msglst.append(msgvalue)
               			 #print "The key and value are (%s) = (%s)"%(msgkey, msgvalue)
               else:
               	    print "Fail %s"%num_messages
               '''          

               
               #return (json.JSONEncoder().encode(result)) 
               '''
               campaign_name="Birthday Greetings"
               campaign_descr="This campaign has been dedicated for birthday greetings to customers"
               campaign_category="Individual Best Wishes"
               target_level="Individual"
               frequency_in_days="Selective Days"
               is_it_life_time=1 
               is_annual_delivery_date_constant=1
               msg1="We wish you happy birthday. Thank you for being our loyal customer"
               msg2="Happy birthday. We value you as esteemed customer"
               msg3="As you celebrate your birthday, we wish you more success in business. Thank for being with us all this time."
               msglst=[msg1,msg2,msg3]
               '''                
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]="Error: '%s'. If the error persists contact the support team"%e
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          

          if(campaign_name=="") or (campaign_descr=="") or (campaign_category=="") or (target_level=="") or (frequency_in_days==""):
               #print "Content-type: text/html\n" 
               result["message"]="Error: You did not enter all important details"
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
               res= session.query(Campaign).filter(Campaign.campaign_name==campaign_name).first()
               
               if res is None:
                    session.close()
                    engine.dispose()
                    dbconn.close()
               else:
                    #if it exists, then update the record in the database.
                    campaign_part1_record=res
                    campaign_part1_record.campaign_name=campaign_name
                    campaign_part1_record.campaign_descr=campaign_descr
                    campaign_part1_record.delivery_mechanism=delivery_medium
                    campaign_part1_record.campaign_category=campaign_category
                    campaign_part1_record.target_level=target_level
                    
                    
                  
                    
                    campaign_id=res.id

                    #Now delete all messages associated with this campaign and then update with new ones
                    
                    resmsg=session.query(CampaignDefinedMessages).filter(CampaignDefinedMessages.campaign_id==campaign_id).all()
                    
                    if len(resmsg)==0:
                    	pass
                    else:
                    	for record in resmsg:
                    	 	session.delete(record)






                    
                    #print "Got here"

                    #now insert new messages
                    counter=0
                    for msgtxt in msglst:
                    	res.campaign_messages.append(CampaignDefinedMessages(msgtxt))
                    	 #session.merge(res)


                    #Now unlink defined audience (groups)  from  this campaign and then update with the new audience
                    
                    resaud=session.query(CampaignAudienceSMS).filter(CampaignAudienceSMS.campaign_id==campaign_id).all()
                    
                    if len(resaud)==0:
                         print "No records on campaign=%s"%campaign_id
                    else:
                         for record in resaud:
                              session.delete(record)


                    #Now create a new audience for this campaign
                                  #print "Got here"

                    counter=0
                    
                    for grp_id in sms_campaign_target_groups:

                         if grp_id==0:
                              
                              break #This campaign is targeting everyone registered in the contact list.

                         res.sms_campaign_audience.append(CampaignAudienceSMS(grp_id))


                    

                    #Now delete all delivery days associated with this campaign and then update with new ones
                    
                    rescmpdays=session.query(SelectedDeliveryDayofWeek).filter(SelectedDeliveryDayofWeek.campaign_id==campaign_id).all()
               
                    if len(rescmpdays)==0:
                         pass
                    else:
                         
                         for record in rescmpdays:
                              session.delete(record)

                    
                    #Now insert delivery days within a week
                    for day in specific_campaign_days:
                         res.selected_delivery_days.append(SelectedDeliveryDayofWeek(day))




                    #start date, end date
                    if campaign_start_date=="":
                         if campaign_category=="IR" or campaign_category=="BW":
                              pass
                         else:
                              raise ValueError("Error: Start Date missing. The only Campaigns with optional start date are Birthday Wishes and Individualized Reminders'. The rest must have start date ")
                    else:

                         #Now delete a start date associated with this campaign and then update with a new one
                         
                         resstartdate=session.query(CampaignStartDay).filter(CampaignStartDay.campaign_id==campaign_id).all()
                    
                         if len(resstartdate)==0:
                              pass
                         else:
                              
                              for record in resstartdate:
                                   session.delete(record)

                         #Now insert a start date
                         campaign_start_date=datetime.datetime.strptime(campaign_start_date, '%m/%d/%Y').date()
                         res.starting_day.append(CampaignStartDay(campaign_start_date))


                    if campaign_end_date=="":
                         if campaign_category=="IR" or campaign_category=="BW" or life_of_campaign==1:
                              pass
                         else:
                              raise ValueError("Error: End Date missing. The only Campaigns with optional end date are Birthday Wishes, Individualized Reminders or any other campaign that has been selected to run indefinately'. The rest must have start date ")
                    else:



                         #Now delete an end date associated with this campaign and then update with a new one
                         
                         resenddate=session.query(CampaignEndDay).filter(CampaignEndDay.campaign_id==campaign_id).all()
                    
                         if len(resenddate)==0:
                              pass
                         else:
                              
                              for record in resenddate:
                                   session.delete(record)

                         #Now insert end date
                         campaign_end_date=datetime.datetime.strptime(campaign_end_date, '%m/%d/%Y').date()
                         res.stopping_day.append(CampaignEndDay(campaign_end_date))

                    

                    #Now delete all the scheduled time for running this campaign before setting the new one

                    #scheduled_times

                    res_scheduled_times=session.query(SelectedDeliveryTime).filter(SelectedDeliveryTime.campaign_id==campaign_id).all()
                    
                    if len(res_scheduled_times)==0:
                         pass
                    else:
                              
                         for record in res_scheduled_times:
                              session.delete(record)


                    for schedule_time in scheduled_times:
                         res.selected_delivery_time.append(SelectedDeliveryTime(schedule_time))

                    

                    #Now append updated messages.
                    #search all messages to to be updated
                    #for msgtuple in msglst:
                    #     msg_id=msgtuple[0]
                    #     msg_txt=msgtuple[1]
                         #search by ID
                    
                    #	 resmsg= session.query(CampaignDefinedMessages).filter(CampaignDefinedMessages.id==msg_id).first()
                         
                     #    if resmsg is None:
                     #    #append this new message to the above campaign
                     
                     #         res.campaign_messages.append(CampaignDefinedMessages(msg_txt))
                     #         session.merge(res)
                      #   else:
                         #update this msg txt to assume a new value
                      #        resmsg.message_txt=msg_txt


                    #Now check individualized reminders from an existing campaign and edit them too  

                    res_individual_reminders=session.query(IndividualizedReminder).filter(IndividualizedReminder.campaign_id==campaign_id).all()
                    if len(res_individual_reminders)==0:
                         pass
                    else:
                         for record in res_individual_reminders:
                              session.delete(record)

                    #update reminders that are attached to a campaign.          

                    res.individual_campaign=[]
                    res.individual_campaign.extend(individual_reminders)








                    #end of code for individualized reminders
                                        
                       
                                                
                    session.commit() #Now commit this session                         
                    allow_insert=0 #Reset allow to zero so that the code doesn't attempt to insert a new record
                    #size=size-1 #ignore the last value because it has arleady been updated
                    
                    result["message"]="The record for '%s' campaign already existed hence has been updated"%campaign_name
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
               integrity_error="_mysql_exceptions.IntegrityError"
               schedule_table="selected_time_of_delivery"
               message_table="selected_time_of_delivery"
               error="%s"%e
               if integrity_error in error and schedule_table in error:
                    result["message"] ="Error :Failed to update. You have entered same value for 'time' in more than one time box."
               else:
                    result["message"]="Error: Failed to update"

               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
               
          
          if allow_insert==1: 
               #If we get here it means the record doesn't exist hence we need to create it for the first time.          
               try:
                    
                
                    new_campaign=Campaign(campaign_name,campaign_descr,delivery_medium,campaign_category,target_level)
                    new_campaign_messages=[]
                    delivery_days=[]
                    new_campaign_audience=[]


                    #Now append messages for this campaign
                   
                    for msg_tuple in msglst:
                         new_campaign_messages.append(CampaignDefinedMessages(msg_tuple))



                    #Now append audeince for this campaign
                    audience_all=False
                    for grp_id in sms_campaign_target_groups:
                         if grp_id==0:
                              audience_all=True
                              break
                         new_campaign_audience.append(CampaignAudienceSMS(grp_id))

                    #Append weekly delivery days for this campaign

                    for day in specific_campaign_days:
                         delivery_days.append(SelectedDeliveryDayofWeek(day))
                    

                   
                    new_campaign.campaign_messages=[]
                    new_campaign.campaign_messages.extend(new_campaign_messages) 
                     
                    #Append only if audience is for specific groups 
                    if audience_all:
                         pass
                    else:
                         new_campaign.sms_campaign_audience=[]
                         new_campaign.sms_campaign_audience.extend(new_campaign_audience)


                    if campaign_start_date=="":
                         if campaign_category=="IR" or campaign_category=="BW":
                              pass
                         else:
                              raise ValueError("Error: Start Date missing. The only Campaigns with optional start date are Birthday Wishes and Individualized Reminders'. The rest must have start date ")
                    else: 

                         campaign_start_date=datetime.datetime.strptime(campaign_start_date, '%m/%d/%Y').date()

                         new_campaign_start_day=CampaignStartDay(campaign_start_date)
                         new_campaign.starting_day=[new_campaign_start_day]


                    if campaign_end_date=="":
                         if campaign_category=="IR" or campaign_category=="BW" or life_of_campaign==1:
                              pass
                         else:
                              raise ValueError("Error: End Date missing. The only Campaigns with optional end date are Birthday Wishes, Individualized Reminders or any other campaign that has been selected to run indefinately'. The rest must have start date ")
                    else:  
                         campaign_end_date=datetime.datetime.strptime(campaign_end_date, '%m/%d/%Y').date()   

                         new_campaign_end_day=CampaignEndDay(campaign_end_date)

                         new_campaign.stopping_day=[new_campaign_end_day]


                    new_campaign.selected_delivery_days= []
                    new_campaign.selected_delivery_days.extend(delivery_days)
                    if campaign_category=="IR":
                         #process records from reminder file
                                                 
                         new_campaign.individual_campaign=[]
                         new_campaign.individual_campaign.extend(individual_reminders) # use individual reminders that have been extracted from excel file
                    

                         #End of code for processing reminder file.

                    #Now check if it is an individualized reminder so that accompanying records from an excel file can be appended



                    session.add(new_campaign)
                    
                    
                    # commit the record the database
                    
                    
                    session.commit()
                    session.close()
                    engine.dispose()
                    dbconn.close()
                     
                    #result["message"]="The campaign was added sucessfully"
                    return (json.JSONEncoder().encode(result))                 
                     
                    
               except Exception as e:
                    session.close()
                    engine.dispose()
                    result["message"]="Error: %s. If the error persists contact the support team"%e.message
                    dbconn.close()
                    return (json.JSONEncoder().encode(result)) 

    
     
#myjson={"campaign_name":"Birthday Greetings","campaign_descr":"This campaign has been dedicated for birthday greetings to customers","campaign_category":"Individual Best Wishes","target_level":"Individual","frequency_in_days":"Selective Days","is_it_life_time":"1","is_annual_delivery_date_constant":"1","messages":[[3,"We wish you happy birthday. Thank you for being our loyal customer"],[2,"Happy birthday. We value you as our esteemed customer"],[1,"As you celebrate your birthday, we wish you more success in business. Thank for being with us all this time."]]}
#myjson={"CampaignName":"Birthday Greetings","CampaignDescr":"This campaign has been dedicated for birthday greetings to customers","CampaignCategory":"Individual Best Wishes","TargetLevel":"Individual","Frequency_in_Days":"Selective Days","is_it_life_time":"1","is_annual_delivery_date_constant":"1","NumMessages":3,"Messages":{"Message0":"Hello there. We wish you happy birthday. Thank you for being our loyal customer","Message1":"Happy birthday. We value you as our esteemed customer","Message2":"As you celebrate your birthday, we wish you more success in business. Thank for being with us all this time."}}
#myjson={}
#obj=ManageCampaign(myjson)
#msg=obj.retrieveCampaignDetailsFromDB()
#msg=obj.saveOneCampaignInDB()

#print msg
