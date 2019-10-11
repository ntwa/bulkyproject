#!/usr/bin/env python
import datetime
import sys,json
#sys.path.insert(0, 'C:\\workspace\\test\\helloword\\sqlalchemy.zip')
#sys.path.insert(0, 'sqlalchemy.zip')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from collections import OrderedDict
import urllib2,urllib
import time

from bulkysms.database.base import Base
from bulkysms.database.dbinit import db,dbconn

import bulkysms.database.sms_feedback_module
from manage_message_template import ManageMessageTemplates
from bulkysms.database.sms_feedback_module import Feedback

Base.metadata.create_all(db)



class QueueFeedback:
     def __init__(self,myjson):
          self.myjson=myjson
     def changeQueuedSMSStatus(self,msg_id):
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
                           
                           req.add_header('Authorization', '6ICXH17PTLqKjXIUBz-VLA==')
                           #req.add_header('Authorization', 'b3itx5JgS-O7nc7xJ9KVlw==') 
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





     def sendOneSMS(self,msg_id):
          result={}
          posn=0
          keyletter="R"

          try:
              
          
                     
               mobile=self.myjson["recipient"]
               message=self.myjson["message"]
                    
  
               message="%s.... [From ASAS Dairies]"%message
       
               values={"content": message, "to": [mobile]}

               url="https://platform.clickatell.com/messages"           
                  
               engine=db
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
                           
                         req.add_header('Authorization', '6ICXH17PTLqKjXIUBz-VLA==')
                            
                         #page = urllib2.urlopen(req)#comment
                         #print page.info()#comment
                         response = urllib2.urlopen(req)
                         
                         data = json.load(response)  
                         #json.loads(json.JSONEncoder().encode(data))["messages"][0]["accepted"]#comment
                         accepted_status=json.loads(json.JSONEncoder().encode(data))["messages"][0]["accepted"]
                         msg_error_status=json.loads(json.JSONEncoder().encode(data))["messages"][0]["errorCode"]
                         snd_error_status=json.loads(json.JSONEncoder().encode(data))["messages"][0]["errorDescription"]
                         print data
                         
                         
                         if accepted_status == True and msg_error_status==None and snd_error_status==None:
                              result["message"]="SMS was sent successfully"
                              result["status"]=1
                         else:
                              result["message"]="SMS failed to send due to the following error: '%s'"%snd_error_status
                              result["status"]=-6
                         
                         

                         #page.close()           

                  
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
                    
                           

                       
          except Exception as e:
                    msg_details={}
                    msg_details["Mobile"]=-1
                    msg_details["Message"]=e
                    result["R0"]=msg_details         
          #result["message"]="SMS was sent successfully"
          return (json.JSONEncoder().encode(result))                   

     def saveFeedbackInDB(self):
          
          
          result={}
          allow_insert=1
          # Get data from fields
          try:
          
               message=self.myjson["message"] 
               recipient=self.myjson["recipient"]
               contact_id=self.myjson["contact_id"]
               recipient_name=self.myjson["fullname"]
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
          
               new_feedback=Feedback(recipient,contact_id,fullname,message,None,None,None,None)
                    
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
 
myjson={"message":"Your OTP is 456789.. Sent by Yotte Messaging App ","recipient":"+255742340759"}
obj=QueueFeedback(myjson)
#result=obj.getQueuedSMS()
#result=obj.saveFeedbackInDB()
result=obj.sendOneSMS(112)
print result
#msg_ids=json.loads(result)


#for msg in msg_ids.items():
# key,msg_id=msg
#  print key,msg_id["Id"]
#  status_change_result=obj.changeQueuedSMSStatus(msg_id["Id"])
#  print status_change_result
          
            

