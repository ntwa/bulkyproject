from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey, ForeignKeyConstraint
from sqlalchemy import Column, Date, Integer, String, Boolean,Enum,Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr
from sqlalchemy.pool import NullPool
import json,sys
from collections import OrderedDict
import enum

#db = create_engine(connstr,pool_size=20, max_overflow=0)
if db is None and dbconn is None:
    db = create_engine(connstr,poolclass=NullPool)
    dbconn=db.connect()

if Base is None:
    Base = declarative_base()
#Base = declarative_base()
class CampaignOptions(enum.Enum):
    rem = "Reminders"
    indgre= "Individual Best Wishes"
    grgre="Holiday Greetings"
    thirdval = "Holiday Adverts"
    thirdval = "General Marketing"

#campaign definition
class Campaign(Base):
    __tablename__="campaigns"
    id=Column("campaign_id",Integer,primary_key=True)
    campaign_name=Column(String(200))
    campaign_description=Column(String(500))
    campaign_category=Column(Enum(CampaignOptions))
    is_it_life_time_campaign=Column(Boolean) # Some Campaign may be set to run year after year over a lifetime.
    is_campaign_date_constant=Column(Boolean) # Some campaigns may  be holidays that have fixed date, some may not be fixed, meaning they have to be updated anually to reflect the current year if it is a lifetime campaign.
  
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id

class CampaignDefinedMessages(Base):
    __tablename__="campaigns_defined_messages"
    id=Column("campaign_message_id",Integer,primary_key=True)
    campaign_id=Column(Integer, ForeignKey("campaigns.campaign_id"))
    message_txt=Column(String(500))

    
    def __init__(self,contact_id,group_id):
         self.contact_id=contact_id
         self.group_id=group_id


Base.metadata.create_all(db)
