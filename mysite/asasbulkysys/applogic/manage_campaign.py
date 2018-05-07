#!/usr/bin/env python
import datetime,time,calendar
import sys,json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from save_sms_feedback import QueueFeedback
from collections import OrderedDict
from bulkysms.database.sms_feedback_module import Campaign,CampaignDefinedMessages,db,dbconn


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
               res= session.query(Campaign).order_by(Campaign.campaign_name).all()
               
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

                         #Now get all messages that are part of eacha campaign
                         res_campaign_messages= session.query(CampaignDefinedMessages).filter(CampaignDefinedMessages.campaign_id==campaign_id).order_by(CampaignDefinedMessages.campaign_id).all()

                         message_tuple={}
                         level_two_json_counter=0
                         for one_msg_rec in res_campaign_messages:
                              if level_one_json_counter<10:
                                   key2="MTXT0"# append a zero. This is important in ordering keys alphabetically
                              else:
                                   key2="MTXT" 
                              message_tuple[key2+"%d"%level_two_json_counter]=one_msg_rec.message_txt
                              level_two_json_counter=level_two_json_counter+1 
           
                        
                         
                         campaign_tuple[key1+"%d"%level_one_json_counter]={"CampaignID":campaign_id, "campaign_name":campaign_rec.campaign_name, "campaign_description":campaign_rec.campaign_descr,"messagestxt": message_tuple}
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
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
     




     def saveOneCampaignInDB(self):
         
          allow_insert=1
          result={}
          # Get data from fields
          try:
  


               campaign_name=self.myjson["GroupName"]
               campaign_descr=self.myjson["CampaignDescr"]
               campaign_category=self.myjson["CampaignCategory"]
               target_level=self.myjson["Target_Level"]
               frequency_in_days=self.myjson["Frequency_in_Days"]
               is_it_life_time=int(self.myjson["is_it_life_time"])
               is_annual_delivery_date_constant=int(self.myjson["is_annual_delivery_date_constant"])
               msglst=self.myjson["Messages"]
               

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
                    
                   
                    
                    #search all messages to to be updated
                    for msgtuple in msglst:
                         msg_id=msgtuple[0]
                         msg_txt=msgtuple[1]
                         #search by ID
                    
                    	 resmsg= session.query(CampaignDefinedMessages).filter(CampaignDefinedMessages.id==msg_id).first()
                         
                         if resmsg is None:
                         #append this new message to the above campaign
                              res.campaign_messages.append(CampaignDefinedMessages(msg_txt))
                              session.merge(res)
                         else:
                         #update this msg txt to assume a new value
                              resmsg.message_txt=msg_txt
                                        
                       
                                                
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
                                   
               result["message"]="Error: %s. (Line 245)"%e
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
               
          
          if allow_insert==1: 
               #If we get here it means the record doesn't exist hence we need to create it for the first time.          
               try:
                    
                
                    new_campaign=Campaign(campaign_name,campaign_descr,campaign_category,target_level,frequency_in_days,is_it_life_time,is_annual_delivery_date_constant)

                    #Now append messages for this campaign
                    new_campaign_messages=[]
                    for msg_tuple in msglst:
                        
                        new_campaign_messages.append(CampaignDefinedMessages(msg_tuple[1]))
                  
                    new_campaign.campaign_messages=[]
                    new_campaign.campaign_messages.extend(new_campaign_messages)       
                                                
                 
                    
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

    
     
#myjson={"campaign_name":"Birthday Greetings","campaign_descr":"This campaign has been dedicated for birthday greetings to customers","campaign_category":"Individual Best Wishes","target_level":"Individual","frequency_in_days":"Selective Days","is_it_life_time":"1","is_annual_delivery_date_constant":"1","messages":[[3,"We wish you happy birthday. Thank you for being our loyal customer"],[2,"Happy birthday. We value you as our esteemed customer"],[1,"As you celebrate your birthday, we wish you more success in business. Thank for being with us all this time."]]}

#myjson={}
#obj=ManageCampaign(myjson)
#msg=obj.retrieveCampaignDetailsFromDB()
#msg=obj.saveOneCampaignInDB()

#print msg
