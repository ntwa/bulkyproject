#This script notify the user if there is change in steps by comparing last week and the week before last week
#this script runs very monday morning
#!/usr/bin/env python
import datetime,calendar
import sys,json
from sqlalchemy import create_engine,distinct,func,asc
from sqlalchemy.orm import sessionmaker
from wellness.applogic.points_module import Points,db
from wellness.applogic.badges_module import Badges,AttainedUserBadges
from retrieve_intermediary import RetrieveIntermediary
from collections import OrderedDict
from save_factors import ManageFactors
from save_sms_feedback import QueueFeedback
import os
from wellness.applogic.activity_module import PhysicalActivity,dbconn
#from wellness.applogic.intermediary_module import Beneficiary
from random import randint


def bubblesort(A,X,Y,Z,U,V,W,L,M,B,C):
  
  for i in range( len( A ) ):
    for k in range( len( A ) - 1, i, -1 ):
      if ( A[k]> A[k - 1] ):
        swap( A, k, k - 1 )
        swap(X, k, k - 1 )
        swap(Y, k, k - 1 )
        swap(Z, k, k - 1 )
        swap(U, k, k - 1 )
        swap(V, k, k - 1 )
        swap(W, k, k - 1 )
        swap(L, k, k - 1 )
        swap(M, k, k - 1 )
        swap(B, k, k - 1 )
        swap(C, k, k - 1 )
  return A
 
def swap( A, x, y ):
  tmp = A[x]
  A[x] = A[y]
  A[y] = tmp
  

