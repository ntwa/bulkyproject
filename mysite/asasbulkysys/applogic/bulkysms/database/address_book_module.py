from abc import ABCMeta, abstractmethod
#from sqlalchemy import *
#from sqlalchemy import create_engine, ForeignKey, ForeignKeyConstraint
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy import Column, Date, DateTime, Integer, String, Boolean
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
#from dbconnect import connstr
#from sqlalchemy.pool import NullPool
#import json,sys
#from collections import OrderedDict
#from dbinit import db,dbconn
from base import Base

#import sms_feedback_module

#db = create_engine(connstr,pool_size=20, max_overflow=0)
#db = create_engine(connstr,poolclass=NullPool)
#dbconn=db.connect()
'''
try:
     db 
except NameError as e:
     db = create_engine(connstr,poolclass=NullPool)


try:
     dbconn
except NameError as e:

     dbconn=db.connect()

'''
#try:
#     Base
#except NameError as e:
#     Base = declarative_base()


class AuthUser(Base):
     __tablename__="auth_user"
     id=Column("id",Integer,primary_key=True)
     password=Column(String(128),nullable=False)
     last_login=Column(DateTime,nullable=False)
     is_super_user=Column(Boolean,nullable=False)
     username=Column(String(30),nullable=False)
     first_name=Column(String(30),nullable=False)
     last_name=Column(String(30),nullable=False)
     email=Column(String(75),nullable=False)
     is_staff=Column(Boolean,nullable=False)
     is_active=Column(Boolean,nullable=False)
     date_joined=Column(DateTime,nullable=False)
     auth_company_users = relationship("CompanyUsers", backref=backref("auth_company_users", order_by=id))



class Company(Base):
     __tablename__="companies"
     id=Column("company_id",Integer,primary_key=True)
     company_name=Column(String(100),nullable=False)
     business_descr=Column(String(500),nullable=True)
     postal_address=Column(String(100),nullable=True)
     region=Column(String(50),nullable=True)
     district=Column(String(50),nullable=True)
     ward=Column(String(50),nullable=True)
     street=Column(String(50),nullable=True)
     mobile_number=Column(String(50),nullable=False)
     email_address=Column(String(50),nullable=True)
     mobile_verified=Column(Boolean,nullable=False)
     #user_id= Column(Integer, ForeignKey("auth_user.id"),primary_key=True) # A user cannot exist in more than one company
     company_address_book = relationship("AddressBook", backref=backref("company_address_book", order_by=id))
     company_users = relationship("CompanyUsers", backref=backref("company_users", order_by=id))

     def __init__(self,company_name,business_descr,postal_address,street,ward,district,region,mobile_number,email_address): 
          self.company_name=company_name
          self.business_descr=business_descr
          self.postal_address=postal_address
          self.street=street
          self.ward=ward
          self.district=district
          self.region=region
          self.mobile_number=mobile_number
          self.email_address=email_address
          self.mobile_verified=0


    #company_message_groups = relationship("Group", backref=backref("company_message_groups", order_by=id))

class CompanyUsers(Base):     
     __tablename__="company_users"
     company_id=Column(Integer, ForeignKey("companies.company_id")) # a company can have many users.
     user_id= Column(Integer, ForeignKey("auth_user.id"),primary_key=True) # A user cannot exist in more that one company

    
     def __init__(self,company_id,user_id):
          self.company_id=company_id
          self.user_id=user_id
'''
class EntityPermissions(Base):
	 __tablename__="user_permissions"
     user_id= Column(Integer, ForeignKey("auth_user.id"),primary_key=True) # A user cannot exist in more that one company
     permissible_entity=Column(Enum('Campaigns','Groups','AddressBook',"Users"),nullable=False)
     permission_type=Column(Enum('RD','RDWRT','RDWRTDLT'),nullable=False) # Read Only, Read Write, Read Write Delete.

 '''   
      
