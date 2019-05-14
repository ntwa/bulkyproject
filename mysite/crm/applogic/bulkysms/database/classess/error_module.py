from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String,Float,Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from dbconn import connstr
from sqlalchemy.pool import NullPool

#db = create_engine(connstr,pool_size=20, max_overflow=0)
db = create_engine(connstr,poolclass=NullPool)
dbconn=db.connect()

Base = declarative_base()

       
class Errors(Base):
    __tablename__="logs"
    id=Column(Integer, primary_key=True)
    error = Column(String(200))
  
    
    def __init__(self,error):
        self.error=error
    @abstractmethod    
    def storeErros(self):
        pass
    def __repr__(self):
        return str(self.intermediary_id)

Base.metadata.create_all(db)