class RetrievePoints:
    def __init__(self,myjson,intermediary_id,last_date_specified):
         self.myjson=myjson
         self.intermediary_id=intermediary_id
         self.last_date_specified=last_date_specified
   
    def first_day_of_month(self,d):
       return datetime.date(d.year, d.month, 1)
    def last_day_of_month(self,d):
       t=(calendar.monthrange(d.year,d.month))
       return datetime.date(d.year,d.month,t[1])

    #get weekly steps
    def getLogs(self,beneficiary_id):
        

        try:
            engine=db
            #create a Session
            Session = sessionmaker(bind=engine)
            session = Session()
            #if self.last_date_specified==1:
            #    day=self.myjson["Day"]
            #    if day == "Today":
            #        day=datetime.date.today()
            #    res=session.query(func.sum(PhysicalActivity.stepscounter).label("sum_steps")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured<=day).first()
         
            #else:
            currentdate=datetime.date.today()
            last_two_days=currentdate-datetime.timedelta(days=2)
            #get the date for the first day of this week
            #day_of_week=currentdate.weekday()
            #week_start_date=currentdate-datetime.timedelta(days=day_of_week)   
            
            #get the first and end date of last week
            #previous_week_end_date=week_start_date-datetime.timedelta(days=1) #go to last sunday
            #previous_week_start_date=previous_week_end_date-datetime.timedelta(days=6)#go to last monday
            
            #get the first and end date of the week before last week
            #previous_previous_week_end_date=previous_week_start_date-datetime.timedelta(days=1) #go to last sunday of the week before last week
            #previous_previous_week_start_date=previous_previous_week_end_date-datetime.timedelta(days=6)#go to last monday of the week before last week
          
            
 
            res=session.query(func.count(Logs.clickscounter).label("number_of_clicks")).filter(Logs.intermediary_id==intermediary_id).filter(Logs.datecaptured>=last_two_days).filter(Logs.datecaptured<=currentdate).first()
            
            
            if res.number_of_clicks==None:
                clicks_counter1=0
            else:
                clicks_counter1=int(res.number_of_clicks)
            result={}
            result["clicks1"]=clicks_counter1
            
            
            
            
            res=session.query(func.count(Logs.clickscounter).label("number_of_clicks")).filter(Logs.intermediary_id==intermediary_id).filter(Logs.datecaptured==currentdate).first()
            if res.number_of_clicks==None:
                clicks_counter2=0
            else:
                clicks_counter2=int(res.number_of_clicks)
          
            result["clicks2"]=sum_steps2
            
            
            

        except Exception as e:
            print "Exception thrown in function getSteps(): %s"%e 
            result={}
            result["steps1"]=0
            result["steps2"]=0
            result["dates_counter"]=1
        
        
        #self.steps=sum_steps
        session.close()
        engine.dispose()
        dbconn.close()
      
        return (json.JSONEncoder().encode(result))

   
            



    def checkPastThreeDaysClicks(self):
        result={}
        try:
            
             day=self.myjson["Day"]
                                 
        except Exception as e:
             #print "Content-type: text/html\n" 
             result["message"]="Error%s"%e.message
             return (json.JSONEncoder().encode(result))

        
        if day is not None:
            #if day=="Today":
            #    today_date=datetime.date.today()
            #    date_str="%s"%today_date 
            #else:
            date_str="%s"%day
        else:
             result["message"]="Error: The option '%s' is invalid"%day
             return (json.JSONEncoder().encode(result))
             
             
             
        
        
        myjson={'Fname':'Dummy','Lname':'Dummy','Username':'dummy'}
        obj=RetrieveIntermediary(myjson)
        res=obj.retrieveIntermediaryInDB()
        
        intermediaries_tuple=json.loads(res)
        intermediaries_emails=[]
        intermediary_names=[]
        orig_emails=[]
        beneficiary_ids=[]
        beneficiary_names=[]
        beneficiary_relations=[]# The relationships between intermediaries and beneficiaries.
        beneficiary_genders=[]
        posn=0
        gardens=[]
        competitors_counter=0
        
        garden_label=date_str.replace("-","_")   
        first_posn=0
        second_posn=0

        key2="D"    
        tree_array=[]
        flower_array=[]
        total_plants=[]
        urls=[]
        usage_points=[]
        bonus_points_start=[]
        bonus_points_end=[]
        badges=[]
        badges_urls=[]
        intermediary_mobiles=[]
        
        for record in intermediaries_tuple.items():
             
             
             key,user =record
            
             if(user["D2"]=="None"):
                 continue
             else:
                  
                   
                  orig_emails.append(user["D1"]) #keep original email addresses
                  orig_email=user["D1"]
             
                  user["D1"]=user["D1"].replace("@","_at_")
                  user["D1"]=user["D1"].replace(".","_dot_")
                  
                  intermediaries_emails.append(user["D1"])
                  intermediary_names.append(user["D0"])
                  beneficiary_names.append(user["D2"][0:user["D2"].index('.')])# get the name only
                  beneficiary_relations.append(user["D3"][(user["D3"].index(':')+1):(len(user["D3"]))])
                  beneficiary_genders.append(user["D4"][(user["D4"].index(':')+1):(len(user["D4"]))])
                  intermediary_mobiles.append(user["D5"][(user["D5"].index(':')+1):(len(user["D5"]))])
                  myjson={'Fname':'Dummy','Lname':'Dummy','Username':orig_email}
                  obj=RetrieveIntermediary(myjson)
                  result2=obj.isAssignedBeneficiary()
                  
                  beneficiary_tuple=json.loads(result2)
                  beneficiary_ids.append(beneficiary_tuple["Id"])
                  
                
                  file_path="django_facebook/images/garden/%s/%s_%s.jpeg"%(intermediaries_emails[posn],beneficiary_ids[posn],garden_label)
                  
                  file_name="%s_%s"%(beneficiary_ids[posn],garden_label)
                  urls.append(file_path)
                  
    
                
                   
                  varmyjson={'Day':day}
                  
                                   
                  stepsPointsObj=RetrievePoints(varmyjson,orig_email,1)


                
                   
      
                 
                  ressteps=stepsPointsObj.getSteps(beneficiary_tuple["Id"])
                  ressteps=json.loads(ressteps)
                   

                  #stepspoints=int(ressteps["steps"]/(100*ressteps["dates_counter"]))
                  clicks_last_three_days=int(ressteps["steps1"])
                  clicks_today=int(ressteps["steps2"])
              
                  
                  
                  #append an array of total steps for each each week for the last two weeks.
                  
                  bonus_points_start.append(stepspoints_last_three_days) 
                  bonus_points_end.append(stepspoints_today)
                  
                  posn=posn+1
                  
                 
        posn=0      
        
        
        
        for beneficiary in beneficiary_ids:
            urls_tuple={}
            if first_posn<10:
              key1="R0"
            else:
              key1="R"     
              
            urls_tuple[key2+"%s"%second_posn]="%s"%intermediary_names[posn]
            second_posn=second_posn+1  #D0
            
            
            urls_tuple[key2+"%s"%second_posn]="%s"%beneficiary_names[posn]
            second_posn=second_posn+1 #D1
            
 
            urls_tuple[key2+"%s"%second_posn]="%s"%bonus_points_start[posn]
            second_posn=second_posn+1 #D2
            
            urls_tuple[key2+"%s"%second_posn]="%s"%bonus_points_end[posn]
            second_posn=second_posn+1 #D3
            
            #urls_tuple[key2+"%s"%second_posn]="%s"%badges[posn]
            #second_posn=second_posn+1
            
            
            urls_tuple[key2+"%s"%second_posn]="%s"%beneficiary_relations[posn]
            second_posn=second_posn+1 #D4
          
            
            urls_tuple[key2+"%s"%second_posn]="%s"%beneficiary_genders[posn]
            second_posn=second_posn+1 #D5

            urls_tuple[key2+"%s"%second_posn]="%s"%intermediary_mobiles[posn]
            second_posn=second_posn+1 #D6           
            
            

            
            second_posn=0
            result[key1+"%s"%first_posn]=(OrderedDict(sorted(urls_tuple.items(), key=lambda t: t[0])))
            first_posn=first_posn+1
            posn=posn+1
        
        
        return (json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))
         

              
     
     
     


