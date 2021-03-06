#!/usr/bin/env python
import datetime,time,calendar
import sys,json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from collections import OrderedDict

from bulkysms.database.base import Base
from bulkysms.database.dbinit import db,dbconn
import bulkysms.database.address_book_module

Base.metadata.create_all(db)

from save_sms_feedback import QueueFeedback
from bulkysms.database.address_book_module import AddressBook,MobileDetails,GroupMember

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
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               result={}  
                            
               sms_details=self.myjson["MessageBody"] 
               mobile_no=self.myjson["MobNo"] 
               sms_audience=self.myjson["SMSAudience"]
               #sms_generalization=self.myjson["SMSGeneralization"]
              
               insertion_point=0
               '''
               while insertion_point>=0:
                    #now extract the string that comes after.
                    insertion_point=sms_details.find('@@',[insertion_point-len(sms_details)])
                    if insertion_point == -1:
                         break
                    insertion_point=insertion_point+2 # skip two positions
                    end_point=sms_details.find('@@',[insertion_point-len(sms_details)]) 

                    insertion_point=end_point+2
               '''
         

          
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
              if sms_audience=="Bulky":
                    #Then iterate to find all mobile numbers of all members of the group so that the message can be broadcasted.
                    mobile_numbers=[]
                    res= session.query(AddressBook,GroupMember).filter(AddressBook.id==GroupMember.contact_id).filter(GroupMember.group_id==mobile_no).order_by(AddressBook.first_name).order_by(AddressBook.last_name).all()
                    for addrbk_rec,group_rec in res:
                          #Now get the first mobile phone number.
                          resmobile=session.query(MobileDetails).filter(MobileDetails.contact_id==addrbk_rec.id).filter(MobileDetails.is_it_primary_number==True).first()
                          first_name=addrbk_rec.first_name
                          last_name=addrbk_rec.last_name
                          contact_id=addrbk_rec.id
                          fullname="%s %s"%(first_name,last_name)

                          if sms_details.find("@@firstname@@",0):
                                sms=sms_details.replace("@@firstname@@",first_name)
                          if sms_details.find("@@lastname@@",0):
                                sms=sms.replace("@@lastname@@",last_name)

                          if resmobile is None:
                                continue #skip this person as they don't have a mobile phone
                          else:
                                mobile_number=resmobile.mobile_number #get the mobile number
                                mobile_numbers.append(mobile_number)# We will use this incase a message is not personalized we will send one message to many numbers
                          #Now prepare a message for this user incase a message is personalized
                          myjson2={"recipient":mobile_no,"message":sms_details,"fullname":fullname,"contact_id":contact_id}
                          obj=QueueFeedback(myjson2)
                          res=obj.saveFeedbackInDB()

                          #res=obj.getQueuedSMS() # Queued messages and send them
                          #Get the ID of the inserted message
                          resmsg=json.loads(res)
                          msg_id=int(resmsg["ID"])
              
                          if msg_id>=0:
                                ressnd=obj.sendOneSMS(msg_id)
                                ressnd=json.loads(res)
                                #result["ID"]=msg_id
                                #result["message"]="Your message has already been scheduled for sending"
                                result["message"]="%s"%ressnd["message"]
                          else:
                                result["message"]="Fail to send the message" 
                    return (json.JSONEncoder().encode(result)) 
              else: 
                     
                   # get first name and last name incase they are needed
                    resdetails= session.query(AddressBook,MobileDetails).filter(AddressBook.id==MobileDetails.contact_id).filter(MobileDetails.mobile_number==mobile_no).order_by(AddressBook.first_name).order_by(AddressBook.last_name).first()
                    if resdetails is None:
                          first_name=""
                          last_name=""
                        
                    else:
                          addrbk_rec, mobile_rec=resdetails
                          contact_id=addrbk_rec.id
                          first_name=addrbk_rec.first_name
                          last_name=addrbk_rec.last_name

                    fullname="%s %s"%(first_name,last_name)      


                    if sms_details.find("@@firstname@@",0):
                         sms_details=sms_details.replace("@@firstname@@",first_name)
                    if sms_details.find("@@lastname@@",0):
                         sms_details=sms_details.replace("@@lastname@@",last_name)
                   
                    myjson2={"recipient":mobile_no,"message":sms_details,"fullname":fullname,"contact_id":contact_id}
                     
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

     
     
myjson={"MobNo":"+255742340759","MessageBody":"Hello Mr. @@firstname@@. We remind you to pay your outstanding bill", "SMSAudience":"Individual"}
obj=SaveSMS(myjson)
msg=obj.saveOneSMSInDB()
print msg
