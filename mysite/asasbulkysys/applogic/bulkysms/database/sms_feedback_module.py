from abc import ABCMeta, abstractmethod

#from sqlalchemy import ForeignKey

#from sqlalchemy import Column, Date, Integer, String,Float,Boolean,Enum,Time

#from sqlalchemy.orm import relationship, backref,relation

#from base import Base

import datetime


from sqlalchemy import *
from base  import Base
from sqlalchemy.orm import relationship,backref


#Beneficiaries of this system: Hospitals, Schools, SMEs, Government Agents such as TRA to remind people to pay their property tax on time or to pay all overdued taxes, or even to file tax/VAT returns

#This class stores all outgoint messages (status:sent 0 and waiting to be sent: 1 )
class Feedback(Base):
     __tablename__="feedback"
     id=Column(Integer, primary_key=True)
     company_id=Column(Integer, ForeignKey("companies.company_id")) # We can only have access to messages in our company
     recipient_mobile=Column(String(20))
     message=Column(String(1000))
     recipient_contact_id=Column(String(20))
     recipient_name=Column(String(200))
     recipient_group_id=Column(Integer,nullable=True)#This is for messages that were targeted to a group
     recipient_campaign_id=Column(Integer,nullable=True)#This is for specifying if a message was for a particular campaign
     scheduled_time=Column(Time,nullable=True) #The time in which the message was supposed to be sent out.
     scheduled_date=Column(Date,nullable=True) #The date in which the message was supposed to be sent out
     delivery_note=Column(String(100),nullable=True) #Delivery note returned by SMS gateway
     #date_modified=Column(Date)
     #time_modified=Column(Time)
     status=Column(Boolean) #if the value is 1 then a message has been tried to  be sent out. 
    #is_group_sms=Column(Boolean)
    #group_id=Column(Integer)
    
    
     def __init__(self,recipient_mobile,recipient_contact_id,recipient_name,message,recipient_group_id,recipient_campaign_id,scheduled_time,scheduled_date):
          self.recipient_mobile=recipient_mobile
          self.recipient_contact_id=recipient_contact_id
          self.recipient_name=recipient_name
          self.message=message
          self.recipient_group_id=recipient_group_id
          self.recipient_campaign_id=recipient_campaign_id
          self.scheduled_time=scheduled_time
          self.scheduled_date=scheduled_date
          self.delivery_note=""
          self.status=0
     @abstractmethod    
     def storeFeedback(self):
          pass
     @abstractmethod
     def viewFeedback(self):
          pass
     def __repr__(self):
          return str(self.id)
     def getID(self):
          return self.id



#campaign definition
class Campaign(Base):
     __tablename__="campaigns"
     id=Column("campaign_id",Integer,primary_key=True)
     campaign_name=Column(String(200),nullable=False)
     campaign_descr=Column(String(500))
     delivery_mechanism=Column(Enum('SMS','Whatsapp','Email'),nullable=False)
     campaign_category=Column(Enum('IR','GR','BW','HG','HO','GM'),nullable=False)
     target_level=Column(Enum('Specific Groups','All'),nullable=False)
     date_created=Column(Date,nullable=False)
     is_campaign_active=Column(Boolean) #is the campaign currently running.A campaign will be active if it has not been stopped manually or its deadline has not yet passed
     company_id=Column(Integer, ForeignKey("companies.company_id")) # a company that owns his campaign.

     campaign_messages = relationship("CampaignDefinedMessages", backref=backref("campaign_messages", order_by=id))
     starting_day = relationship("CampaignStartDay", backref=backref("campaign_end_day", order_by=id))
     stopping_day = relationship("CampaignEndDay", backref=backref("campaign_end_day", order_by=id))
     selected_delivery_days= relationship("SelectedDeliveryDayofWeek", backref=backref("delivery_day", order_by=id))
     selected_delivery_time= relationship("SelectedDeliveryTime", backref=backref("delivery_time", order_by=id))

     sms_campaign_audience = relationship("CampaignAudienceSMS", backref=backref("campaignaudience", order_by=id))
     individual_campaign =relationship("IndividualizedReminder", backref=backref("individualized_reminders", order_by=id))
     
     def __init__(self,campaign_name,campaign_descr,delivery_mechanism,campaign_category,target_level,company_id):
          self.campaign_name=campaign_name
          self.campaign_descr=campaign_descr
          self.delivery_mechanism=delivery_mechanism
          self.campaign_category=campaign_category
          self.target_level=target_level
          self.is_campaign_active=True
          self.date_created=datetime.date.today() 
          self.company_id=company_id
     #if a campaign is not in this table it means it has been set to run indefinately
 

#Individualized Reminders and BirthDays are triggered by special dates, these don't have start day 
class CampaignStartDay(Base):
     __tablename__="campaign_start_day"
     campaign_id=Column(Integer, ForeignKey("campaigns.campaign_id"),primary_key=True) # A campaign must have atmost one start date
     campaign_start_date=Column(Date,nullable=False) #The Date when the campaign becomes active
     
     def __init__(self,campaign_start_date):
          self.campaign_start_date=campaign_start_date

        
         
