#!/usr/bin/env python
import datetime,calendar
from datetime import timedelta
import sys,json
from sqlalchemy import create_engine,distinct,func,asc
from sqlalchemy.orm import sessionmaker
from wellness.applogic.points_module import Points,db
from wellness.applogic.logs_module import Logs,db,dbconn
from wellness.applogic.clicked_items_module import ClickedItemsRecord
import os.path

    

class RetrieveLogData:
    def __init__(self):
        pass

    def getLogs(self):
        demarcation_date_str0='2015-10-18'
        
        demarcation_date_str='2015-11-12'

        demarcation_date=datetime.datetime.strptime(demarcation_date_str,'%Y-%m-%d').date()

        demarcation_date0=datetime.datetime.strptime(demarcation_date_str0,'%Y-%m-%d').date()
        #print demarcation_date,demarcation_date_str
        try:
            engine=db
            #create a Session
            Session = sessionmaker(bind=engine)
            session = Session()

            res=session.query(distinct(Logs.intermediary_id).label("id")).all()
            
           
            user_posn=0
            user_dict={}
            key="User"
            key2="Day"
            for user in res:
                #intermediaries.append(user.id)
                reslog=session.query(Logs).filter(Logs.intermediary_id==user.id).filter(Logs.datecaptured>=demarcation_date0).order_by(Logs.datecaptured).order_by(Logs.timecaptured).all()
                recordposn=0
                diff=0
                session_counter=0
                each_day_session=0
                user_sessions={}
                posn=0 #For tracking days from each user
                total_day_session_this_day=0
                for logrecord in reslog:
                    
                    datecaptured=logrecord.datecaptured
                    timecaptured=logrecord.timecaptured
                    hr=timecaptured.hour
                    mn=timecaptured.minute
                    sec=timecaptured.second
                    print user.id,datecaptured
                    
 
                    datestr=datecaptured.strftime('%Y-%m-%d')

                    newdate=datetime.datetime.strptime(datestr,'%Y-%m-%d').replace(hour=hr,minute=mn,second=sec)
                    newdate2=newdate.strftime('%Y-%m-%d %H:%M:%S')
                    print "Carry on"

                    if recordposn==0:
                      previousdatecaptured=newdate
                      session_counter=session_counter+1 # start a the first session
                    
                      time_minutes=0
                      each_day_session=each_day_session+1
                    
                    if recordposn>0:

                      
                      delta=newdate-previousdatecaptured
                      days=delta.days
                      seconds=delta.seconds
                      minutes=int((seconds/60))
                      hour=int((minutes/60))
                      seconds=seconds%60 # remainder is actual seconds
                      minutes=(minutes%60) # remainder in actual minutes
                    
                      #convert the time to seconds
                      time_minutes=float(float(delta.seconds+(days*24*60*60))/60)
                      if(time_minutes<1.0):
                        #print "Less than a minute"
                        time_minutes=1.0


                      threshold=datetime.timedelta(minutes=60)
                      #print threshold
                      # now check if delta is greater than threshold of 60 minutes. This implies the begining of a new session
                      if delta>threshold:
                        #print "Session"
                        session_counter=session_counter+1
                        if(newdate.date()>previousdatecaptured.date()):
                            #it is a new day reset session daily session counts
                            
                            tuple_day={}
                            tuple_day["Date"]=previousdatecaptured.date()
                            tuple_day["TotalSessions"]=total_day_session_this_day
                            each_day_session["key2%"%posn]=tuple_day

                            total_day_session_this_day=0
                            posn=posn+1



                        total_day_session_this_day=total_day_session_this_day+1




                        #print "No session"


                      previousdatecaptured=newdate
                 
                    #print logrecord.intermediary_id," ",logrecord.datecaptured," diff=%s"%delta,"\n"
                    recordposn=recordposn+1
                    diff=0
                    print "Got last"
                #now put the last sssion counter
                tuple_day={}
                tuple_day["Date"]=previousdatecaptured.date()
                tuple_day["TotalSessions"]=total_day_session_this_day

                user_sessions["%s%s"%(key2,posn)]=tuple_day

                user_tuple={}
                user_tuple["User"]=user.id
                user_tuple["Sessions"]=user_sessions


                posn=0

                user_posn=user_posn+1

                user_dict["%s%s"%(key,user_posn)]=user_tuple

           
                user_posn=user_posn+1     

                      
 
        except Exception as e:
            print "Exception thrown in getLogs: %s"%e 
            user_dict["User0"]=-1
            #result["R00"]=-1
            #result["R01"]=e
          
          
        
        #self.steps=sum_steps
        session.close()
        engine.dispose()
        dbconn.close()
        
        return (json.JSONEncoder().encode(user_dict))


  
  

obj=RetrieveLogData()
result=obj.getLogs()
#result=obj.retrieveScoreGardensUrls()
print result
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
