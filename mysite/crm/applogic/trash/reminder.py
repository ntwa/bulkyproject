#This script runs every monday morning
#!/usr/bin/env python
import datetime,calendar
import sys,json
from sqlalchemy import create_engine,distinct,func,asc
from sqlalchemy.orm import sessionmaker
from wellness.applogic.points_module import Points,db
from wellness.applogic.badges_module import Badges,AttainedUserBadges
from retrieve_intermediary import RetrieveIntermediary
from wellness.applogic.intermediary_module import Intermediary
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
    def getSteps(self,beneficiary_id):
        

        try:
            engine=db
            #create a Session
            Session = sessionmaker(bind=engine)
            session = Session()

            currentdate=datetime.date.today()
            
            #get the date for the first day of this week
            day_of_week=currentdate.weekday()
            week_start_date=currentdate-datetime.timedelta(days=day_of_week)            
            
          
            
 
            res=session.query(func.sum(PhysicalActivity.stepscounter).label("sum_steps")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured>=week_start_date).filter(PhysicalActivity.datecaptured<=currentdate).first()
            
            
            if res.sum_steps==None:
                sum_steps=0
            else:
                sum_steps=int(res.sum_steps)
            result={}
            result["steps"]=sum_steps
     

        except Exception as e:
            print "Exception thrown in function getSteps(): %s"%e 
            result["steps"]=0
            result["dates_counter"]=1
        
        
        #self.steps=sum_steps
        session.close()
        engine.dispose()
        dbconn.close()

        return (json.JSONEncoder().encode(result))





       
    
    def retrieveIntermediaryClickPoints(self):
         result={}       
         try:
              #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
              engine=db
              # create a Session
              Session = sessionmaker(bind=engine)
              session = Session()
                                  

              #if self.last_date_specified==1:
              #    day=self.myjson["Day"]
              #    if day=="Today":
              #       day=datetime.date.today()
                           
              #res= session.query(func.sum(Points.scoredpoints).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured<=day).first()
              #get points by number of days an application has been used.
              #res=session.query(func.count(distinct(Points.datecaptured)).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured<=day).first()
              #else:
                  #res= session.query(func.sum(Points.scoredpoints).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).first()
              res=session.query(func.count(distinct(Points.datecaptured)).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).first()


              
              retrieved_points_sum=0# initialize how many distinct dates are in the database
              #for retrieved_points_sum in res:
              #     break               
              
              
              if res.sum_points is None:
                   
                   retrieved_points_sum="0"
                   result["message"]="You have no points"
                   result["points"]=int(retrieved_points_sum)
              else: 
                   result["message"]="You have some points so far."
                   retrieved_points_sum=int(res.sum_points)
                   result["points"]=int(retrieved_points_sum)
 

            





 
              session.close()
              engine.dispose()
              dbconn.close()
                   
              return (json.JSONEncoder().encode(result))                   
                                  
         except Exception as e:
                        
              #print "Content-type: text/html\n" 
              session.close()
              engine.dispose() 
              dbconn.close()
                                
              result["message"]="Error: %s"%e
              print "Exception thrown in function getIntermediaryClickPoints(): %s"%e
              print "The day captured=%s"%day
              return (json.JSONEncoder().encode(result))
              #sys.exit()    
              


    def tipOftheDay(self):
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
             
             
        try:
          
          myjson={'Fname':'Dummy','Lname':'Dummy','Username':'dummy'}
          obj=RetrieveIntermediary(myjson)
          res=obj.retrieveIntermediaryInDB()
          
          intermediaries_tuple=json.loads(res)
          intermediaries_emails=[]
          intermediary_names=[]
          orig_emails=[]
          beneficiary_ids=[]
          beneficiary_names=[]
          intermediary_mobiles=[]
          beneficiary_relations=[]
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
          bonus_points=[]
          badges=[]
          badges_urls=[]
          
          currentdate=datetime.datetime.today()
          #get the date for the first day of this week
          day_of_week=currentdate.weekday()
          week_start_date=currentdate-datetime.timedelta(days=day_of_week)   
         
          #get the first and end date of last week
          previous_week_end_date=week_start_date-datetime.timedelta(days=1) #go to last sunday
          previous_week_start_date=previous_week_end_date-datetime.timedelta(days=6)#go to last monday
          
          
          #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
          engine=db
          # create a Session
          Session = sessionmaker(bind=engine)
          session = Session()
          
          res2=session.query(AttainedUserBadges,Badges,Intermediary).filter(Intermediary.intermediary_id==AttainedUserBadges.intermediary_id).filter(AttainedUserBadges.status==1).filter(AttainedUserBadges.badge_id==Badges.rank).filter(AttainedUserBadges.date_attained>=previous_week_start_date).filter(AttainedUserBadges.date_attained<=previous_week_end_date).all()
          users_with_progress_str="|"
          
          
          users_with_progress=0
          
          
          for rel1,rel2,rel3 in res2:
            users_with_progress_str=users_with_progress_str+rel3.intermediary_fname
            users_with_progress_str=users_with_progress_str+" "
            #users_with_progress_str=users_with_progress_str+rel3.intermediary_lname
            users_with_progress_str=users_with_progress_str+", Badge:"
            users_with_progress_str=users_with_progress_str+rel2.badgename
            users_with_progress_str=users_with_progress_str+"|"
            users_with_progress=users_with_progress+1
      
           
          for record in intermediaries_tuple.items():
               
               
               key,user =record
              
               if(user["D2"]=="None"):
                   continue
               else:
                    
                    orig_email=user["D1"]
                    myjson={'Fname':'Dummy','Lname':'Dummy','Username':orig_email}
                    obj=RetrieveIntermediary(myjson)
                    result2=obj.isAssignedBeneficiary()

                    usergroupres=obj.getUserGroup()                    
                    usergroupres=json.loads(usergroupres)
                    usergroup=usergroupres["Group"]
                    if usergroup==2:
                        continue


 
                    orig_emails.append(user["D1"]) #keep original email addresses
                    #orig_email=user["D1"]
               
                    user["D1"]=user["D1"].replace("@","_at_")
                    user["D1"]=user["D1"].replace(".","_dot_")
                    
                    intermediaries_emails.append(user["D1"])
                    intermediary_names.append(user["D0"])
                    beneficiary_names.append(user["D2"][0:user["D2"].index('.')])# get the name only
                    beneficiary_relations.append(user["D3"][(user["D3"].index(':')+1):(len(user["D3"]))])
                    intermediary_mobiles.append(user["D5"][(user["D5"].index(':')+1):(len(user["D5"]))])
                    first_name=intermediary_names[posn][0:(intermediary_names[posn].index(' ')+1)] # 
                    '''
                    myjson={'Fname':'Dummy','Lname':'Dummy','Username':orig_email}
                    obj=RetrieveIntermediary(myjson)
                    result2=obj.isAssignedBeneficiary()
                    
                    usergroupres=obj.getUserGroup()
                    usergroupres=json.loads(usergroupres)
                    usergroup=usergroupres["Group"]
                    if usergroup==2:
                        continue
                    '''
                    beneficiary_tuple=json.loads(result2)
                    beneficiary_ids.append(beneficiary_tuple["Id"])
                    
                    
                  
                    file_path="django_facebook/images/garden/%s/%s_%s.jpeg"%(intermediaries_emails[posn],beneficiary_ids[posn],garden_label)
                    
                    file_name="%s_%s"%(beneficiary_ids[posn],garden_label)
                    urls.append(file_path)
          
                    message_counter=0
                  
                    
                      
                        # select one message out of five messages
                       # num=randint(0,4)
                    message_bank=[]



                    feedback_message="Reminder: Hey %s "%first_name

                    feedback_message=feedback_message+"! Dont forget to share the app information with your  %s so that she/he can walk more steps...[This message was autogenerated by the 'Family Wellness App']"% beneficiary_relations[posn]
                    message_bank.append(feedback_message)
                    message_counter=message_counter+1

                    feedback_message="Reminder: Hey %s "%first_name

                    feedback_message=feedback_message+"! Did  you remember to record every meal eaten by your  %s...[This message was autogenerated by the 'Family Wellness App']"% beneficiary_relations[posn]
                    message_bank.append(feedback_message)


                    feedback_message="Reminder: Hallo %s "%first_name

                    feedback_message=feedback_message+",your  %s's health is more important. Don't forget to record what she ate...[This message was autogenerated by the 'Family Wellness App']"% beneficiary_relations[posn]
                    message_bank.append(feedback_message)
                    message_counter=message_counter+1




                    feedback_message="Reminder: Hi %s "%first_name

                    feedback_message=feedback_message+", don't forget to check how much your %s has walked today...[This message was autogenerated by the 'Family Wellness App']"% beneficiary_relations[posn]
                    message_bank.append(feedback_message)
                    message_counter=message_counter+1

          


                    feedback_message="Reminder: Hallo %s "%first_name
                    feedback_message=feedback_message+",  tell your %s to continue to be more active. Your %s needs to aim to reach a goal of 10000 steps in order to be healthy...[This message was autogenerated by the 'Family Wellness App']"%(beneficiary_relations[posn],beneficiary_relations[posn])
                    message_bank.append(feedback_message)
                    message_counter=message_counter+1


                    feedback_message="Reminder: Hi %s "%first_name
                    feedback_message=feedback_message+", Tell your %s fruits and vegetables are important for living healthy..[This message was autogenerated by the 'Family Wellness App']"% beneficiary_relations[posn]
                    message_bank.append(feedback_message)
                    message_counter=message_counter+1

                    feedback_message="Reminder: Whats up %s "%first_name
                    feedback_message=feedback_message+", have you remembered to check the app today?..[This message was autogenerated by the 'Family Wellness App']"
                    message_bank.append(feedback_message)
                    message_counter=message_counter+1


                    feedback_message="Reminder: Hello %s "%first_name
                    feedback_message=feedback_message+", Have remembered to record meals eaten by your %s, today [This message was autogenerated by the 'Family Wellness App']"% beneficiary_relations[posn]
                    message_bank.append(feedback_message)
                    message_counter=message_counter+1


                   
                    num=randint(0,message_counter-1)
                    print message_bank[num]
                        
                
                                    
                    myjson2={"recipient":intermediary_mobiles[posn],"message":message_bank[num]}
                        
                    obj=QueueFeedback(myjson2)
                    res=obj.saveFeedbackInDB()

                    posn=posn+1
        except Exception as e:
          print "Exception thrown %s "%e 
          return -1
              
                
                  
        return 1         
      
         

              
     
     
     


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
recommendations=[]

myjson={'Day':score_date_str2}
obj=RetrievePoints(myjson,'katulentwa@gmail.com',0)
result=obj.tipOftheDay()

if result==1:
  print "The tip of the day has been scheduled"
else:
  print "The schedule of the tip failed to complete"

