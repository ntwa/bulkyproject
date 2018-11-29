#from sqlalchemy import create_engine, ForeignKey, ForeignKeyConstraint
#from sqlalchemy import Column, Date, Integer, String, Boolean, Enum, Time, Float
#from sqlalchemy.orm import relationship, backref,sessionmaker
from sqlalchemy.pool import NullPool
from dbconnect import connstr
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
try:
     db 
except NameError as e:
     db = create_engine(connstr,poolclass=NullPool)


try:
     dbconn
except NameError as e:
     dbconn=db.connect()
