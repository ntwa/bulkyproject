#!/usr/bin/env python
import datetime,time,calendar
import sys,json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from save_sms_feedback import QueueFeedback
from collections import OrderedDict


class SaveSMS:
     def __init__(self,myjson):
          self.myjson=myjson
       
     def first_day_of_month(self,d):
          return datetime.date(d.year, d.month, 1)
      
     def last_day_of_month(self,d):
          t=(calendar.monthrange(d.year,d.month))
          return datetime.date(d.year,d.month,t[1])




     def saveOneCampaignInDB(self):
         
          allow_insert=1
          
          # Get data from fields
          try:
               '''             
               firstname=self.myjson["FName"] 
               middlename=self.myjson["MName"] 
               lastname=self.myjson["LName"] 
               dob=self.myjson["DOB"] 
               gender=self.myjson["Gender"] 
               ward=self.myjson["Ward"]
               district=self.myjson["District"]
	       region=self.myjson["Region"]
	       country=self.myjson["Country"]  
               mobile1=self.myjson["Mobile1"] 
               mobile2=self.myjson["Mobile2"] 
               mobile3=self.myjson["Mobile3"]  
	       email1=self.myjson["Email1"]
	       email2=self.myjson["Email2"]
	       email3=self.myjson["Email3"]       
               
               '''
               
               campaign_name="Birthday Greetings"
               campaign_descr="This campaign is specifically for birthday greetings to customers"
               campaign_category="Individual Best Wishes"
               target_level="Individual"
               frequency_in_days="SelectiveDays"
               is_it_life_time=1 
               is_annual_delivery_date_constant=1
               msg1="We wish you happy birthday. Thank you for being our loyal customer"
               msg2="Happy birthday. We value you as esteemed customer"
               msg2="As you celebrate your birthday, we wish you more success in business. Thank for being with us all this time.
               msglst=[msg1,msg2,msg3]
                               
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]="Error: '%s' encountered in editing the 'The Campaign'. If the error persists contact the developer"%e
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          

          if(campaign_name=="") and (campaign_descr=="") and (campaign_category=="") and (target_level=="") and (frequency_in_days=="") and (is_it_life_time=="") and (is_annual_delivery_date_constant==""):
               #print "Content-type: text/html\n" 
               result["message"]="Error: You did not enter any details"
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
		    campaign_part1_record.campaign_category=campaign_category
                    campaign_part1_record.target_level=target_level
                    campaign_part1_record.frequency_in_days=frequency_in_days
                    campaign_part1_record.is_it_life_time=is_it_life_time
		    campaign_part1_record.is_annual_delivery_date_constant=is_annual_delivery_date_constant

                    campaign_id=res.id
                    
                    '''
                    #search all messages to to be updated
                    res2= session.query(CampaignDefinedMessages).filter(CampaignDefinedMessages.campaign_id==campaign_id).order_by(CampaignDefinedMessages.contact_id).order_by(CampaignDefinedMessages.id).all()
                   
                    
                    
                    #initialize counter to zero before start changing each message txt
                    counter=0
                   
                    if len(res2) ==0:
                       #Incase the Campaign existed but messages for campaign didn't exist then attempt to create them
                       #
                       res.message_txt.append(CampaignDefinedMessages(msglst[0]))
                       res.message_txt.append(CampaignDefinedMessages(msglst[1]))
                       res.message_txt.append(CampaignDefinedMessages(msglst[2]))
                       session.merge(res)
                     
			 
                    else:
                         for message in res2:
                              message.message_txt=msglst[counter]
                                  
			      counter=counter+1
                         if counter==len(msglst):
                              pass # It means the number msgtxt boxes matched the number message in the database and have been updated successfully

                         else: #less than three phone number existed in the database hence add the new ones too
                             # append the new records that were not part of the previous records
                             #initialize index to the last value of counter
                            
                             for index in range(counter,len(msglst)):
	   			   res.message_txt.append(CampaignDefinedMessages(msglst[index]))
                             session.merge(res) 
                                   
           
                    '''          
                    
                                                
                    session.commit() #Now commit this session                         
                    allow_insert=0 #Reset allow to zero so that the code doesn't attempt to insert a new record
                    #size=size-1 #ignore the last value because it has arleady been updated
                    
                    result["message"]="The record for '%s %s %s' already existed hence has been updated"%(first_name,middle_name,last_name)
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
                                   
               result["message"]="Error: %s. (Line 245)"%e
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
               
          
          if allow_insert==1: 
               #If we get here it means the record doesn't exist hence we need to create it for the first time.          
               try:
                    
                
                    new_campaign=Campaign(campaign_name,campaign_descr,campaign_category,target_level,frequency_in_days,is_it_life_time,is_annual_delivery_date_constant)
                    #new_messages=[MobileDetails(mobile_numbers[0],1),MobileDetails(mobile_numbers[0],0),MobileDetails(mobile_numbers[2],0)]#packed all three mobile numbers
                    
                    #new_address.mobile_number=[]
                    #new_address.mobile_number.extend(new_mobiles)



      
                   
                                                
                                 
                    
                    
                    session.add(new_campaign)
                    
                    
                    # commit the record the database
                    
                    
                    session.commit()
		    session.close()
                    engine.dispose()
                    dbconn.close()
                     
                    result["R00"]={"F1":1,"F0":"The campaign was added sucessfully"}
                    return (json.JSONEncoder().encode(result))                 
                     
                    
               except Exception as e:
                    session.close()
                    engine.dispose()
                    result["R00"]={"F1":-6,"F0":e.message}
                    dbconn.close()
                    return (json.JSONEncoder().encode(result)) 
          
         


     
         

 
    


     def saveOneSMSInDB(self):
          
          sms_details="" 
          date_captured="" 
          time_captured="" 
          mobile_no=""
          message_sent_status=""
          result={}
          allow_insert=1
          
          # Get data from fields
          try:
                            
               sms_details=self.myjson["MessageBody"] 
               mobile_no=self.myjson["MobNo"] 
               
               

               
                
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]='There was an error in processing a JSON object:%s'%e
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          

          if (sms_details=="None"):
               #print "Content-type: text/html\n" 
               result["message"]="There is an error in sending your message due to missing of some information"
               return (json.JSONEncoder().encode(result)) 


                   
          try:
              myjson2={"recipient":mobile_no,"message":sms_details}
              obj=QueueFeedback(myjson2)
              res=obj.saveFeedbackInDB()
              #res=obj.getQueuedSMS() # Queued messages and send them
              #Get the ID of the inserted message
              res=json.loads(res)
              msg_id=int(res["ID"])
              
              if msg_id>=0:
                    res=obj.sendOneSMS(msg_id)
                    res=json.loads(res)
                    #result["ID"]=msg_id
                    #result["message"]="Your message has already been scheduled for sending"
                    result["message"]="%s"%res["message"]
              else:
                    result["message"]="Fail to send the message" 
              return (json.JSONEncoder().encode(result))         
                             
                    
          except Exception as e:
              result["message"]=e
              print result
              return (json.JSONEncoder().encode(result))  

     
     
myjson={}
obj=ManageCampaign(myjson)
msg=obj.saveOneCampaignInDB()
print msg