#indefinately Campaign Don't have end day, Individualized Reminders and BirthDay also don't have end day as they are triggered by special dates. For instance 
class CampaignEndDay(Base):
     __tablename__="campaign_end_day"
     campaign_id=Column(Integer, ForeignKey("campaigns.campaign_id"),primary_key=True) # A campaign must have atmost one end date
     campaign_end_date=Column(Date,nullable=False)

     def __init__(self,campaign_end_date):
          self.campaign_end_date=campaign_end_date
         
     

#Define a message bank that will be picked randomly
class CampaignDefinedMessages(Base):
     __tablename__="campaigns_defined_messages"
     id=Column("campaign_message_id",Integer,primary_key=True)
     campaign_id=Column(Integer, ForeignKey("campaigns.campaign_id"))
     message_txt=Column(String(500),nullable=False)

    
     def __init__(self,message_txt):
          self.message_txt=message_txt


class SelectedDeliveryDayofWeek(Base):
     __tablename__="selected_days_of_delivery"
     id=Column("selected_day_id",Integer, primary_key=True)
     campaign_id=Column(Integer, ForeignKey("campaigns.campaign_id"))
     selected_day=Column(Integer,nullable=False) #Selected Days of a week

     def __init__(self,selected_day):
          self.selected_day=selected_day

class SelectedDeliveryTime(Base):
     __tablename__="selected_time_of_delivery"
     #id=Column("selected_day_id",Integer, primary_key=True)
     #PRimary key to ensure a campaign can't pick the same time twice
     campaign_id=Column(Integer, ForeignKey("campaigns.campaign_id"),primary_key=True)
     selected_time=Column(Time,primary_key=True) #Selected Days of a week

     def __init__(self,selected_time):
          self.selected_time=selected_time


'''

#The records are generated after looking at active campaigns that have messages that qualify to be sent the next day. We look at what day will it be         
class MessageSendingSchedule:
     __tablename__="messages_sending_time_schedules"
     id=Column("snd_schedule_id",Integer, primary_key=True)
     campaign_id=Column(Integer, ForeignKey("campaigns.campaign_id"))

     sending_time=Column(Time) # Based on selected Delivery time
     not_queued_for_send=Column(Boolean) #Is the message already scheduled for sending to all recipients. Messages are scheduled at midnight ready to be sent in the next business day. Any scheduled message is put under feedback when it the time for sending it. Once put on feedback then not_queued_for_send is set to 0. In this way we can track which messages are awaiting to be put into feedback before sending are which ones have already been scheduled for sending

     def __init__(self,sending_time,not_ready_for_send):
          self.sending_time=sending_time
          self.not_queued_for_send=not_queued_for_send
     

'''
#Audience
class CampaignAudienceSMS(Base):
     __tablename__="sms_campaign_targeted_groups"
     group_id=Column(Integer, ForeignKey("groups.group_id"),primary_key=True)
     campaign_id= Column(Integer, ForeignKey("campaigns.campaign_id"),primary_key=True)
     def __init__(self,group_id):
          self.group_id=group_id
'''
class CampaignAudienceWhatsapp(Base):
     __tablename__="campaign_targeted_groups"
     id=Column("campaign_audience_id",Integer)
     group_id=Column(Integer, ForeignKey("groups.group_id"),primary_key=True)
     campaign_id= Column(Integer, ForeignKey("campaigns.campaign_id"),primary_key=True)
     def __init__(self):
          pass
'''
#Tracking individualiezeReminder as dates may vary. For instance there may be customers that owe the company with different deadlines for payments. So each reminder need to be individualized. Or it may be about company drivers renew of driver licence/ car insurance or service due
class IndividualizedReminder(Base):
     __tablename__="individualized_reminders"
     id=Column("individualized_reminders_id",Integer,primary_key=True)
     campaign_id=Column(Integer, ForeignKey("campaigns.campaign_id"))
     contact_id=Column(Integer,ForeignKey("address_book.contact_id"))
     reminder_end_date=Column(Date)
     event_deadline_date=Column(Date)
     no_running_days=Column(Integer)

     reason_for_reminder=Column(String(200)) #Examples, expiry of driving licence or insurance, debt to be paid for rendered service or school fees, clinical appointment etc.
     def __init__(self,contact_id,reminder_end_date,event_deadline_date,no_running_days,reason_for_reminder):
          self.contact_id=contact_id
          self.reminder_end_date=reminder_end_date
          self.event_deadline_date=event_deadline_date
          self.no_running_days=no_running_days
          self.reason_for_reminder=reason_for_reminder
     

'''
#Keeping track of all messages sent out 
class CampaignDeliveryHistory(Base):
     __tablename__="campaign_delivery_history"
     campaign_id=Column(Integer, ForeignKey("campaigns.campaign_id"),primary_key=True)
     contact_id= Column(Integer, ForeignKey("address_book.contact_id"))
     feedback_id=Column(Integer, ForeignKey("feedback.id")) #It easier to know from which campaign messages belong to

'''

#Base.metadata.create_all(db)
