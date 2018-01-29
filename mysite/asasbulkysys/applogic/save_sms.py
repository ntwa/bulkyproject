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

     
     
#myjson={"MessageBody":"Hello. We wish you happy new year...","MobNo":"+255742340759"}
#obj=SaveSMS(myjson)
#msg=obj.saveOneSMSInDB()
#print msg
