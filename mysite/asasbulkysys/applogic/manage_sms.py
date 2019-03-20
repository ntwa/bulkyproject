#!/usr/bin/env python
import datetime,time,calendar
import sys,json
import pika
#import thread
import threading
#from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from save_sms_feedback import QueueFeedback
from collections import OrderedDict
#from bulkysms.database.address_book_module import AddressBook,MobileDetails,GroupMember,db,dbconn
import urllib2,urllib
import time
from bulkysms.database.base import Base
from bulkysms.database.dbinit import db,dbconn
import bulkysms.database.address_book_module
import bulkysms.database.sms_feedback_module
Base.metadata.create_all(db)

from bulkysms.database.address_book_module import AddressBook,MobileDetails,GroupMember
from bulkysms.database.sms_feedback_module import Feedback

class ScheduleSMS:
     def __init__(self,myjson):
          self.myjson=myjson
       
     def first_day_of_month(self,d):
          return datetime.date(d.year, d.month, 1)
      
     def last_day_of_month(self,d):
          t=(calendar.monthrange(d.year,d.month))
          return datetime.date(d.year,d.month,t[1])


#Code for storing SMS to DB and sending


     def changeQueuedSMSStatus(self,msg_id):
          print "Enter"
          result={}
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
                engine=db
               # create a Session
                Session = sessionmaker(bind=engine)
                session = Session()
                res=session.query(Feedback).filter(Feedback.id==msg_id).first()
                if res is None:
                   result["Message"]="Status for ID %s was not changed to sent"
                else:
                   res.status=1
                   session.commit()
                   result["Message"]="Status for ID %s was changed to sent"
                
          except Exception as e:
                result["Message"]=e

          return (json.JSONEncoder().encode(result))



     def getQueuedSMS(self):
          result={}
          posn=0
          keyletter="R"

          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
                engine=db
               # create a Session
                Session = sessionmaker(bind=engine)
                session = Session()
                res=session.query(Feedback).filter(Feedback.status==0).all()
                if res is None:
                   pass
                else:
                   for msg in res:
                       msg_details={}
                       key="%s%s"%(keyletter,posn)   
                       mobile=msg.recipient_mobile
                       message=msg.message
                       msg_id=msg.id
  
                       #mobile="27%s"%mobile[1:]
                       message="%s.... [Auto Generated SMS]"%message
                       '''
                       values = {'user' : 'wellnessapp',
                       'password' : 'AbGXWETGaKdEdD',
                       'api_id' : '3543084',
                       'to':mobile,
                       'text':message}

                       '''
                       values={"content": message,
                               "to": [mobile]}
             #"from": "ASAS Dairies"}
              #"binary": false,
              #"clientMessageId": "b3itx5JgS-O7nc7xJ9KVlw==",
              #"scheduledDeliveryTime": "yyyy-MM-dd'T'HH:mm:ssZ",
              #"userDataHeader": "0605040B8423F0",
              #"validityPeriod": 0,
              #"charset": "UTF-8"
              #}
                       url="https://platform.clickatell.com/messages"
                       #url="http://api.clickatell.com/http/sendmsg?"+urllib.urlencode(values)
                       #url="https://platform.clickatell.com/messages/http/send?apiKey=-eKVKLmnSEiQhYNaR5UApQ==&to=255718255585&content=Test again"
                       '''
                       api_key="-eKVKLmnSEiQhYNaR5UApQ=="
                       url="https://platform.clickatell.com/messages/http/send?apiKey=%s&to=%s&content=%s"%(api_key,mobile,message)
                       '''
                       try:
                           #req = urllib2.Request(url)
                           #req.add_header("User-Agent",'Mozilla/5.0')

                           #req.add_header("Content-type",'application/x-www-form-urlencoded')
                           #req.add_header("Content-type",'application/json')
                           #req.add_header("Accept",'application/json')
                           
                           #req.add_header('Authorization', 'b3itx5JgS-O7nc7xJ9KVlw==')
                           data=json.JSONEncoder().encode(values)
                           req = urllib2.Request(url, data)
                           req.add_header("Content-type",'application/json')
                           req.add_header("Accept",'application/json')
                           
                           req.add_header('Authorization', 'b3itx5JgS-O7nc7xJ9KVlw==')
                            
                           page = urllib2.urlopen(req)
                           print page.info()
                           #print page

                           page.close()           

                           #Pile all messages that need to be changed status    
                           #msg_details["Id"]=msg_id
                           #msg_details["Mobile"]=mobile
                           #msg_details["Message"]=message
                           #result[key]=msg_details      
                           posn=posn+1 
                           self.changeQueuedSMSStatus(msg_id)
                           time.sleep(5) # No need for this now
                           
                       except urllib2.HTTPError as error:
                           result["message"]="Error in sending message to clickatell with the following code: %s"%error.code
                           return (json.JSONEncoder().encode(result)) 
                           

                       
          except Exception as e:
                msg_details={}
                msg_details["Mobile"]=-1
                msg_details["Message"]=e
                result["R0"]=msg_details         
          result["message"]="SMS was sent successfully"
          return (json.JSONEncoder().encode(result)) 




     '''
     def sendOneSMS(self,msg_id):
          result={}
          posn=0
          keyletter="R"

          try:
              
          
                     
               mobile=self.myjson["recipient"]
               message=self.myjson["message"]
                    
  
               message="%s.... [From Yote App]"%message
       
               values={"content": message, "to": [mobile]}

               url="https://platform.clickatell.com/messages"           
                
               engine=db
               #print "%s: %s"%(mobile,values)
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               res=session.query(Feedback).filter(Feedback.id==msg_id).first()
               if res is None:
                    pass
               else:

                    try:
                        
                         data=json.JSONEncoder().encode(values)
                         req = urllib2.Request(url, data)
                         req.add_header("Content-type",'application/json')
                         req.add_header("Accept",'application/json')
                           
                         req.add_header('Authorization', 'b3itx5JgS-O7nc7xJ9KVlw==')
                            
                         #page = urllib2.urlopen(req)
                         #print page.info()
                         response = urllib2.urlopen(req)
                         
                         data = json.load(response)  
                         #json.loads(json.JSONEncoder().encode(data))["messages"][0]["accepted"]
                         accepted_status=json.loads(json.JSONEncoder().encode(data))["messages"][0]["accepted"]
                         msg_error_status=json.loads(json.JSONEncoder().encode(data))["messages"][0]["error"]
                         snd_error_status=json.loads(json.JSONEncoder().encode(data))["error"]
                         #print data
                         
                         if accepted_status == True and msg_error_status==None and snd_error_status==None:
                              result["message"]="SMS was sent successfully"
                              result["status"]=1
                              self.changeQueuedSMSStatus(msg_id)
                         else:
                              result["message"]="SMS failed to send due to the following error: '%s'"%snd_error_status
                              result["status"]=-6
                         

                         #page.close()           
                         #print "Finish 1"
                         
                         #self.changeQueuedSMSStatus(msg_id)
                    
                    except urllib2.URLError as err: 
                         result["message"]="Error: '%s'. Check if you are connected to the Internet. If the problem persists contact the developer"%err           
                         result["status"]=-6
                         return (json.JSONEncoder().encode(result)) 
                                
                           
                    except Exception as error:
                         #print response.code
                         result["message"]="Error in sending message with the following code: %s"%error
                         result["status"]=-6
                         return (json.JSONEncoder().encode(result)) 
                    
                           

               #print "Finish 2"             
          except Exception as e:
               msg_details={}
               msg_details["Mobile"]=-1
               msg_details["Message"]=e
               result["R0"]=msg_details 
          #print result
          #print "Finish 3"             
          #result["message"]="SMS was sent successfully"
          return (json.JSONEncoder().encode(result))                   
     '''
     def sendOneSMS(self, msg_id):
          result={}
          try:
              
          
               message={}  
               message["msgID"]="Default"    
               mobile_number=self.myjson["recipient"]
               outgoing_message=self.myjson["message"]
               connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
               channel = connection.channel()
               channel.queue_declare(queue='yote_sms_multithreading')
               message["to"]=mobile_number
               message["content"]=outgoing_message
               message_out=json.JSONEncoder().encode(message)
               channel.basic_publish(exchange='',routing_key='yote_sms_multithreading', body=message_out)
               print " [x] Scheduled message: '%s' to be sent to '%s'"%(message["content"],message["to"])
               connection.close()
               #result["message"]="SMS was scheduled successfully for sending"

          except Exception as e:
               print "Failed to schedule a message with ID '%s'"%msg_id
               #result["message"]="Error in sending message with the following code: %s"%error

          return (json.JSONEncoder().encode(result)) 

                    
     def storeSMSInDB(self):
          
          
          result={}
          allow_insert=1
          # Get data from fields
          try:
          
               message=self.myjson["message"] 
               recipient=self.myjson["recipient"]
               #url=self.myjson["url"]
               #pic=self.myjson["pic"]
               #name=self.myjson["name"]
               #caption=self.myjson["caption"]
               #description=self.myjson["description"]
               
               e="Error"
                        
                             
          except Exception as e:
               messages_tuples={}
               messages_tuple={}
     
               key1="R"
               key2="F"
               first_posn=0
               second_posn=0
               messages_tuple[key2+"%d"%second_posn]=e
               second_posn=second_posn+1
                                                                                                                                                                             
                                                                                                                                                                           
               messages_tuple[key2+"%d"%second_posn]=-1
               second_posn=0 
               if first_posn<10:
                    key1="R0"
               else:
                    key1="R"
                                                                                                                                            
               messages_tuples[key1+"%d"%first_posn]=messages_tuple
                                                                                                                                          
               first_posn=first_posn+1
               messages_tuple={}
               return(json.JSONEncoder().encode(OrderedDict(sorted(messages_tuples.items(), key=lambda t: t[0]))))
          
                                        
                         
                         

          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
          
               new_feedback=Feedback(recipient,message)
                    
               session.add(new_feedback)
          
          
               # commit the record the database
          
          
               session.commit()
               result["message"]="The post was recorded successfully"
               result["ID"]=new_feedback.getID()
               
          except Exception as e:
               session.close()
               engine.dispose()
               result["message"]=e
               result["ID"]=-6
               return (json.JSONEncoder().encode(result)) 
          
          session.close()
          engine.dispose() 
          print "Message queue"
          return (json.JSONEncoder().encode(result))









