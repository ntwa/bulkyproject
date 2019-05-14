#!/usr/bin/env python
import datetime,calendar
from datetime import timedelta
import sys,json
from sqlalchemy import create_engine,distinct,func,asc
from sqlalchemy.orm import sessionmaker
from wellness.applogic.points_module import Points,db
from wellness.applogic.logs_module import Logs,db,dbconn
from wellness.applogic.clicked_items_module import ClickedItemsRecord
from retrieve_intermediary import RetrieveIntermediary

import os.path

    

class RetrieveLogData:
    def __init__(self):
        pass

    def getLogs(self):
        start_date_str='2015-10-18'
        mid_date_str='2015-11-13'
        end_date_str='2015-11-27'


        start_date=datetime.datetime.strptime(start_date_str,'%Y-%m-%d').date()
        mid_date=datetime.datetime.strptime(mid_date_str,'%Y-%m-%d').date()
        end_date=datetime.datetime.strptime(end_date_str,'%Y-%m-%d').date()
        

        try:

            print "Date\tLogbook\Gamification\n"
            while start_date<end_date:
                gamification_counter=0
                logbook_counter=0
                engine=db

                #create a Session
                Session = sessionmaker(bind=engine)
                session = Session()
                res=session.query(distinct(Logs.intermediary_id).label("id"),Logs.usergroup).filter(Logs.datecaptured==start_date).all()
                
                #print "%s\t"%start_date
                
                for user in res:
                    
                    #myjson={'Username':user.id}
                    #obj=RetrieveIntermediary(myjson)
                    #userjson=obj.getUserGroup()

                    #retuser=json.loads(userjson)
                    #usergroup=retuser["Group"]
                    usergroup=user.usergroup
                    if start_date<mid_date:#Phase 1
                        if usergroup==1:
                            gamification_counter=gamification_counter+1
                        else:
                            logbook_counter=logbook_counter+1
                    else: # Phase 2
                        if usergroup==1:
                            logbook_counter=logbook_counter+1  
                        else:
                            gamification_counter=gamification_counter+1



                print "%s\t%s\t%s\n"%(start_date,logbook_counter,gamification_counter)

                #Reset counters to zero     
                logbook_counter=0
                gamification_counter=0

                

                start_date=start_date+datetime.timedelta(days=1) #increment start date by 1 day

            

 
        except Exception as e:
            print "Exception thrown in getLogs: %s"%e 
            #result["R00"]=-1
            #result["R01"]=e
          
          
        
        #self.steps=sum_steps
        session.close()
        engine.dispose()
        dbconn.close()
        
        #return (json.JSONEncoder().encode(result))

  
  

obj=RetrieveLogData()
result=obj.getLogs()
#result=obj.retrieveScoreGardensUrls()
#print result
#result=obj.getUpdatedComments()
#print result
#result=obj.getCurrentRank()
#result=obj.countRecordedMeals()

#result=obj.getUpdatedAquariumComments()
#print result
#print result

#myjson={'Day':'Today'}
#obj=RetrievePoints(myjson,'katulentwa@gmail.com')
#print resulti
