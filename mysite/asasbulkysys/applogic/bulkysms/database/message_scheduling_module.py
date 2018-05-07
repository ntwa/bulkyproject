from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date,Time, Integer, String,Float,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr
from sqlalchemy.pool import NullPool

#db = create_engine(connstr,pool_size=20, max_overflow=0)
db = create_engine(connstr,poolclass=NullPool)
dbconn=db.connect()
Base = declarative_base()

class ScheduledMessage(Base): #If a message is to be repeated several times in a day. Then clone the same message to the number of times it has to repeat
    __tablename__="scheduled_messages"
    id=Column("message_id",Integer, primary_key=True)
    time_for_sending_out=Column(Time)
    time_limit_for_sending_out_=Column(Time)
    expiry_date=Column(Date) #if the message has no expiry date it means it will run indefinately
    last_date_sent = Column(Date) #This is for keeping track if a message has already ran in a particular day
    is_message_personalized=Column(Boolean);    
    
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

class CampaignMessage(ScheduledMessage): #If a message is to be repeated several times in a day. Then clone the same message to the number of times it has to repeat
    __tablename__="scheduled_messages"
    id=Column("message_id",Integer, primary_key=True)
    messagetxt=Column(String(500))
    time_for_sending_out=Column(Time)
    time_limit_for_sending_out_=Column(Time)
    expiry_date=Column(Date) #if the message has no expiry date it means it will run indefinately
    last_date_sent = Column(Date) #This is for keeping track if a message has already ran in a particular day
        
    
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

class GroupMessage(CampaignMessage): #If a message is to be repeated several times in a day. Then clone the same message to the number of times it has to repeat
    __tablename__="scheduled_messages"
    id=Column("message_id",Integer, primary_key=True)
    messagetxt=Column(String(500))
    time_for_sending_out=Column(Time)
    time_limit_for_sending_out_=Column(Time)
    expiry_date=Column(Date) #if the message has no expiry date it means it will run indefinately
    last_date_sent = Column(Date) #This is for keeping track if a message has already ran in a particular day
        
    
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

class IndividualMessage(CampaignMessage): #If a message is to be repeated several times in a day. Then clone the same message to the number of times it has to repeat
    __tablename__="scheduled_messages"
    id=Column("message_id",Integer, primary_key=True)
    messagetxt=Column(String(500))
    time_for_sending_out=Column(Time)
    time_limit_for_sending_out_=Column(Time)
    expiry_date=Column(Date) #if the message has no expiry date it means it will run indefinately
    last_date_sent = Column(Date) #This is for keeping track if a message has already ran in a particular day
        
    
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


Base.metadata.create_all(db)
