from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey, ForeignKeyConstraint
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr
from sqlalchemy.pool import NullPool
import json,sys
from collections import OrderedDict
from address_book_module import AddressBook

#db = create_engine(connstr,pool_size=20, max_overflow=0)
db = create_engine(connstr,poolclass=NullPool)
dbconn=db.connect()

Base = declarative_base()

       
class Group(Base):

    __tablename__="groups"
    id=Column("group_id",Integer, primary_key=True)
  
    group_name=Column(String(50))
    group_description=Column(String(200))
 

    group_member = relationship("GroupMember", backref=backref("group", order_by=id))
    #email_address = relationship("EmailDetails", backref=backref("address_book_emails", order_by=id))
    def __init__(self,group_name,group_description):
	self.group_name=group_name
    	self.group_description=group_description


    #@abstractmethod    
    def editGroupDetails(self,group_name,group_description):
	self.group_name=group_name
    	self.group_description=group_description

    #@abstractmethod
    def viewGroupDetails(self):
	 group_tuple={}
         group_tuple["group_name"]=self.group_name
	 group_tuple["group_description"]=self.group_description
	 return(json.JSONEncoder().encode(group_tuple)) 


class GroupMember(Base):     
    __tablename__="group_members"
    id=Column("membership_id",Integer)
    group_id=Column(Integer, ForeignKey("address_book.contact_id"),primary_key=True)
    contact_id= Column(Integer, ForeignKey("address_book.contact_id"),primary_key=True)
    
    def __init__(self):
        pass




Base.metadata.create_all(db)