#End of code for storing SMS to SB and sending



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
                          myjson2={"recipient":mobile_number,"message":sms}
                          #obj=QueueFeedback(myjson2)
                          #res=obj.saveFeedbackInDB()
                          self.myjson=myjson2
                          res=self.storeSMSInDB()

                          #res=obj.getQueuedSMS() # Queued messages and send them
                          #Get the ID of the inserted message
                          resmsg=json.loads(res)
                          msg_id=int(resmsg["ID"])
              
                          if msg_id>=0:
                            
                                #ressnd=self.sendOneSMS(msg_id)
                                #ressnd=json.loads(ressnd)
                                #result["message"]="%s"%ressnd["message"]
                              	try:
                              
                              		t1 = threading.Thread(target=self.sendOneSMS,args=(msg_id,))
       
                              		t1.start()
      
        		      		t1.join()
                              		result["message"]="Message to Group has already been submitted to be scheduled for sending"
        
                          	except Exception as e:
                              		result["message"]="Failed to start a thread for scheduling this message"

                                #Now change the status of a message to one to indicate already sent message
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
                          first_name=addrbk_rec.first_name
                          last_name=addrbk_rec.last_name


                    if sms_details.find("@@firstname@@",0):
                         sms_details=sms_details.replace("@@firstname@@",first_name)
                    if sms_details.find("@@lastname@@",0):
                         sms_details=sms_details.replace("@@lastname@@",last_name)
                   
                    myjson2={"recipient":mobile_no,"message":sms_details}
                  
                    #obj=QueueFeedback(myjson2)
                    #res=obj.saveFeedbackInDB()
                    self.myjson=myjson2
                    res=self.storeSMSInDB()
                    #res=obj.getQueuedSMS() # Queued messages and send them
                    #Get the ID of the inserted message
                    res=json.loads(res)
                    msg_id=int(res["ID"])
              
                    if msg_id>=0:

                        
                          #ressnd=self.sendOneSMS(msg_id)
                          #ressnd=json.loads(ressnd)
                          try:
                              #print "Thread started"
                              #thread.start_new_thread(self.sendOneSMS, (msg_id, ) )
                              t1 = threading.Thread(target=self.sendOneSMS,args=(msg_id,))
       
                              t1.start()
      
        		      t1.join()
                              result["message"]="Your message has already been submitted to be scheduled for sending"
        
                          except Exception as e:
                              result["message"]="Failed to start a thread for scheduling this message"

                          #result["ID"]=msg_id
                          
                          #result["message"]="%s"%ressnd["message"]
                    else:
                          result["message"]="Fail to send the message" 
                    return (json.JSONEncoder().encode(result))         
                             
                    
          except Exception as e:
              result["message"]=e
              print result
              return (json.JSONEncoder().encode(result))  

     
     

myjson={"MobNo":"+255742340759","MessageBody":"Asante. @@firstname@@. Majaribio yetu ya mfumo bado yanaendelea.", "SMSAudience":"Individual"}
obj=ScheduleSMS(myjson)
msg=obj.saveOneSMSInDB()
print msg