class AddressBook(Base):

     __tablename__="address_book"
     id=Column("contact_id",Integer, primary_key=True)
  
     first_name=Column(String(50))
     middle_name=Column(String(50))
     last_name=Column(String(50))
     gender=Column(String(4))
     birth_date = Column(Date)
     country=Column(String(50))
     region=Column(String(50))
     district=Column(String(50))
     ward=Column(String(50))
     company_id= Column(Integer, ForeignKey("companies.company_id"))

     mobile_number = relationship("MobileDetails", backref=backref("address_book_mobile", order_by=id))
     email_address = relationship("EmailDetails", backref=backref("address_book_emails", order_by=id))
     group_member_contact = relationship("GroupMember", backref=backref("group_member_contact", order_by=id))
     individual_campaign  = relationship("IndividualizedReminder", backref="AddressBook.id")

     def __init__(self,first_name,middle_name,last_name,gender,birth_date,ward,district,region,country):
          self.first_name=first_name
          self.middle_name=middle_name
      	  self.last_name=last_name
      	  self.gender=gender
      	  self.birth_date = birth_date
      	  self.country= country
      	  self.region= region
      	  self.district=district
      	  self.ward=ward

    #@abstractmethod    
     def editAddressDetails(self,first_name,middle_name,last_name,gender,birth_date,ward,district,region,country):
          self.first_name=first_name
          self.middle_name=middle_name
      	  self.last_name=last_name
      	  self.gender=gender
      	  self.birth_date = birth_date
      	  self.country= country
      	  self.region= region
      	  self.district=district
      	  self.ward=ward

    #@abstractmethod
     def viewAddressDetails(self):
          address_tuple={}
          address_tuple["first_name"]=self.first_name
          address_tuple["middle_name"]=self.middle_name
  	  address_tuple["last_name"]=self.last_name
  	  address_tuple["gender"]=self.gender
  	  address_tuple["birth_date"]=self.birth_date
          address_tuple["ward"]=self.ward
          address_tuple["district"]=self.district
          address_tuple["region"]=self.region
  	  address_tuple["country"]=self.country
  	  return(json.JSONEncoder().encode(address_tuple)) 


class MobileDetails(Base):     
     __tablename__="mobile_details"
     id=Column("mobile_id",Integer, primary_key=True)
     mobile_number=Column(String(15))
     is_it_primary_number=Column(Boolean,nullable=False)
     contact_id= Column(Integer, ForeignKey("address_book.contact_id"))
    
     def __init__(self,mobile_number,is_it_primary_number):
          self.mobile_number=mobile_number
          self.is_it_primary_number=is_it_primary_number

     def editMobileDetails(self,mobile_number,is_it_primary_number):
          self.mobile_number=mobile_number
          self.is_it_primary_number=is_it_primary_number

   
     def viewMobileDetails(self):
  	  mobile_tuple={}
          mobile_tuple["mobile_number"]=self.mobile_number
  	  mobile_tuple["is_it_primary_number"]=self.is_it_primary_number
  	  mobile_tuple["contact_id"]=self.contact_id
  	  return(json.JSONEncoder().encode(mobile_tuple)) 
  
class EmailDetails(Base):     
     __tablename__="email_details"
     id=Column("email_id",Integer, primary_key=True)
     email_address=Column(String(50))
     is_it_primary_email=Column(Boolean,nullable=False)
     contact_id= Column(Integer, ForeignKey("address_book.contact_id"))
    
     def __init__(self,email_address,is_it_primary_email):
          self.email_address=email_address
          self.is_it_primary_email=is_it_primary_email

     def editEmailDetails(self,email_address,is_it_primary_email):
          self.email_address=email_address
          self.is_it_primary_email=is_it_primary_email

   
     def viewEmailDetails(self):
  	  email_tuple={}
          email_tuple["email_address"]=self.email_address
  	  email_tuple["is_it_primary_email"]=self.is_it_primary_email
  	  email_tuple["contact_id"]=self.contact_id
  	  return(json.JSONEncoder().encode(email_tuple))

class Group(Base):

     __tablename__="groups"
     id=Column("group_id",Integer, primary_key=True)
  
     group_name=Column(String(50))
     group_description=Column(String(200))
     #company_id= Column(Integer, ForeignKey("company.company_id")) #Links the groups created by a certain company
 

     group_member = relationship("GroupMember", backref=backref("group", order_by=id))
     sms_campaign_audience = relationship("CampaignAudienceSMS", backref=backref("groupcampaign", order_by=id))
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
     group_id=Column(Integer, ForeignKey("groups.group_id"),primary_key=True)
     contact_id= Column(Integer, ForeignKey("address_book.contact_id"),primary_key=True)

    
     def __init__(self,contact_id,group_id):
          self.contact_id=contact_id
          self.group_id=group_id
          

#Base.metadata.create_all(db)
