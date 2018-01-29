#!/usr/bin/env python
import datetime,time,calendar
import sys,json
#sys.path.insert(0, 'C:\\workspace\\test\\helloword\\sqlalchemy.zip')
#sys.path.insert(0, 'sqlalchemy.zip')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.intermediary_module import Intermediary,Beneficiary,Comment,db,dbconn
from save_sms_feedback import QueueFeedback
from collections import OrderedDict
from manage_avatars import ManageAvatars


class SaveSMS:
     def __init__(self,myjson,b_id,i_id):
          self.myjson=myjson
          self.b_id=b_id
          self.i_id=i_id
     def first_day_of_month(self,d):
          return datetime.date(d.year, d.month, 1)
      
     def last_day_of_month(self,d):
          t=(calendar.monthrange(d.year,d.month))
          return datetime.date(d.year,d.month,t[1])


     def saveSMSInDB(self):
          
          smsdetails="" 
          date_captured="" 
          time_captured="" 
          mobile_no=""
          message_sent_status=""
          result={}
          allow_insert=1
          
          # Get data from fields
          try:
                            
               smsdetails=self.myjson["MessageBody"] 
               mobile_no=self.myjson["MobNo"] 
               date_captured=datetime.date.today()# today's date
               time_captured=time.strftime("%H:%M:%S")
               message_sent_status=False          
               

               
                
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]='There was an error in processing a JSON object:%s'%e
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          

          if (smsdetails=="None"):
               #print "Content-type: text/html\n" 
               result["message"]="There is an error in sending your message due to missing of some information"
               return (json.JSONEncoder().encode(result)) 


          if allow_insert==1:           
               try:
                    
               
                    #engine=db
                    # create a Session
                    #Session = sessionmaker(bind=engine)
                    
                    #session = Session()
                    
                 
     


                        
                    myjson2={"recipient":mobile_no,"message":sms_details}
                    obj=QueueFeedback(myjson2)
                    res=obj.saveFeedbackInDB()
                       
                     
                     
                    
               except Exception as e:
             

                    result["message"]=e
                    return (json.JSONEncoder().encode(result)) 
               
               result["message"]="Your message has already been scheduled for sending"
               return (json.JSONEncoder().encode(result))
     
     
#myjson={"MessageBody":"Hi mom. You have reached your activity goal this week. Keep it up!!","EventType":"Garden", "TeamName":"Cameroon","OptionalText":"Team y has left a comment in your garden"}
#obj=SaveComment(myjson,1,'ntwakatule')
#msg=obj.saveCommentInDB()
#msg=obj.getComments("Aquarium")
#print msg
