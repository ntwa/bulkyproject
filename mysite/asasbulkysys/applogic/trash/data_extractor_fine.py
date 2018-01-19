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

        filter_date_str='2015-11-02'
        filter_date_str2='2015-11-26'



        filter_date=datetime.datetime.strptime(filter_date_str,'%Y-%m-%d').date()
        filter_date2=datetime.datetime.strptime(filter_date_str2,'%Y-%m-%d').date()

        demarcation_date=datetime.datetime.strptime(demarcation_date_str,'%Y-%m-%d').date()

        demarcation_date0=datetime.datetime.strptime(demarcation_date_str0,'%Y-%m-%d').date()
        #print demarcation_date,demarcation_date_str
        try:
            engine=db
            #create a Session
            Session = sessionmaker(bind=engine)
            session = Session()

            res=session.query(distinct(Logs.intermediary_id).label("id")).all()
            
            posn=0

            print "User\tTotal Sessions\tNo_of_dates_phase_1\tNo_of_dates_phase_2\tNo_of_sessions_phase_1\tNo_of_sessions_phase_2\tAverage_minutes_for_sessions_phase_1\tAverage_minutes_for_sessions_phase_2"
            for user in res:
                #intermediaries.append(user.id)
                reslog=session.query(Logs).filter(Logs.intermediary_id==user.id).filter(Logs.datecaptured>=demarcation_date0).order_by(Logs.datecaptured).order_by(Logs.timecaptured).all()
                recordposn=0
                diff=0
                session_counter=0
                #These two variables count session for the first three weeks of experiment and the last two weeks of experiments
                condition_one_counter=0
                condition_two_counter=0
                #accumulate seconds for each user on each session
                minutes_phase_1=0
                minutes_phase_2=0

                for logrecord in reslog:
        
                    datecaptured=logrecord.datecaptured
                    if datecaptured>=filter_date and datecaptured<demarcation_date:
                        continue
                    elif datecaptured>filter_date2:
                        break

                    timecaptured=logrecord.timecaptured
                    hr=timecaptured.hour
                    mn=timecaptured.minute
                    sec=timecaptured.second
                    
                    #now add hours to date captured
                    #newdate=datecaptured;
                    #print datecaptured.second
                    datestr=datecaptured.strftime('%Y-%m-%d')

                    newdate=datetime.datetime.strptime(datestr,'%Y-%m-%d').replace(hour=hr,minute=mn,second=sec)
                    newdate2=newdate.strftime('%Y-%m-%d %H:%M:%S')
                    #print "New=",newdate2
                    if recordposn==0:
                      previousdatecaptured=newdate
                      session_counter=session_counter+1 # start a the first session
                      condition_one_counter=condition_one_counter+1
                      time_minutes=0
                    
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


                      #diff=((delta.days*24*60)+(delta.hour*60)+(delta.seconds/60))

                      threshold=datetime.timedelta(minutes=60)
                      #print threshold
                      # now check if delta is greater than threshold of ten minutes. This implies the begining of a new session
                      if delta>threshold:
                        #print "Session"
                        session_counter=session_counter+1
                        #Categorize those in phase one of experiments vs phase two
                        if datecaptured<demarcation_date:
                          condition_one_counter=condition_one_counter+1
                        else:
                          condition_two_counter=condition_two_counter+1
                        

                      else:
                        if datecaptured<demarcation_date:
                          minutes_phase_1=minutes_phase_1+time_minutes
                        else:
                          minutes_phase_2=minutes_phase_2+time_minutes


                        #print "No session"


                      previousdatecaptured=newdate
                 
                    #print logrecord.intermediary_id," ",logrecord.datecaptured," diff=%s"%delta,"\n"
                    recordposn=recordposn+1
                    diff=0
                 #Now look for distinct dates in phase one and phase two of experiments 

                 #start with phase 1
                resdates=session.query(func.count(distinct(Logs.datecaptured)).label("counter")).filter(Logs.intermediary_id==user.id).filter(Logs.datecaptured>=demarcation_date0).filter(Logs.datecaptured<=filter_date).first()
                
                if resdates.counter is None:
                    phase_one_total=0
                else:
                    phase_one_total=resdates.counter
                    if condition_one_counter==0:
                      pass
                    else:
                      minutes_phase_1=float(minutes_phase_1/condition_one_counter)

                 #finish with phase 1
                resdates=session.query(func.count(distinct(Logs.datecaptured)).label("counter")).filter(Logs.intermediary_id==user.id).filter(Logs.datecaptured>=demarcation_date).filter(Logs.datecaptured<=filter_date2).first()
                if resdates.counter is None:
                    phase_two_total=0
                else:
                    phase_two_total=resdates.counter
                    if condition_two_counter==0:
                      pass
                    else:
                      minutes_phase_2=float(minutes_phase_2/condition_two_counter)
            



                print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(user.id,session_counter,phase_one_total,phase_two_total,condition_one_counter,condition_two_counter,minutes_phase_1,minutes_phase_2)
                 #print "total number of sessions for %s is %s sessions"%(user.id,session_counter)
                #print "\n\n\n"
              
                     

                      
 
        except Exception as e:
            print "Exception thrown in getLogs: %s"%e 
            #result["R00"]=-1
            #result["R01"]=e
          
          
        
        #self.steps=sum_steps
        session.close()
        engine.dispose()
        dbconn.close()
        
        #return (json.JSONEncoder().encode(result))


'''
    def getLogs(self,intermediary_id):
        result={}
     
        try:
            engine=db
            #create a Session
            Session = sessionmaker(bind=engine)
            session = Session()

            pilotdateres=session.query(PilotCommencement).first()

            if pilotdateres is None:
                sys.exit
            else:
                datestarted=pilotdateres.datestarted




            if self.last_date_specified==1:
                day=self.myjson["Day"]
                if day == "Today":
                    day=datetime.date.today()
                res=session.query(func.sum(PhysicalActivity.stepscounter).label("sum_steps")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured>=datestarted).filter(PhysicalActivity.datecaptured<=day).first()
         
            else:
 
                res=session.query(func.sum(PhysicalActivity.stepscounter).label("sum_steps")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured>=datestarted).first()
            
            if res.sum_steps==None:
                sum_steps=0
            else:
                sum_steps=int(res.sum_steps)
          
            result["steps"]=sum_steps
            
            if self.last_date_specified==1:
                res=session.query(func.min(PhysicalActivity.datecaptured).label("min_date")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured<=day).first()
            else: 
                res=session.query(func.min(PhysicalActivity.datecaptured).label("min_date")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).first()
            
            min_date=res.min_date 

            

            if self.last_date_specified==1:
                max_date=self.myjson["Day"]
                if max_date=="Today":
                    max_date=datetime.date.today()
                else:
                    max_date=datetime.datetime.strptime(max_date , '%Y-%m-%d').date()
            else:
                max_date=datetime.date.today()

            
            if min_date is None:
                dates_difference=1
            else:
                delta=max_date-min_date
                dates_difference=delta.days+1
                if min_date>max_date:
                    dates_difference=1
        
            result["dates_counter"]=dates_difference
                      
 
        except Exception as e:
            print "Exception thrown in function getSteps(): %s"%e 
            result["steps"]=0
            result["dates_counter"]=1
          
        
        #self.steps=sum_steps
        session.close()
        engine.dispose()
        dbconn.close()
        
        return (json.JSONEncoder().encode(result))
'''

  
  

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
