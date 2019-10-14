#!/usr/bin/env python
import datetime
import sys,json
#from sqlalchemy import create_engine,distinct,func
from sqlalchemy import distinct,func
from sqlalchemy.orm import sessionmaker
#from bulkysms.database.address_book_module import AddressBook, Group, GroupMember,db,dbconn

#from sqlalchemy import ForeignKey, ForeignKeyConstraint
#from sqlalchemy import Column, Date, Integer, String, Boolean, Enum, Time, Float
#from sqlalchemy.orm import relationship, backref,sessionmaker
#from sqlalchemy.pool import NullPool
#from sqlalchemy.ext.declarative import declarative_base


from collections import OrderedDict
from bulkysms.database.base  import Base
from bulkysms.database.dbinit import db,dbconn
import bulkysms.database.address_book_module

Base.metadata.create_all(db)

from bulkysms.database.address_book_module import AddressBook, Group, GroupMember
from bulkysms.database.sms_feedback_module import Campaign

class switch(object):
          value = None
          def __new__(class_, value):
                    class_.value = value
                    return True
def case(*args):
          return any((arg == switch.value for arg in args))

class GroupsManager:
     def __init__(self,myjson):
          self.myjson=myjson

   
 
     def addGroupMember(self):
          result={}
        
          try:
               contact_id=self.myjson["ContactID"]
               group_id=self.myjson["GroupID"]
               company_id=self.myjson["CompanyID"]

          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]="Error: '%s'. If the error persists contact the developer"%e
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          try:
               
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               #Get person's name
               res2ab=session.query(AddressBook).filter(AddressBook.id==contact_id).filter(AddressBook.company_id==company_id).first()
               person_name="%s %s"%(res2ab.first_name,res2ab.last_name)
               if res2ab is None:
                    result["message"]="Error: The Person you are trying to assign to a group doesn't exist"
                    return (json.JSONEncoder().encode(result)) 
                  



               #get group was trying to be assigned to. This will also prevent users to edit groups that don't belong to their company
               res2g=session.query(Group).filter(Group.id==group_id).filter(Group.company_id==company_id).first()
               group_name="%s"%(res2g.group_name)

               if res2g is None:
                    result["message"]="Error: You are trying to assign '%s' to a group that doesn't exist"%person_name
                    return (json.JSONEncoder().encode(result))
               
                                  
               # querying for if a person has been assigned to this group before.
               res= session.query(GroupMember).filter(GroupMember.contact_id==contact_id).filter(GroupMember.group_id==group_id).first()
               if res is None:
                    #
                    new_member=GroupMember(contact_id,group_id)
                    session.add(new_member)
                    session.commit()
                    result["message"]="'%s' has been assigned to '%s' group successfully."%(person_name,group_name)
               else:

                    result["message"]="Error:'%s' is arleady a member to '%s' group hence can't be assigned again"%(person_name,group_name) 
                     
          except Exception as e:
               #print "Content-type: text/html\n" 
               session.close()
               engine.dispose()
                    
               dbconn.close()
               result["message"]="Error: '%s'. If the error persists contact the developer"%e
               return (json.JSONEncoder().encode(result)) 
               #sys.exit(
       
          session.close()
          engine.dispose()
                    
          dbconn.close()
	  return (json.JSONEncoder().encode(result))




     def removeGroupMember(self):
          result={}
        
          try:
               contact_id=self.myjson["ContactID"]
               group_id=self.myjson["GroupID"]
               company_id=self.myjson["CompanyID"]

          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]="Error: '%s'. If the error persists contact the developer"%e
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          try:
               
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               #Get person's name
               res2ab=session.query(AddressBook).filter(AddressBook.id==contact_id).filter(AddressBook.company_id==company_id).first()
               person_name="%s %s"%(res2ab.first_name,res2ab.last_name)
               if res2ab is None:
                    result["message"]="Error: The Person you are trying to remove from a group doesn't exist"
                    return (json.JSONEncoder().encode(result)) 
                  



               #get group was trying to be assigned to. This will also prevent a user to remove someone from a group that doesn't belong to their company
               res2g=session.query(Group).filter(Group.id==group_id).filter(Group.company_id==company_id).first()
               group_name="%s"%(res2g.group_name)

               if res2g is None:
                    result["message"]="Error: You are trying to assign '%s' to a group that doesn't exist"%person_name
                    return (json.JSONEncoder().encode(result))
               
                                  
               # querying for if a person has been assigned to this group before.
               res= session.query(GroupMember).filter(GroupMember.contact_id==contact_id).filter(GroupMember.group_id==group_id).first()
               if res is None:
                    #
                    result["message"]="Error:'%s' is not a member to '%s' group"%(person_name,group_name) 
                    
               else:
                    session.delete(res) 
                    session.commit()
                    result["message"]="'%s' has been removed from '%s' group successfully."%(person_name,group_name)
                     
          except Exception as e:
               #print "Content-type: text/html\n" 
               session.close()
               engine.dispose()
                    
               dbconn.close()
               result["message"]="Error: '%s'. If the error persists contact the developer"%e
               return (json.JSONEncoder().encode(result)) 
               #sys.exit(
       
          session.close()
          engine.dispose()
                    
          dbconn.close()
          return (json.JSONEncoder().encode(result))



     def retrieveGroupDetailsFromDB(self):
           
          #The tuples are used for definition of JSON objects
          group_tuple={}
    

          #important in keeping track of number of groups
          level_one_json_counter=0
         
          key1="AD" #part of forming a key to json object for the group
   
           
	 
	  #get all groups and their respective details 
          try:
               company_id=self.myjson["CompanyID"]
               
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               result={}                    
               # querying for existence of groups for this company. It is possible for the same name to be used by different companies. So have to filter only for one company
               res= session.query(Group).order_by(Group.group_name).filter(Group.company_id==company_id).all()
               
               if len(res) ==0:
                    session.close()
                    engine.dispose()
                    dbconn.close()
                    result["AD00"]=-1
                    result["Message"]="No groups present."
                    return (json.JSONEncoder().encode(result))
	       else: 
                    for group_rec in res:	  
                         #Now  put both mobile tuple and email tuple to the main address tuple
                         if level_one_json_counter<10:
                              key1="AD0"# append a zero. This is important in ordering keys alphabetically
                         else:
                              key1="AD"


                         members_count_res=session.query(func.count(distinct(GroupMember.contact_id))).filter(GroupMember.group_id==group_rec.id).first()
                         retrieved_members_counter=0# initialize how many distinct dates are in the database
                         for retrieved_members_counter in members_count_res:
                              break
                         
                        

                         group_tuple[key1+"%d"%level_one_json_counter]={"GroupID":group_rec.id, "GroupName":group_rec.group_name, "group_description":group_rec.group_description,"NumMembers":retrieved_members_counter}
                         level_one_json_counter=level_one_json_counter+1 # After getting the first record add 1 to the counter	

                         
         
                         
                    session.close()  
                    engine.dispose()   
                    dbconn.close()
                    #we wind up the retrieve operation.  
                    #return json.JSONEncoder().encode(address_tuple) 
                    return(json.JSONEncoder().encode(OrderedDict(sorted(group_tuple.items(), key=lambda t: t[0]))))   
                                   
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
     


       
     def saveGroupInDB(self):
          #group_name="" 
          #group_descr="" 
         
       
       
          result={}
          allow_insert=1
          
          # Get data from fields
          try:
               group_id=self.myjson["GroupID"]            
               group_name=self.myjson["GroupName"] 
               group_descr=self.myjson["GroupDescr"] 
               company_id=self.myjson["CompanyID"]
               
               
               #group_name="Farmers Kilolo"
               #group_descr="This group is important for communicating important information to Farmers in Kilolo" 
                        
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]="Error: '%s' encountered in editing the 'Groups'. If the error persists contact the developer:%s"%(e,group_descr)
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          

          if(group_name==None) and (group_descr==None) :
               #print "Content-type: text/html\n" 
               result["message"]="Error: You did not enter any group details"
               return (json.JSONEncoder().encode(result)) 
               #sys.exit()


          #check if a record exists
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()

               #check if the name exists.
                                   
               # querying for a record if it exists already for this company.
               res= session.query(Group).filter(Group.id==group_id).filter(Group.company_id==company_id).first()
               
               if res is None:
                    session.close()
                    engine.dispose()
                    dbconn.close()
               else:
                    #if it exists, then update the record in the database.
                    group_record=res
                    group_record.group_name=group_name
                    group_record.group_description=group_descr
				    
                    group_id=res.id
                    

                                                
                    session.commit() #Now commit this session                         
                    allow_insert=0 #Reset allow to zero so that the code doesn't attempt to insert a new record
                    #size=size-1 #ignore the last value because it has arleady been updated
                    
                    result["message"]="The record for group '%s' already existed hence  has been updated"%(group_name)
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
                                   
               result["message"]="Error: %s."%e
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
               
          
          if allow_insert==1: 
               #If we get here it means the record doesn't exist hence we need to create it for the first time.          
               try:
                    
                
                    new_group=Group(group_name,group_descr,company_id)           
                                                            
                    session.add(new_group)
                    
                    # commit the record the database
                                      
                    session.commit()
		    session.close()
                    engine.dispose()
                    dbconn.close()
                    message="The new group called '%s' was created sucessfully"%group_name
                     
                    result["message"]=message
                    return (json.JSONEncoder().encode(result))                 
                     
                    
               except Exception as e:
                    session.close()
                    engine.dispose()
                    
                    dbconn.close()
                    result["message"]="Error:%s"%e.message
                    return (json.JSONEncoder().encode(result)) 
            

               #result["R00"]={"F1":1,"F0":"The contact was recorded sucessfully"}
               #return (json.JSONEncoder().encode(result))
     
     
#myjson={"GroupID":12,"GroupName":"Customers in Kinondoni B","GroupDescr":"This group is for customers in Kinondoni areas."}
#myjson={"CompanyID":1}
#myjson={"GroupID":11,"Option":-1}
#obj=GroupsManager(myjson)
#msg=obj.retrieveGroupDetailsFromDB()
#msg=obj.addGroupMember()
#msg=obj.saveGroupInDB()
#print msg
