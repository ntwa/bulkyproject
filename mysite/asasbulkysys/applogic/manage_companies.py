#!/usr/bin/env python
import datetime
import sys,json
from random import randint
import os
import hashlib
import binascii

import urllib2,urllib

from sqlalchemy.orm import sessionmaker


from collections import OrderedDict

from bulkysms.database.base  import Base
from bulkysms.database.dbinit import db,dbconn

import bulkysms.database.address_book_module

import bulkysms.database.sms_feedback_module

Base.metadata.create_all(db)

from bulkysms.database.address_book_module import Company, CompanyUsers



class CompanyManager:
     def __init__(self,myjson):
          self.myjson=myjson




     def verifyCompanyMobile(self):
          status={}
          
          try:
               code=self.myjson["Code"]
               saltkey=self.myjson["Token"]
               company_id=self.myjson["CompanyID"]
               #separate salt and key.
               salt=binascii.unhexlify(saltkey[:64].encode('utf-8'))
               key=binascii.unhexlify(saltkey[64:].encode('utf-8'))

               new_key = hashlib.pbkdf2_hmac('sha256',code.encode('utf-8'), salt, 100000)
               new_key=binascii.hexlify(new_key).decode('utf-8')
               #print saltkey[64:]
               #print "separator"
               #print new_key
               if new_key == saltkey[64:]:
                    print('Code is correct')
                    #Now change verification status in  the database
                    engine=db
                    # create a Session
                    Session = sessionmaker(bind=engine)
                    session = Session()
                    res=session.query(Company).filter(Company.id==company_id).first()
                    if res is None:
                        print "Fail to verify number"
             
                    else:
                        res.mobile_verified=1
                        session.commit()
                        print "Number verified"
          	    session.close()
                    engine.dispose()
                    dbconn.close()
                    status["code"]=1
                    status["descr"]="Verification Completed Successfuly"
                    
                    
               else:
                    print('Code is incorrect')
                    status["code"]=-2
                    status["descr"]="Code is incorrect"

               return (json.JSONEncoder().encode(status))
               
               
          except Exception as e:
               
               status["code"]=-1
               status["descr"]="Failed due to the following error: %s"%e
               return (json.JSONEncoder().encode(status))



     def sendVerificationCode(self):
          status={}
          result={}
          try:
               
               #generate random code
               code=randint(100000,999999)
               code_str='%s'%code
               #company_phone=self.myjson["MobileNumber"]
               

               #Now generate salt.
               salt = os.urandom(32)
               num_iterations=100000
               key = hashlib.pbkdf2_hmac('sha256', code_str.encode('utf-8'), salt, num_iterations)
               hash_bytes=salt+key
               hash_string = "%s%s"%(binascii.hexlify(salt).decode('utf-8'),binascii.hexlify(key).decode('utf-8'))
               #hash_string = binascii.hexlify(hash_bytes).decode('utf-8')
               status["code"]=hash_string
               status["descr"]="Key generated successfully"
               print "Sent code: %s"%code_str
               print "salt=%s"%binascii.hexlify(salt).decode('utf-8')
               print "key=%s"%binascii.hexlify(key).decode('utf-8')
               print "complete code=%s"%hash_string
 

               return (json.JSONEncoder().encode(status))
               
               #now the next task is to send the uncrypted code to a registered phone number
               #Disable this for now
               '''
               mobile="+255742340759"
               message=code_str
                    
  
               message="Verification code: %s.... [From Yotte Messaging]"%message
       
               values={"content": message, "to": [mobile]}

               url="https://platform.clickatell.com/messages"
               
 
               try:
                        
                    data=json.JSONEncoder().encode(values)
                    req = urllib2.Request(url, data)
                    req.add_header("Content-type",'application/json')
                    req.add_header("Accept",'application/json')
                           
                    req.add_header('Authorization', 'b3itx5JgS-O7nc7xJ9KVlw==')
                    print req
                            
                         #page = urllib2.urlopen(req)
                         #print page.info()
                    response = urllib2.urlopen(req)
                    #print response    
                    data = json.load(response)  
                    print data
                         #json.loads(json.JSONEncoder().encode(data))["messages"][0]["accepted"]
                    accepted_status=json.loads(json.JSONEncoder().encode(data))["messages"][0]["accepted"]
                    msg_error_status=json.loads(json.JSONEncoder().encode(data))["messages"][0]["error"]
                    snd_error_status=json.loads(json.JSONEncoder().encode(data))["error"]
                         #print data
                         
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
             '''
               

               
               
          except Exception as e:
               status["code"]="-1"
               status["descr"]="Failed due to the following error: %s"%e
               return (json.JSONEncoder().encode(status))
 


     def registerCompanyDetails(self):
          status={}
          
          try:
               company_name=self.myjson["CompanyName"]
               business_descr=self.myjson["BusinessDescr"]
               postal_address=self.myjson["PostalAddress"]
               street_name=self.myjson["StreetName"]
               ward_name=self.myjson["WardName"]
               district_name=self.myjson["DistrictName"]
               region_name=self.myjson["RegionName"]
               email_address=self.myjson["EmailAddress"]
               mobile_number=self.myjson["MobileNumber"]
               user_id=self.myjson["UserID"]
               
          except Exception as e:
               pass
               status["code"]=-1
               status["descr"]="Failed due to the following error: %s"%e
               return (json.JSONEncoder().encode(status))


          try:
               
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()

	       new_company=Company(company_name,business_descr,postal_address,street_name,ward_name,district_name,region_name,mobile_number,email_address)
               
               session.add(new_company)
               session.commit()
               
               new_company_user=CompanyUsers(new_company.id,user_id)
               session.add(new_company_user)
               session.commit()

               status["code"]=1
               status["descr"]="Successful"
               #return (json.JSONEncoder().encode(status))

          except Exception as e:
        
               status["code"]=-1
               status["descr"]="Failed due to the following error: %s"%e
               

          session.close()
          engine.dispose()
          dbconn.close()
          return (json.JSONEncoder().encode(status))

          
          
               
               



     def getCompanyDetails(self):
           
          #The tuple is used for definition of a JSON object
          company_tuple={}
          
           
           
	 
	  #get all contacts and their respective details from the database
          try:
               
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               result={}    

               res=session.query(Company,CompanyUsers).filter(Company.id==CompanyUsers.company_id).filter(CompanyUsers.user_id==self.myjson["user_id"]).first()
               if res is None:
		    

                    
                    company_tuple["company_id"]=-1
                    company_tuple["company_name"]="No Name"
                    
                    
                   
               else:
		    company_det,company_user=res
                    company_tuple["company_id"]=company_det.id
                    company_tuple["company_name"]=company_det.company_name
                    company_tuple["postal_addess"]=company_det.postal_address
                    company_tuple["district"]=company_det.district
                    company_tuple["region"]=company_det.region
		    company_tuple["ward"]=company_det.ward
		    company_tuple["street"]=company_det.street
		    company_tuple["mobile_number"]=company_det.mobile_number
		    company_tuple["email_address"]=company_det.email_address
                    company_tuple["mobile_verified"]=company_det.mobile_verified
               
               session.close()
               engine.dispose()
               dbconn.close()

               return (json.JSONEncoder().encode(company_tuple))
	
                    
          except Exception as e:
	       company_tuple["company_id"]=-2
	       company_tuple["company_name"]="Failed to retrieve company name: %s"%e
               session.close()
               engine.dispose()
               dbconn.close()
               return (json.JSONEncoder().encode(company_tuple))
                     

               #result["R00"]={"F1":1,"F0":"The contact was recorded sucessfully"}
               #return (json.JSONEncoder().encode(result))
     
#Suser_id=5   
#myjson={"Code":"520622","Key":"61a5f4e32a2e41acbf5de6d5a5c87f9acb8788863d88680a9e43e56e760497c3d2416e1d2fbd60236450a70ae9bd3a078611816bf13c36dd643ac121058dfbfe"}
#obj=CompanyManager(myjson)
#msg=obj.sendVerificationCode()
#msg=obj.verifyCompanyMobile()
#print msg

#obj=CompanyManager(user_id)
#msg=obj.getCompanyDetails()
#print json.loads(msg)
#myjson={"CompanyName":"Coca Cola","BusinessDescr":"Manufacturing of soft drinks","PostalAddress":"35176", "StreetName":"Mikocheni Viwandani","WardName": "Mikocheni", "DistrictName":"Kinondoni","RegionName":"DSM","EmailAddress":"coca@fmail.com","MobileNumber":"0718255585","UserID":5}
#obj=CompanyManager(myjson)
#msg=obj.registerCompanyDetails()
#print msg
