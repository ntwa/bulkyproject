#!/usr/bin/env python
import datetime
import time
import sys,json
#sys.path.insert(0, 'C:\\workspace\\test\\helloword\\sqlalchemy.zip')
sys.path.insert(0, 'sqlalchemy.zip')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.logs_module import Logs,db,dbconn
from collections import OrderedDict
from wellness.applogic.clicked_items_module import ClickedItemsRecord

class SaveLogs:
     def __init__(self,myjson,intermediary_id,usergroup):
          self.myjson=myjson
          self.intermediary_id=intermediary_id
          self.usergroup=usergroup
     def saveLogsInDB(self):
               
          datecaptured=""
          timecaptured=""
          clickscounter=0
          result={}
          allow_insert=1
          # Get data from fields
          try:
              
               clickscounter=self.myjson["ClicksCounter"]; 
               #clickscounter=40
               datecaptured = datetime.date.today()
               #timecaptured=time.strftime("%H:%M:%S")
               timecaptured=time.strftime("%H:%M:%S")
               clickeditems=self.myjson["ClickedItems"]               
               e="Error"
                        
                             
          except Exception as e:
               logs_tuples={}
               logs_tuple={}
     
               key1="R"
               key2="F"
               first_posn=0
               second_posn=0
               logs_tuple[key2+"%d"%second_posn]=e
               second_posn=second_posn+1
                                                                                                                                                                             
                                                                                                                                                                             
               logs_tuple[key2+"%d"%second_posn]=-1
               second_posn=0 
               if first_posn<10:
                    key1="R0"
               else:
                    key1="R"
                                                                                                                                            
               logs_tuples[key1+"%d"%first_posn]=logs_tuple
                                                                                                                                          
               first_posn=first_posn+1 
               logs_tuple={}
               return(json.JSONEncoder().encode(OrderedDict(sorted(logs_tuples.items(), key=lambda t: t[0]))))
          
          try:
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()

               for itemtuple in clickeditems.items():
                    key,item=itemtuple
                    print "1--",itemtuple
                    new_item_clicked=ClickedItemsRecord(self.intermediary_id,item,datecaptured,timecaptured,self.usergroup)
                    session.add(new_item_clicked)
                    session.commit()
          except Exception as e:
               print e
               
          
          
                            
                         
                         
          if allow_insert==1:
               try:
                    #print "Content-Type: text/html\n"
                    #engine=db
                    # create a Session
                    Session = sessionmaker(bind=engine)
               
                    session = Session()
               
                    # Create weight
                    #new_food=FoodAndBeverage('KTLNTW00',datetime.date(1988,12,01))
                    new_clickscounter=Logs(self.intermediary_id,clickscounter,datecaptured,timecaptured,self.usergroup)
                         
                    session.add(new_clickscounter)
               
               
                    # commit the record the database
               
               
                    session.commit()

                    result["message"]="The clicks was recorded sucessfully"
                    
               except Exception as e:
                    result["message"]=e
                    session.close()
                    engine.dispose()
                    dbconn.close()

                    return (json.JSONEncoder().encode(result)) 
          
          session.close()
          engine.dispose()          
          dbconn.close()
          return (json.JSONEncoder().encode(result))
#myjson={"ClicksCounter":4,"ClickedItems":{"Key0":"Game12","Key1":"Activity"}}
#obj=SaveLogs(myjson,"ntwa.katule",1)
#result=obj.saveLogsInDB()
#print result
