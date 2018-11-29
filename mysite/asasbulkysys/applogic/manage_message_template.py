#!/usr/bin/env python
import datetime,time,calendar
import sys,json
#from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from bulkysms.database.message_templates_module import TemplateCategory,MessageTemplates,MessageSignature,db,dbconn

#from sqlalchemy import ForeignKey, ForeignKeyConstraint
#from sqlalchemy import Column, Date, Integer, String, Boolean, Enum, Time, Float
#from sqlalchemy.orm import relationship, backref,sessionmaker
#from sqlalchemy.pool import NullPool
#from sqlalchemy.ext.declarative import declarative_base


from collections import OrderedDict

from bulkysms.database.base  import Base
from bulkysms.database.dbinit import db,dbconn
import bulkysms.database.message_templates_module

Base.metadata.create_all(db)

from bulkysms.database.message_templates_module import TemplateCategory,MessageTemplates,MessageSignature



class ManageMessageTemplates:
     def __init__(self,myjson):
          self.myjson=myjson

     def retrieveTemplateCategories(self):
          
          result={}
          
          records_counter=0
          try:
               

               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               res=session.query(TemplateCategory).all()
               for template_category_record in res:
                    if records_counter<10:
                         key="TC0" #part of forming a key to json object for each category
                    else:
                         key="TC" #part of forming a key to json object for each category
                    record={}
                    record["ID"]=template_category_record.id
                    record["CN"]=template_category_record.template_category_name     
                    result[key+"%d"%records_counter]=record
                    records_counter=records_counter+1


               session.close()
               engine.dispose()         
               dbconn.close()
               return(json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))      

          except Exception as e:
               
               session.close()
               engine.dispose()         
               dbconn.close()

               #print "Content-type: text/html\n" 
                                   
               result["message"]="Error: %s."%e
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()

         
       

     def saveTemplateCategoryInDB(self):
         
          allow_insert=1
          result={}
          # Get data from fields
          try:
               '''             
               firstname=self.myjson["FName"]        
               '''
               template_category_name=self.myjson["CategoryName"]  
               template_category_id=self.myjson["CategoryId"]          
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]="Error: '%s' encountered in editing the 'The Template Category'. If the error persists contact support@lktecautomation.com"%e
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          

          if template_category_name=="":
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

               #First check if there is any category with the same name in the database

               res= session.query(TemplateCategory).filter(TemplateCategory.template_category_name==template_category_name).first()
               if res is None:
                                   
                    # querying for a record if it exists already.
                    res= session.query(TemplateCategory).filter(TemplateCategory.id==template_category_id).first()
                    
                    if res is None:
                         session.close()
                         engine.dispose()
                         dbconn.close()
                    else:
                         #if it exists, then update the record in the database.
                         template_category_record=res
                         template_old_category_name=template_category_record.template_category_name

                         template_category_record.template_category_name=template_category_name

                         #template_category_record_id=res.id        
                                              
                         session.commit() #now commit this session                         
                         allow_insert=0 #Reset allow to zero so that the code doesn't attempt to insert a new record
                         #size=size-1 #ignore the last value because it has arleady been updated
                         
                         result["message"]="The category '%s' has been renamed to \"%s\"."%(template_old_category_name, template_category_name)

                         session.close()  
                         engine.dispose()   
                         dbconn.close()
                         #we wind up our update operation and notify the use of the outcome.
                         return (json.JSONEncoder().encode(result)) 
               else:
                    #Now check if the existing name corresponds to the ID we want to update. If true then it means the user has not updated anything from the form

                    res_cat= session.query(TemplateCategory).filter(TemplateCategory.id==template_category_id).first()
                    if res_cat is None:
                         result["message"]="Error: The category with name '%s' already exists. Find a unique category name"%template_category_name 
                    else:
                         result["message"]="The category '%s' has been updated."%template_category_name

                    session.close()
                    engine.dispose()
                    dbconn.close()
                    return (json.JSONEncoder().encode(result)) 



                                        
          except Exception as e:
               #if we get here the entire operation has failed so we have wind up all attempts to transact and close the database and then notify the user about the failure.
               session.close()
               engine.dispose()         
               dbconn.close()

               #print "Content-type: text/html\n" 
                                   
               result["message"]="Error: %s. (Line 70)"%e
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
               
          if allow_insert==1: 
               #If we get here it means the record doesn't exist hence we need to create it for the first time.          
               try:
                    
                
                    new_template_category=TemplateCategory(template_category_name)
                    
                    session.add(new_template_category)
                    
                    #commit the record the database
                    
                    session.commit()
                    session.close()
                    engine.dispose()
                    dbconn.close()
                     
                    result["R00"]={"F1":1,"F0":"`The SMS Template Category' was added sucessfully"}
                    return (json.JSONEncoder().encode(result))                 
                    
               except Exception as e:
                    session.close()
                    engine.dispose()
                    result["R00"]={"F1":-6,"F0":e.message}
                    dbconn.close()
                    return (json.JSONEncoder().encode(result)) 




     def retrieveSMSTemplates(self):
          
          result={}

          
          try:
               

               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               res=session.query(TemplateCategory).all()
               outer_records_counter=0

               for template_category_record in res:
                    if outer_records_counter<10:
                         key1="TC0" #part of forming a key to json object for each category
                    else:
                         key1="TC" #part of forming a key to json object for each category
                    record={}
                    template_category_id=template_category_record.id
                    template_category_name=template_category_record.template_category_name  
                    record["ID"]=template_category_id
                    record["CN"]=template_category_name

                    #now get all messages for rhis category
                    res_templates=session.query(MessageTemplates).filter(MessageTemplates.template_class_id==template_category_id).all()
                    templates={}
                    inner_records_counter=0
                    for message_template_record in res_templates:
                         if inner_records_counter<10:
                              key2="TM0" #part of forming a key to json object for each template
                         else:
                              key2="TM" #part of forming a key to json object for each template
                         one_template={}
                         one_template["TempId"]=message_template_record.id
                         one_template["TempCont"]=message_template_record.template_content

                         templates[key2+"%d"%inner_records_counter]=one_template
                         inner_records_counter=inner_records_counter+1


                    record["Templates"]=templates #puit all messages in the ids to the respective category
                        
                    result[key1+"%d"%outer_records_counter]=record
                    outer_records_counter=outer_records_counter+1


               session.close()
               engine.dispose()         
               dbconn.close()
               return(json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))      

          except Exception as e:
               
               session.close()
               engine.dispose()         
               dbconn.close()

               #print "Content-type: text/html\n" 
                                   
               result["message"]="Error: %s."%e
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()



     def saveSMSTemplateInDB(self):
         
          allow_insert=1
          result={}
          # Get data from fields
          try:


               template_category_id=self.myjson["CategoryId"]
               sms_template_id=self.myjson["TemplateId"]
               template_content=self.myjson["TemplateContent"]
                        
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]="Error: '%s' encountered in adding new 'SMS Template'. If the error persists contact support@lktecautomation.com."%e
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          

          if template_content =="":
               #print "Content-type: text/html\n" 
               result["message"]="Error: You did not enter any detail for template"
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
               res= session.query(MessageTemplates).filter(MessageTemplates.id==sms_template_id).first()
               
               if res is None:
                    pass
                 
                    #session.close()
                    #engine.dispose()
                    #dbconn.close()
               else:

                    #Now check if the content exists under under existing categories.
                    res_template= session.query(MessageTemplates).filter(MessageTemplates.template_content==template_content).filter(MessageTemplates.template_class_id==template_category_id).first()
                    if res_template is None:
                         pass

                    else:
                         #It means it is just an update of a template with content tht is not different from existing template there fore ignore any changes 
                         result["message"]="The record has been updated"
                         return (json.JSONEncoder().encode(result))

                    #if it exists, then update the record in the database.
                    template_content_record=res
                    template_content_record.template_content=template_content

                                
                                                
                    session.commit() #now commit this session                         
                    allow_insert=0 #Reset allow to zero so that the code doesn't attempt to insert a new record
                    #size=size-1 #ignore the last value because it has arleady been updated
                    
                    result["message"]="The record has been updated"
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
                                   
               result["message"]="Error: %s. (Line 70)"%e
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
               
          if allow_insert==1: 
               #If we get here it means the record doesn't exist hence we need to create it for the first time.          
               try:

                    res= session.query(TemplateCategory).filter(TemplateCategory.id==template_category_id).first()
                    if res is None:
                         result["message"]="Error: Category for this message is undefined"
                         return (json.JSONEncoder().encode(result))
                    else:
                         pass

                    #Now check for duplication if there is a template with exactly the same content as the one to be created 


                    res_template_existence= session.query(TemplateCategory,MessageTemplates).filter(TemplateCategory.id==template_category_id).filter(TemplateCategory.id==MessageTemplates.template_class_id).filter(MessageTemplates.template_content==template_content).first()
                    if res_template_existence is None:
                         pass
                    else:
                         categorypart,templatepart=res_template_existence
                         #Ensure that template is not duplicated undet the same tempkate category.
                         result["message"]="Duplication Error: The content of the template you are trying to create under category  '%s' already exists under the same category."%categorypart.template_category_name
                         return (json.JSONEncoder().encode(result))

                  
                    # Create the new template  
                    new_template=MessageTemplates(template_content)

                    res.template_messages.append(new_template)
                   
                    session.merge(res)
                    
                    #session.add(new_template)
                    
                    #commit the record the database
                    
                    session.commit()
                    session.close()
                    engine.dispose()
                    dbconn.close()
                     
                    result["R00"]={"F1":1,"F0":"`The SMS Template' was added sucessfully."}
                    return (json.JSONEncoder().encode(result))                 
                     
                    
               except Exception as e:
                    session.close()
                    engine.dispose()
                    result["R00"]={"F1":-6,"F0":e.message}
                    dbconn.close()
                    return (json.JSONEncoder().encode(result)) 


     def configureSMSSignature(self):
          pass
          result={}
          # Get data from fields
          try:
               '''             
               firstname=self.myjson["FName"]        
               '''
               signature_id=self.myjson["SigId"]  
               signature_content=self.myjson["SigContent"]
               signature_status=self.myjson["SigStatus"]
               action=self.myjson["Action"]          
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]="Error: '%s' encountered in editing the SMS signature. If the error persists contact support@lktecautomation.com"%e
               return (json.JSONEncoder().encode(result)) 

          try: 
               #setting session
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db

               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
          except Exception as e:
               result["message"]="Error: '%s'. If the error persists contact support@lktecautomation.com"%e
               return (json.JSONEncoder().encode(result)) 


     
          if action=="Update":
               if signature_id==-1:
                    try:
                          #Now check is the signature has been selected to be primary so that we reset all other signatures to non primary before inserting

                         if signature_status==1:
                              #then 
                              res_all_signatures=session.query(MessageSignature).all()
                              for one_signature in res_all_signatures:
                                   one_signature.signature_status=0
                              if res_all_signatures is None:
                                   pass
                              else:
                                   session.commit()
                                    
                                  
                         
                         new_signature=MessageSignature(signature_content,signature_status)
                        
                         session.add(new_signature)
                         
                         #commit the record the database
                         
                         session.commit()

                        
                         session.close()
                         engine.dispose()
                         dbconn.close()
                          
                         result["message"]="The SMS Signature' was added sucessfully."
                         return (json.JSONEncoder().encode(result))       
                    except Exception as e:
                         result["message"]="Error: %s."%e
                         return (json.JSONEncoder().encode(result)) 
                         session.close()
                         engine.dispose()
                         dbconn.close()
               else:
                    
                    try:
                         
                         res_signature= session.query(MessageSignature).filter(MessageSignature.id==signature_id).first()
                         if res_signature is None:
               
                              result["message"]="Error: The signature is not recognized"
                              return (json.JSONEncoder().encode(result)) 
                         else:

                              if signature_status==1:
                                   #then 
                                   res_all_signatures=session.query(MessageSignature).all()
                                   for one_signature in res_all_signatures:
                                        one_signature.signature_status=0
                                   if res_all_signatures is None:
                                        pass
                                   else:
                                        session.commit()
                              elif signature_status==0:
                                   if res_signature.signature_status==1:
                                        #Don't change the status until a different signature has been designated as primary
                                        signature_status=1


                              res_signature.signature_content=signature_content
                              res_signature.signature_status=signature_status
                              session.commit()

                         session.close()
                         engine.dispose()
                         dbconn.close()
                          
                         result["message"]="The SMS Signature' has been added sucessfully."
                         return (json.JSONEncoder().encode(result))       
                    except Exception as e:
                         result["message"]="Error: %s."%e
                         return (json.JSONEncoder().encode(result)) 
                         session.close()
                         engine.dispose()
                         dbconn.close()

          elif action=="Delete":
               try:
                         
                    res_signature= session.query(MessageSignature).filter(MessageSignature.id==signature_id).first()
                    if res_signature is None:
               
                         result["message"]="Error: No signature selected for deletion"
                         return (json.JSONEncoder().encode(result)) 
                    else:
                         if signature_status==1:
                              session.close()
                              engine.dispose()
                              dbconn.close()
                    
                              result["message"]="Error: This is a primary signature. First designate the other signature as the primary before deleting this."
                              return (json.JSONEncoder().encode(result)) 
                         session.delete(res_signature)
                         session.commit()

                    session.close()
                    engine.dispose()
                    dbconn.close()
                          
                    result["R00"]={"F1":1,"F0":"`The SMS Signature' has been deleted sucessfully."}
                    return (json.JSONEncoder().encode(result))       
               except Exception as e:
                    result["message"]="Error: %s."%e
                    return (json.JSONEncoder().encode(result)) 
                    session.close()
                    engine.dispose()
                    dbconn.close()
          else:
               result["message"]="No action was taken because you didn't select any."
               return (json.JSONEncoder().encode(result)) 


     def getPrimarySignature(self):
          result={}
          try:
          
               engine=db

               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               res_signature= session.query(MessageSignature).filter(MessageSignature.signature_status==1).first()

               if res_signature is None:
                    result["message"]="...."
               else:
                    result["message"]=res_signature.signature_content


               session.close()
               engine.dispose()
               dbconn.close()
               return (json.JSONEncoder().encode(result)) 


          except Exception as e:
               result["message"]="Error: %s."%e
               return (json.JSONEncoder().encode(result)) 
               session.close()
               engine.dispose()
               dbconn.close()




     def getAllSignatures(self):
          result={}
          signature_counter=0

          signature_record={}
          signature_record["SigId"]=-1 # When ther is no saved signature
          signature_record["SigContent"]="No Existing Signature. You can define one."
          result["Sign00"]=signature_record

          try:
          
               engine=db

               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               res_signature= session.query(MessageSignature).all()

               for one_signature in res_signature:
                    if signature_counter<10:
                         key="Sign0"
                    else:
                         key="Sign"
                    signature_record={}
                    signature_record["SigId"]=one_signature.id
                    signature_record["SigContent"]=one_signature.signature_content   
                    result[key+"%d"%signature_counter]=signature_record
                    signature_counter=signature_counter+1
                   

               
               session.close()
               engine.dispose()
               dbconn.close()
               return(json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))      


          except Exception as e:
               result["message"]="Error: %s."%e
               return (json.JSONEncoder().encode(result)) 
               session.close()
               engine.dispose()
               dbconn.close()



     
          
         

#myjson={"CategoryId":-1,"CategoryName":"Seasonal Greetings"}
#myjson={}    
#myjson={"SigId":4,"SigContent":"..Director, Lucatec Automation", "SigStatus":0,"Action":"Update"}     

#obj=ManageMessageTemplates(myjson)
#msg=obj.getAllSignatures()
#print msg
#msg=obj.configureSMSSignature()
#msg=obj.saveSMSTemplateInDB()
#msg=obj.saveTemplateCategoryInDB()

#msg=obj.retrieveSMSTemplates()
#msg=obj.retrieveTemplateCategories()
#print msg
