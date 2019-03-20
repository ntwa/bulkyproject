from sqlalchemy import *
#from bulkysms.database.base  import Base

class B(Base):
    __tablename__ = "B"
    id    = Column(Integer, primary_key=True)
    A_id  = Column(Integer, ForeignKey("A.id"))