from sqlalchemy import *
#from bulkysms.database.base  import Base
from sqlalchemy.orm import relationship

class A(Base):
    __tablename__ = "A"
    id  = Column(Integer, primary_key=True)
    Bs  = relationship("B", backref="A.id")
    Cs  = relationship("C", backref="A.id")