#from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from bulkysms.database.dbinit import db,dbconn
from bulkysms.database.base  import Base


#import bulkysms.database.a
#import bulkysms.database.b
#import bulkysms.database.c

from bulkysms.database.a import A
from bulkysms.database.b import B
from bulkysms.database.c import C
engine=db
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

#a1 = bulkysms.database.a.A()
#b1 = bulkysms.database.b.B()
#b2 = bulkysms.database.b.B()
#c1 = bulkysms.database.c.C()
#c2 = bulkysms.database.c.C()

a1 = A()
b1 = B()
b2 = B()
c1 = C()
c2 = C()

a1.Bs.append(b1)
a1.Bs.append(b2)    
a1.Cs.append(c1)
a1.Cs.append(c2)    
session.add(a1)
session.commit()