highest_points=0
team=""
score_date=datetime.date.today()-datetime.timedelta(days=1)
score_date_str="%s"%score_date.strftime("%d/%m/%Y")
score_date_str2="%s"%score_date.strftime("%Y-%m-%d")
recommendation=""
url="0"
leaders_counter=0
team=[]
top_points=[]
level=[]
badge=[]
recommendations=""

myjson={'Day':score_date_str2}
obj=RetrievePoints(myjson,'katulentwa@gmail.com',0)
result=obj.checkPastThreeDaysSteps()

decoded_result=json.loads(result)

sentinal=3
counter=0
posn=0

for rec,tup in decoded_result.items():
  #team.append(tup["D0"])
  stepspoints=[]
  stepspoints.append(int(tup["D2"]))
  stepspoints.append(int(tup["D3"]))
  msg=""
  
  if (stepspoints[0]==0):

      if tup["D5"] =="Female":

        recommendations="Hello %s, your %s has not uploaded any steps in the past three days. Go to your %s's phone and open an app called Pedometer. Then click upload steps."%(tup["D0"],tup["D4"],tup["D4"])
      else:
        recommendations="Hello %s, your %s has not uploaded any steps in the past three days. You might not proceed to  higher badges. Go to your %s's phone and open an app called Pedometer. Then click upload steps."%(tup["D0"],tup["D4"],tup["D4"])
  

      msg=msg+recommendations
  else:
      recommendations="Hello %s, your %s has uploaded %s steps today . Please ensure they have uploaded all steps. Go to your %s's phone and open an app called Pedometer. Then click upload steps."%(tup["D0"],tup["D4"],stepspoints[1],tup["D4"])
      msg=msg+recommendations
      

    
  myjson2={"recipient":tup["D6"],"message":msg}
  obj=QueueFeedback(myjson2)
  result=obj.saveFeedbackInDB()
  print msg
