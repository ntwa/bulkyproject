from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String,Float,Boolean,Enum,Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr
from sqlalchemy.pool import NullPool
import address_book_module
import enum
#db = create_engine(connstr,pool_size=20, max_overflow=0)


try:
     db 
except NameError as e:
     db = create_engine(connstr,poolclass=NullPool)


try:
     dbconn
except NameError as e:

     dbconn=db.connect()


try:
     Base
except NameError as e:
     Base = declarative_base()





#campaign definition
class Campaign(Base):
    __tablename__="campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_descr=Column(String(500))
    campaign_category=Column(Enum('Reminders','Individual Best Wishes','Holiday Greetings','Holiday Adverts','General Marketing'))
    target_level=Column(Enum('Individual','Group'))
    frequency_in_days=Column(Enum('Daily','Weekdays','Weekends','Selective Days'))
    is_it_life_time=Column(Boolean) # Some Campaign may be set to run year after year over a lifetime i.e birthdays.
    is_annual_delivery_date_constant=Column(Boolean) # Some campaigns may  be holidays that have fixed date, some may not be fixed, meaning they have to be updated anually to reflect the current year if it is a lifetime campaign.
    campaign_messages = relationship("CampaignDefinedMessages", backref=backref("campaign", order_by=id))
  
    def __init__(self,campaign_name,campaign_descr,campaign_category,target_level,frequency_in_days,is_it_life_time,is_annual_delivery_date_constant):
         self.campaign_name=campaign_name
         self.campaign_descr=campaign_descr
         self.campaign_category=campaign_category
         self.target_level=target_level
         self.frequency_in_days=frequency_in_days
         self.is_it_life_time=is_it_life_time
         self.is_annual_delivery_date_constant=is_annual_delivery_date_constant

#Define a message bank that will be picked randomly
class CampaignDefinedMessages(Base):
    __tablename__="campaigns_defined_messages"
    id=Column("campaign_message_id",Integer,primary_key=True)
    campaign_id=Column(Integer, ForeignKey("campaigns.campaign_id"))
    message_txt=Column(String(500))

    
    def __init__(self,message_txt):
         self.message_txt=message_txt


class Feedback(Base):
    __tablename__="feedback"
    id=Column(Integer, primary_key=True)
    recipient_mobile=Column(String(20))
    message=Column(String(1000))
    status=Column(Boolean)
    is_group_sms=Column(Boolean)
    group_id=Column(Integer)
    
    
    def __init__(self,recipient_mobile,message):
        self.recipient_mobile=recipient_mobile
        self.message=message
        self.status=0
    @abstractmethod    
    def storeFeddback(self):
        pass
    @abstractmethod
    def viewFeedback(self):
        pass
    def __repr__(self):
        return str(self.id)
    def getID(self):
        return self.id

class ScheduledMessageDefinition:
    __tablename__="scheduled_messages_definitions"
    id=Column("scheduled_msg_id",Integer, primary_key=True)
    campaign_id=Column(Integer, ForeignKey("campaigns.campaign_id"))
    campaign_start_date=Column(Date) #If it is a lifetime Campaign the start date is when the message was scheduled 
    campaign_end_date=Column(Date)   #This is a lifetime Campaign the start date is when the message was scheduled 
    
    
    
    def __init__(self,campaign_start_date,campaign_end_date):
        self.campaign_start_date=campaign_start_date
        self.campaign_end_date=campaign_end_date

class SelectedDeliveryDay:
    __tablename__="individuals_selected_days"
    id=Column("selected_day_id",Integer, primary_key=True)
    campaign_id=Column(Integer, ForeignKey("individuals_target_subscribers.subscribe_id"))
    selected_day=Column(String(20)) #Selected Days of a week

    def __init__(self,selected_day):
        self.selected_day=selected_day
        
class MessageSendingTimeSchedule:
    __tablename__="messages_sending_time_schedules"
    id=Column("snd_schedule_id",Integer, primary_key=True)
    scheduled_msg_id=Column(Integer, ForeignKey("scheduled_messages_definitions.scheduled_msg_id"))
    sending_time=Column(Time)
    queued_status=Column(Boolean) #Is the message already queued for sending. Messages are queued at midnight ready to be sent in the next business day.

    def __init__(self,sending_time,queued_status):
        self.sending_time=sending_time
        self.queued_status=queued_status
     

class GroupTargetSubscriber:
    __tablename__="groups_target_subscribers"
    id=Column("subscribe_id",Integer, primary_key=True)
    group_id=Column(Integer, ForeignKey("groups.group_id"))
    scheduled_msg_id=Column(Integer, ForeignKey("scheduled_messages_definitions.scheduled_msg_id"))

    def __init__(self):
        pass


class IndividualTargetSubscriber:
    __tablename__="individuals_target_subscribers"
    id=Column("subscribe_id",Integer, primary_key=True)
    contact_id=Column(Integer, ForeignKey("address_book.contact_id"))
    scheduled_msg_id=Column(Integer, ForeignKey("scheduled_messages_definitions.scheduled_msg_id"))

    def __init__(self):
        pass



Base.metadata.create_all(db)
