from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey, ForeignKeyConstraint
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr
from sqlalchemy.pool import NullPool
import json,sys
from collections import OrderedDict
import address_book_module

#db = create_engine(connstr,pool_size=20, max_overflow=0)
if db is None and dbconn is None:
    db = create_engine(connstr,poolclass=NullPool)
    dbconn=db.connect()

if Base is None:
    Base = declarative_base()
#Base = declarative_base()

#general campaign definition
class Campaign(Base):
    __tablename__="campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day

    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id

#Campaigns that run indefinately 
class LifeTimeCampaign(Base):
    __tablename__="lifetime_campaigns"
    id=Column("lifer_time_campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually

    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id

#Campaigns that run indefinatelly but once every year
class OnceLifeTimeCampaign(Base):
    __tablename__="lifetime_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually

    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id

#Campaigns that run indefinatelly but once every year at a fixed date i.e Birthdays, X
class FixedOnceLifeTimeCampaign(Base):
    __tablename__="lifetime_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually

    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id

#Campaigns that run indefinatelly but once every year at a flexible date i.e Greeting for holidays such as Eid,and Easter (They don't have a fixed date, as it can change from a year to a year)
class FlexibleOnceLifeTimeCampaign(Base):
    __tablename__="lifetime_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually



  
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id

#FixedOnceLifeTimeCampaign for Groups. For instance, greetings during xmass, new year, Mapinduzi day, Uhuru Day etc,
class GroupFixedOnceLifeTimeCampaign(Base):
    __tablename__="lifetime_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually



  
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id

#FixedOnceLifeTimeCampaign for individuals. For instance a birthday applies to individuals
class IndividualFixedOnceLifeTimeCampaign(Base):
    __tablename__="lifetime_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually



  
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id

#FlexibleOnceLifeTimeCampaign that applies to a group. For instance seasonal greetings for eid, easter etc
class GroupFlexibleOnceLifeTimeCampaign(Base):
    __tablename__="lifetime_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually



  
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id

#FlexibleOnceLifeTimeCampaign for individuals. For instance to notify cars care takers i.e drivers that their car's insurances have already expired
class IndividualFlexibleOnceLifeTimeCampaign(Base):
    __tablename__="lifetime_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually



  
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id





#These Campaigns are lifetime and run several times during the year. For instance if one wants to remind the customers about unpaid debts  
class PeriodicLifeTimeCampaign(Base):
    __tablename__="lifetime_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually

    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id
#PeriodicLifeTimeCampaign that have fixed dates. For instance every year they run on same dates. This can be used for offers that a tied to season such as christmass, new year, Valentine day etc.
class FixedPeriodicLifeTimeCampaign(Base):
    __tablename__="lifetime_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually


    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id

#FixedPeriodicLifeTimeCampaign for campaigns applied at individual level. At the moment there is no use case for this class. But it can be useful in the future
class IndividualFixedPeriodicLifeTimeCampaign(Base):
    __tablename__="lifetime_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually

    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id


#FixedPeriodicLifeTimeCampaign for the group. This can be used for offers that a tied to season such as xmass, saba saba etc
class GroupFixedPeriodicLifeTimeCampaign(Base):
    __tablename__="lifetime_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually

    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id


#PeriodicLifeTimeCampaign that have flexible dates every year. This can be used for offers that a tied to season such as eid, easter,etc.
class FlexiblePeriodicLifeTimeCampaign(Base):
    __tablename__="lifetime_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually

    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id


#FlexiblePeriodicLifeTimeCampaign for groups. This can be used for offers that a tied to seasons such as eid, easter,etc. May bey few day before and after the event of interest
class GroupFlexiblePeriodicLifeTimeCampaign(Base):
    __tablename__="lifetime_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually

    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id


#PeriodicLifeTimeCampaign for individuals. No practical use case for now
class IndividualFlexiblePeriodicLifeTimeCampaign(Base):
    __tablename__="lifetime_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually

    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id


#Campaigns that last for a certain period of time usually non consecutive time until the campaign finishes and it never comes back
class ShortCampaign(Base):
    __tablename__="short_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually

    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id

class ShortGroupCampaign(Base):
    __tablename__="short_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually

    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id


class ShortIndividualCampaign(Base):
    __tablename__="short_campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    event_type=Column(String(200))#Reminder #celebration #marketing #seasonal greetings #special offers #others
    number_of_times_runs_per_day=Column(SmallInteger) # How many times the campaign will run during the day
    is_it_annual_repeatable=Column(Boolean) #The campaign will repeat every year. # For instance birthday
    is_date_fixed=Column(Boolean) #For instance Islamic holidays don't have fixed dates hence dates will be updated annually

    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id







class CampaignIndividualsSubscribed(Base):
    __tablename__="campaign_individuals_subscribed"
    id=Column("subscriber_id",Integer,primary_key=True)
    date_to_be_triggered=Column(Date)
    date_to_be_switched_off=Column(Date)
    campaign_id=Column(Integer, ForeignKey("defined_campaigns.campaign_id"))
    contact_id=Column(Integer, ForeignKey("address_book.contact_id"))

    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id


class CampaignGroupsSubscribed(Base):
    __tablename__="campaign_groups_subscribed"
    id=Column("subscriber_id",Integer,primary_key=True)
    date_to_be_triggered=Column(Date)
    date_to_be_switched_off=Column(Date)  
    campaign_id=Column(Integer, ForeignKey("defined_campaigns.campaign_id"))
    group_id=Column(Integer, ForeignKey("address_book.contact_id"))
    
    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id


#Base.metadata.create_all(db)
