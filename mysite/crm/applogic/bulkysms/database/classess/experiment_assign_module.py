from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Time, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn2 import connstr


db2 = create_engine(connstr ,pool_size=20, max_overflow=0)
Base = declarative_base()


       
class Users(Base):
    __tablename__="auth_user"
    id = Column(Integer,primary_key=True)
    password = Column(String(128))
    last_login=Column(Date)
    is_superuser=Column(Integer)
    username=Column(String(30))
    first_name=Column(String(30))
    last_name=Column(String(30))
    email=Column(String(30))
    is_staff=Column(Integer)
    is_active=Column(Integer)
    date_joined=Column(Date)    
    experimentgroup = relationship("ExperimentGroup", backref=backref("auth_user", order_by=username))

    #def __repr__(self):
    #    return str("%s %s. UserID:%s"%(self.intermediary_fname,self.intermediary_lname,self.intermediary_id))
       
class ExperimentGroup(Base):
    __tablename__="experiment_group_assignments"
    id = Column(Integer,primary_key=True)
    username=Column(String(30),ForeignKey("auth_user.username"))
    experiment_no=Column(Enum('1','2'), nullable=False)
    date_assigned=Column(Date)
    status=Column(Boolean)

    def __init__(self,username,experiment_no,date_assigned,status):     

        self.username=username
        self.experiment_no=experiment_no
        self.date_assigned=date_assigned
        self.status=status        
    
Base.metadata.create_all(db2)


    
