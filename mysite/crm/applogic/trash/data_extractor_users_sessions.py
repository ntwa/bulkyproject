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

            print "Date\tLogbook Users\tGamification Users\tLogbook Total Sessions\tGamification Total Sessions"
            while start_date<end_date:
                gamification_counter=0
                logbook_counter=0
                engine=db

                #create a Session
                Session = sessionmaker(bind=engine)
                session = Session()
                res=session.query(distinct(Logs.intermediary_id).label("id"),Logs.usergroup).filter(Logs.datecaptured==start_date).all()
                gamification_session_counter=0
                logbook_session_counter=0
                #print "%s\t"%start_date
                
                for user in res:
                    

                    usergroup=user.usergroup
                    #if start_date<mid_date:#Phase 1
                    #    if usergroup==2:
                    #        gamification_counter=gamification_counter+1
                    #    else:
                    #        logbook_counter=logbook_counter+1
                    #else: # Phase 2
                    #    if usergroup==1:
                    #        logbook_counter=logbook_counter+1  
                    #    else:
                    #        gamification_counter=gamification_counter+1

                    #now extract total number of sessions for this user on this particular day
                    reslog=session.query(Logs).filter(Logs.intermediary_id==user.id).filter(Logs.datecaptured==start_date).order_by(Logs.datecaptured).order_by(Logs.timecaptured).all()
                    recordposn=0
                    diff=0
                    

                    
                    
                    for logrecord in reslog:
                        
                        datecaptured=logrecord.datecaptured
                        timecaptured=logrecord.timecaptured
                        hr=timecaptured.hour
                        mn=timecaptured.minute
                        sec=timecaptured.second
                        #print "%s\t%s\t%s"%(user.id,datecaptured,timecaptured)

                        datestr=datecaptured.strftime('%Y-%m-%d')

                        newdate=datetime.datetime.strptime(datestr,'%Y-%m-%d').replace(hour=hr,minute=mn,second=sec)
                        newdate2=newdate.strftime('%Y-%m-%d %H:%M:%S')
                        #print "New=",newdate2
                        if recordposn==0:
                            
                            previousdatecaptured=newdate
                    


                            time_minutes=0

                            if start_date<mid_date:# Phase 1

                                if usergroup==2:
                             
                                    gamification_session_counter=gamification_session_counter+1
                                else:
                                    logbook_session_counter=logbook_session_counter+1
                            else: # Phase 2
                                if usergroup==1:

                                    logbook_session_counter=logbook_session_counter+1
                                else:
                                    gamification_session_counter=gamification_session_counter+1
                         
                        if recordposn>0:
                            delta=newdate-previousdatecaptured
                            days=delta.days
                            seconds=delta.seconds
                            minutes=int((seconds/60))
                            hour=int((minutes/60))
                            seconds=seconds%60 # remainder in actual seconds
                            minutes=(minutes%60) # remainder in actual minutes
                        
                            #convert the time to seconds
                            time_minutes=float(float(delta.seconds+(days*24*60*60))/60)
                            if(time_minutes<1.0):
                            #print "Less than a minute"
                                time_minutes=1.0


                          #diff=((delta.days*24*60)+(delta.hour*60)+(delta.seconds/60))

                            threshold=datetime.timedelta(minutes=60)
                          #print threshold
                          # now check if delta is greater than threshold of ten minutes. This implies the begining of a new session
                            if delta>threshold:
                        
                                if start_date<mid_date:
                
                                    if usergroup==2:
                               
                                        gamification_session_counter=gamification_session_counter+1
                                    else:
                                        logbook_session_counter=logbook_session_counter+1
                                else: # Phase 2
                                    if usergroup==1:

                                        logbook_session_counter=logbook_session_counter+1
                                    else:
                                        gamification_session_counter=gamification_session_counter+1
                




                            previousdatecaptured=newdate
                     
                        #print logrecord.intermediary_id," ",logrecord.datecaptured," diff=%s"%delta,"\n"
                        recordposn=recordposn+1
                        diff=0
                     #Now look for distinct dates in phase one and phase two of experiments 




                print "%s\t%s\t%s\t%s\t%s"%(start_date,logbook_counter,gamification_counter, logbook_session_counter,gamification_session_counter)

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
