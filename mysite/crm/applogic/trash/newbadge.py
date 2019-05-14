#!/usr/bin/env python
#This script runs every evening at 8 PM
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
from wellness.applogic.pilot_start import PilotCommencement

 

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

    #get average steps
    def getSteps(self,beneficiary_id):
        

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
            
                res=session.query(func.sum(PhysicalActivity.stepscounter).label("sum_steps")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured>=datestarted).filter(PhysicalActivity.datecaptured<=day).first()
         
            else:
 
                res=session.query(func.sum(PhysicalActivity.stepscounter).label("sum_steps")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).first()
            
            if res.sum_steps==None:
                sum_steps=0
            else:
                sum_steps=int(res.sum_steps)
            result={}
            result["steps"]=sum_steps
            
            if self.last_date_specified==1:
                res=session.query(func.min(PhysicalActivity.datecaptured).label("min_date")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured<=day).filter(PhysicalActivity.datecaptured>=datestarted).first()
            else: 
                res=session.query(func.min(PhysicalActivity.datecaptured).label("min_date")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured>=datestarted).first()
            
            min_date=res.min_date 

            

            if self.last_date_specified==1:
                max_date=self.myjson["Day"]
           
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
        result["steps"]=result["steps"]/result["dates_counter"]

        return (json.JSONEncoder().encode(result))
        

       
    
    def retrieveIntermediaryClickPoints(self):
        result={}       
        try:
                         
            #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
            engine=db
            # create a Session
            Session = sessionmaker(bind=engine)
            session = Session()
                                

            if self.last_date_specified==1:
                day=self.myjson["Day"]
                if day=="Today":
                   day=datetime.date.today()

                res=session.query(func.count(distinct(Points.datecaptured)).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured<=day).first()        
                 #res= session.query(func.sum(Points.scoredpoints).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured<=day).first()
            #get points by number of days an application has been used.
            #res=session.query(func.count(distinct(Points.datecaptured)).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured<=day).first()
            else:
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
              


    def assignBadges(self):
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
            new_badges=[]
            teams_promoted=[]
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
                    if usergroup==1:
                        continue
                    
                    print "\n",orig_email 
                    orig_emails.append(user["D1"]) #keep original email addresses
                    #orig_email=user["D1"]
               
                    user["D1"]=user["D1"].replace("@","_at_")
                    user["D1"]=user["D1"].replace(".","_dot_")
                    
                    intermediaries_emails.append(user["D1"])
                    intermediary_names.append(user["D0"])
                    beneficiary_names.append(user["D2"][0:user["D2"].index('.')])# get the name only
                    beneficiary_relations.append(user["D3"][(user["D3"].index(':')+1):(len(user["D3"]))])
                    intermediary_mobiles.append(user["D5"][(user["D5"].index(':')+1):(len(user["D5"]))])
                    
                    
                    myjson={'Fname':'Dummy','Lname':'Dummy','Username':orig_email}
                    obj=RetrieveIntermediary(myjson)
                    result2=obj.isAssignedBeneficiary()
                  #  usergroupres=obj.getUserGroup()
                   # usergroupres=json.loads(usergroupres)
                    #usergroup=usergroupres["Group"] 
                   # if usergroup==1:
                    #    continue 
                    beneficiary_tuple=json.loads(result2)
                    beneficiary_ids.append(beneficiary_tuple["Id"])
                    
                    
                  
                    file_path="django_facebook/images/garden/%s/%s_%s.jpeg"%(intermediaries_emails[posn],beneficiary_ids[posn],garden_label)
                    
                    file_name="%s_%s"%(beneficiary_ids[posn],garden_label)
                    urls.append(file_path)
                   # 
                   #print orig_email
                   # continue      
                  
                     
                    varmyjson={'Day':day}
                    
                                     
                    clickPointsObj=RetrievePoints(varmyjson,orig_email,1)
                    resclickpoints=clickPointsObj.retrieveIntermediaryClickPoints()
                    resclickpoints=json.loads(resclickpoints)
                   
                    #clickpoints=int(resclickpoints["points"]/resclickpoints["dates_counter"])
                    clickpoints=int(resclickpoints["points"])
                    if clickpoints>18:
                        clickpoints=18
  
                  
                     
                    usage_points.append(clickpoints)
                   
                    ressteps=clickPointsObj.getSteps(beneficiary_tuple["Id"])
                    ressteps=json.loads(ressteps)
                     
  
                    #stepspoints=int(ressteps["steps"]/(100*ressteps["dates_counter"]))
                    stepspoints=int(ressteps["steps"])
                    if stepspoints>70000:
                        stepspoints=70000
                    
                    bonus_points.append(stepspoints) 
                    
                       


                    #Get the current badge of this individual
                     
                    engine=db
                    # create a Session
                    Session = sessionmaker(bind=engine)
                    session = Session()
                   

                    #get the current badge 
                    res=session.query(AttainedUserBadges).filter(AttainedUserBadges.intermediary_id==orig_email).filter(AttainedUserBadges.status==1).first()

                    if res is None:
                        #this user is not assigned a bagde 
                        currentbadge=0 #start with slave badge
                       
                    else:
                        currentbadge=res.badge_id
                    print "Current Badge 1=",currentbadge
                    old_badge=currentbadge 
                    old_badge_res=session.query(Badges).filter(Badges.rank==currentbadge).first()
                    if old_badge_res is None:
                        old_badge="None"
                    else:
                        
                        old_badge=old_badge_res.badgename
                      
                    next_badge_requirement=""                 
                    if currentbadge==2:
                        if stepspoints>=10000 and clickpoints>=18:
                                   
                            badges.append("Queen/King")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/queen.jpeg")
                        elif stepspoints>=10000:
                            badges.append("No promotion")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/princess.jpeg")
                            next_badge_requirement="You and your %s need to use the application for at least 18 days since day one to get to 'Queen/King' badge. You have used the application for only %s days"%(beneficiary_relations[posn],clickpoints)
                        else:
                            badges.append("No promotion")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/princess.jpeg")
                            next_badge_requirement="Your %s needs to walk an average of 10000 steps per day to attain 'Queen/King' badge. The average number of steps is currently at %s steps per day"%(beneficiary_relations[posn],stepspoints)
                         
                    elif currentbadge==3:
                        if stepspoints>=9000 and clickpoints>=16:
                            badges.append("Princess/Prince")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/princess.jpeg")
                        
                        elif stepspoints>=9000:
                            badges.append("No promotion") 
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/duchess.jpeg")
                            next_badge_requirement="You and your %s need to use the application for at least 16 days since day one to get to 'Princess/Prince' badge. You have used the application for only %s days"%(beneficiary_relations[posn],clickpoints)

                        else:
                            badges.append("No promotion") 
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/duchess.jpeg")
                            next_badge_requirement="Your %s needs to walk an average of 9000 steps per day to attain 'Princess/Prince' badge. The average number of steps is currently at %s steps per day"%(beneficiary_relations[posn],stepspoints)
                         

                    elif currentbadge==4:
                        if stepspoints>=8000 and clickpoints>=14:
                            badges.append("Duchess/Duke")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/duchess.jpeg")
                        elif stepspoints>=8000:
                            badges.append("No promotion")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/grandmaster.jpeg")
                            next_badge_requirement="You and your %s need to use the application for at least 14 days since day one to get to 'Duchess/Duke' badge. You have used the application for only %s days"%(beneficiary_relations[posn],clickpoints)

                        else:
                           badges.append("No promotion")
                           badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/grandmaster.jpeg")
                           next_badge_requirement="Your %s needs to walk an average of 8000 steps per day to attain 'Duchess' badge. The average number of steps is currently at %s steps per day"%(beneficiary_relations[posn],stepspoints)
                         

                    elif currentbadge==5:
                        if stepspoints>=7000 and clickpoints>=12:
                            badges.append("Grand Master")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/grandmaster.jpeg")
                        
                        elif stepspoints>=7000:

                            badges.append("No promotion")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniormaster.jpeg")
                            next_badge_requirement="You and your %s need to use the application for at least 12 days since day one to get to 'Grand Master' badge. You have used the application for only %s days"%(beneficiary_relations[posn],clickpoints)
                        else:
                            badges.append("No promotion")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniormaster.jpeg")
                            next_badge_requirement="Your %s needs to walk an average of 7000 steps per day to attain 'Grand Master' badge. The average number of steps is currently at %s steps per day"%(beneficiary_relations[posn],stepspoints)
                         
                    elif currentbadge==6:
                        print "On six"
                        if stepspoints>=6000 and clickpoints>=10:
                            print "Append"
                            badges.append("Senior Master")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniormaster.jpeg")
                        elif stepspoints>=6000:

                            badges.append("No promotion")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/master.jpeg")
                            next_badge_requirement="You and your %s need to use the application for at least 10 days since day one to get to 'Senior Master' badge. You have used the application for only %s days"%(beneficiary_relations[posn],clickpoints)
                        else:
                            badges.append("No promotion")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/master.jpeg")
                            next_badge_requirement="Your %s needs to walk an average of 6000 steps per day to attain 'Senior Master' badge. The average number of steps is currently at %s steps per day"%(beneficiary_relations[posn],stepspoints)
                         
                    elif  currentbadge==7:
                        print "On seven",stepspoints,clickpoints
                        if stepspoints>=5000 and clickpoints>=8:
                            print "Append"
                            badges.append("Master")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/master.jpeg")
                        elif stepspoints>=5000:
                            print "Got here"
                            badges.append("No promotion")               
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/juniormaster.jpeg")
                            next_badge_requirement="You and your %s need to use the application for at least 8 days since day one to get to 'Master' badge. You have used the application for only %s days"%(beneficiary_relations[posn],clickpoints)

                        else:
                            badges.append("No promotion")               
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/juniormaster.jpeg")
                            next_badge_requirement="Your %s needs to walk an average of 5000 steps per day to attain 'Master' badge. The average number of steps is currently at %s steps per day"%(beneficiary_relations[posn],stepspoints)
                         
                    elif currentbadge==8:
                        if stepspoints>=4000 and clickpoints>=4:
                            badges.append("Junior Master")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/juniormaster.jpeg")
                        
                        elif stepspoints>=4000:
                            badges.append("No promotion")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniorservant.jpeg")
                            next_badge_requirement="You and your %s need to use the application for at least 4 days since day one to get to 'Junior Master' badge. You have used the application for only %s days"%(beneficiary_relations[posn],clickpoints)

                        else:
                            badges.append("No promotion")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniorservant.jpeg")
                            next_badge_requirement="Your %s needs to walk an average of 4000 steps per day to attain 'Junior Master' badge. The average number of steps is currently at %s steps per day"%(beneficiary_relations[posn],stepspoints)
                         
                    elif currentbadge==9:
                        if stepspoints>=3000 and clickpoints>=2:
                            badges.append("Senior Servant")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniorservant.jpeg")

                        elif stepspoints>=3000:
                            badges.append("No promotion") 
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/servant.jpeg")
                            next_badge_requirement="You and your %s need to use the application for at least 2 days since day one to get to 'Senior Servant' badge. You have used the application for only %s day"%(beneficiary_relations[posn],clickpoints)
                          
                        else:
                            badges.append("No promotion") 
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/servant.jpeg")
                            next_badge_requirement="Your %s needs to walk an average of 3000 steps per day to attain 'Senior Servant' badge. The average number of steps is currently at %s steps per day"%(beneficiary_relations[posn],stepspoints)
                         
                    elif currentbadge==10:
                      
                        if stepspoints>=2500 and clickpoints>=1:
                            badges.append("Servant")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/servant.jpeg")
                        elif stepspoints>=2500:
                            badges.append("No promotion")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/slave.jpeg")
                            next_badge_requirement="You and your %s need to use the application for at least 1 day to get to 'Servant' badge. You have used the application for only %s days"%(beneficiary_relations[posn],clickpoints)
                  
                        else:
                            badges.append("No promotion")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/slave.jpeg")
                            next_badge_requirement="Your %s needs to walk an average of 2500 steps per day to attain 'Servant' badge. The average number of steps is currently at %s steps per day"%(beneficiary_relations[posn],stepspoints)

                    else:
                        print "I am also a slave"        
                        badges.append("Slave")
                        
                        badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/slave.jpeg")
                        next_badge_requirement="Your next challenge is achieve 'Servant' badge"
                    #print "currentbadge=%s and req=%s"%(currentbadge,next_badge_requirement)
                    #posn=posn+1
                    #continue 
                    try:
  
                        
                        #get the rank of the badge
                        message_bank=[]
                        message_counter=0
                        first_name=intermediary_names[posn][0:(intermediary_names[posn].index(' ')+1)] # 
                        print "Badges position =", badges[posn]
                        if badges[posn] == "No promotion":
                            print "No promotion"
                            next_rank=currentbadge-1
                            print "currentbadge",currentbadge
                            if next_rank>=0:
                                res=session.query(Badges).filter(Badges.rank==next_rank).first()
                                if res ==None:
                                    next_badge_name="Complete"
                                else:
                                    
                                    next_badge_name=res.badgename #next badge name
                                   
                            else:
                                pass

                            if next_badge_name=="Complete":
                                pass
                            else:
                                feedback_message="Hi %s "%first_name
                                feedback_message=feedback_message+" The challenge ahead for your team is to achieve '%s' badge."%next_badge_name
                                message_bank.append(feedback_message)
                                message_counter=message_counter+1

                                feedback_message="Hello %s "%first_name
                                feedback_message=feedback_message+" You and your %s need to work harder to progress to higher badges. The next challenge is to achieve '%s' badge that you can use to buy fertilizer for trees in your garden. "%(beneficiary_relations[posn],next_badge_name)
                                message_bank.append(feedback_message)
                                message_counter=message_counter+1

                                feedback_message="Hey %s "%first_name
                                feedback_message=feedback_message+" You and your %s can work together to conquer the next challenge which is to achieve '%s' badge. Login to the app to see the state of your garden and aquarium. "%(beneficiary_relations[posn],next_badge_name)
                                message_bank.append(feedback_message)
                                message_counter=message_counter+1

                                if next_badge_requirement=="":
                                    num=randint(0,message_counter-1)
                                else:    
                                    feedback_message="Hey %s "%first_name
                                    feedback_message=feedback_message+next_badge_requirement
                                    message_bank.append(feedback_message)
                                    message_counter=message_counter+1
                                    num=message_counter-1 #assign the last message
                               # num=randint(0,message_counter-1)
                                
                               
                                #Schedule feedback
                                myjson2={"recipient":intermediary_mobiles[posn],"message":message_bank[num]}
                                                               
                                obj=QueueFeedback(myjson2)
                                res=obj.saveFeedbackInDB()
                                print message_bank[num]
                                


                        else:
                            print "Got here it means there is promotion"
                            #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
                            engine=db
                            # create a Session
                            Session = sessionmaker(bind=engine)
                            session = Session()
                            #get the new badge name
                            res=session.query(Badges).filter(Badges.badgename==badges[posn]).first()
                            
                            if res ==None:
                                rank=0
                            else:
                                
                                rank=res.rank #new acquired rank

                            next_rank=rank-1;
                            if next_rank>=0:
                                #now check what is the next challenge for this team
                                res=session.query(Badges).filter(Badges.rank==next_rank).first()
                                if res ==None:
                                    next_badge_nam="Complete"
                                else:
                                    next_badge_name=res.badgename #next badge name
                               

                                   
                            else:
                                next_badge_name=None

                            
                           
                           
   


                              

                           
                            #new_attained_badge
                            #first get the current badge of this
                            #Get the current badge
                            res=session.query(AttainedUserBadges).filter(AttainedUserBadges.intermediary_id==orig_email).filter(AttainedUserBadges.status==1).first()
               
                            if res is None:
                            #No badge has been assigned before
                              #first promotion 
                                #insert a new badge into the database
                                new_attained_badge=AttainedUserBadges(orig_email,datetime.date.today(),rank)
                                session.add(new_attained_badge)
                                session.commit()# Commit this transaction
                                first_name=intermediary_names[posn][0:(intermediary_names[posn].index(' ')+1)] #
                                print "First Promotion"
                                if next_badge_name=="Complete":
                                    pass
                                else:
                                    feedback_message="Hi %s "%first_name
                                    feedback_message=feedback_message+" your team's first badge is %s . You and your %s need to work harder to progress to higher badges. The next challenge is to achieve '%s' badge."%(badges[posn],beneficiary_relations[posn],next_badge_name)
                                    message_bank.append(feedback_message)
                                    message_counter=message_counter+1


                                 
             

                           
                                feedback_message="Hey %s "%first_name
                                feedback_message=feedback_message+"your team's first badge is %s . You and your %s need to work harder to progress to higher badges. Higher badges can give more points to buy fertilizer for tree in your garden "%(badges[posn],beneficiary_relations[posn])
                                message_bank.append(feedback_message)
                                message_counter=message_counter+1


                                feedback_message="Hallo %s "%first_name
                                feedback_message=feedback_message+"your team's first badge is %s . You and your %s need to work harder to progress to higher badges. You can only obtain higher badges if you keep on using the app everyday and motivate your %s to walk more steps everyday."%(badges[posn],beneficiary_relations[posn],beneficiary_relations[posn])
                                message_bank.append(feedback_message)
                                message_counter=message_counter+1


                                feedback_message="Whatsap %s "%first_name
                                feedback_message=feedback_message+"!!. Your team's first badge is %s . Encourage your %s to walk more steps and keep on using the app everyday. If you get a Queen or King Badge you will have enough points to buy more fish for your aquarium."%(badges[posn],beneficiary_relations[posn])
                                message_bank.append(feedback_message)
                                message_counter=message_counter+1

                                num=randint(0,message_counter-1)
                    
                                #Feedback Schedule
                                myjson2={"recipient":intermediary_mobiles[posn],"message":message_bank[num]}
                                
                                obj=QueueFeedback(myjson2)
                                res=obj.saveFeedbackInDB()
                            
                            else:
                               # This person already had an existing badge 
                                
                              #check if new badge rank is less than the existing badge rank
                              #The highest badge must have the small rank
                                if rank<res.badge_id:
                                    print "I am here the old badge is obsolete as as shown old=%s,new=%s, next=%s"%(old_badge,badges[posn],next_badge_name)
                                    print "And the ranks for new is %s and for old is %s"%(rank,res.badge_id)
                                 #promote to new higher badge
                                    if next_badge_name=="Complete":
                                        feedback_message="Congratulations!! %s "%first_name
                                        feedback_message=feedback_message+" your team has been promoted to 'Queen/King' badge.This is the highest badge."
                                        message_bank.append(feedback_message)
                                        message_counter=message_counter+1
                                    else:
                                        feedback_message="Welldone %s "%first_name
                                        feedback_message=feedback_message+" your team has been promoted to a new badge.Your old badge was %s and your new badge is %s . The next challenge is to achieve '%s' badge."%(old_badge,badges[posn],next_badge_name)
                                        message_bank.append(feedback_message)
                                        message_counter=message_counter+1
                                    #Feedback schedule
                                    res.status=0# make the current badge obsolete
                                    session.commit()

                                    session = Session()#create a new session
                                    
                                    #insert a new badge into the database
                                    #Feedback message

                                    new_attained_badge=AttainedUserBadges(orig_email,datetime.date.today(),rank)
                                    session.add(new_attained_badge)
                                    session.commit()# Commit this transaction
                                    print "Promoted to new rank"
                                    feedback_message="Hey %s "%first_name
                                    
                                    feedback_message=feedback_message+"your team has been promoted to a new badge. Your old badge was %s and now your new badge is %s. Keep on using your app every day and keep on motivating your %s to walk more steps so that your team can continue to shine."%(old_badge,badges[posn],beneficiary_relations[posn])
                                    message_bank.append(feedback_message)
                                    message_counter=message_counter+1


                                    feedback_message="Hallo %s "%first_name
                                    
                                    feedback_message=feedback_message+"your team has been promoted to a new badge. Your old badge was %s and now your new badge is %s. This new badge gives you a change to buy one more fish type for your aquarium"%(old_badge,badges[posn])
                                    message_bank.append(feedback_message)
                                    message_counter=message_counter+1

                                    feedback_message="Hi %s "%first_name
                                    
                                    feedback_message=feedback_message+"your team has been promoted to a new badge. Your old badge was %s and now your new badge is %s. With this new badge you will be awarded points to buy fertilizer for your trees in your garden."%(old_badge,badges[posn])
                                    message_bank.append(feedback_message)
                                    message_counter=message_counter+1

                                    num=randint(0, message_counter-1)

                                    teams_promoted.append(first_name)
                                    new_badges.append(badges[posn])                                     
                                    #Feedback message
                                    myjson2={"recipient":intermediary_mobiles[posn],"message":message_bank[num]}
                                    obj=QueueFeedback(myjson2)
                                    res=obj.saveFeedbackInDB()
                                  
                                
                                else:
                                    print "No new promotion"
                                    engine=db
                            # create a Session
                                    Session = sessionmaker(bind=engine)
                                    session = Session()
                                    res=session.query(Badges,AttainedUserBadges).filter(Badges.rank==currentbadge).filter(Badges.rank==AttainedUserBadges.badge_id).filter(AttainedUserBadges.status==1).first()

                                    if res ==None:
                                        rank=0
                                    else:

                                        rank=currentbadge #new acquired rank

                                    next_rank=rank-1;
                                    if next_rank>=0:
                                        res=session.query(Badges).filter(Badges.rank==next_rank).first()
                                        if res ==None:
                                            next_badge_name="Complete"
                                        else:
                                            next_badge_name=res.badgename #next badge name



                                    else:
                                        next_badge_name=None
                                    feedback_message="Hi %s "%first_name
                                    feedback_message=feedback_message+" The challenge ahead for your team is to achieve '%s' badge."%next_badge_name
                                    message_bank.append(feedback_message)
                                    message_counter=message_counter+1

                                    feedback_message="Hello %s "%first_name
                                    feedback_message=feedback_message+" You and your %s need to work harder to progress to higher badges. The next challenge is to achieve '%s' badge that you can use to buy fertilizer for trees in your garden. "%(beneficiary_relations[posn],next_badge_name)
                                    message_bank.append(feedback_message)
                                    message_counter=message_counter+1

                                    feedback_message="Hey %s "%first_name
                                    feedback_message=feedback_message+" You and your %s can work together to conquer the next challenge which is to achieve '%s' badge. Login to the app to see the state of your garden and aquarium. "%(beneficiary_relations[posn],next_badge_name)
                                    message_bank.append(feedback_message)
                                    message_counter=message_counter+1


                                    num=randint(0, message_counter-1)

                    
                                    print message_bank[num]
                                    print num
                                    #Feedback message
                                    myjson2={"recipient":intermediary_mobiles[posn],"message":message_bank[num]}
                                    obj=QueueFeedback(myjson2)
                                    res=obj.saveFeedbackInDB()
                                    
                        
              
                      
                        
                        
                    except Exception as e:
                        print "Exception thrown: %s"%e
                        return -1
                        
                    
                        
  
                   
                    posn=posn+1


            
            team_iter=0
            #progress_message="Congratulations to these people for being promoted to new badges:"  
            teams_and_badges=""
            for team in teams_promoted:
                print team,new_badges[team_iter]
                if team_iter>0:
                    teams_and_badges="%s, "%teams_and_badges
                teams_and_badges="%s%s:%s"%(teams_and_badges,team,new_badges[team_iter])
                team_iter=team_iter+1
            if team_iter>1:
                progress_message="Congratulations to these people for being promoted to new badges today:%s. [Auto-generated Message]"%teams_and_badges
            else:
                progress_message="Congratulation to this person for being the only one to get a new badge today:%s. [Auto-generated Message]"%teams_and_badges

#now send a message to every one about new badges      
            if team_iter>0: #it means we have new promotion
                print "\n"
                for mobile in intermediary_mobiles:
                    #Feedback message
                    print mobile,progress_message
                    myjson2={"recipient":mobile,"message":progress_message}
                    obj=QueueFeedback(myjson2)
                    res=obj.saveFeedbackInDB() 

        except Exception as e:
            print "Exception thrown %s "%e
            return -1
              
                
                  
        return 1   
#team_iter=0
#progress_message="Congratulations to these people for being promoted to new badges:"  
#teams_and_badges=""    
#for team in teams_promoted:
#        print team,new_badges[team_iter] 
#        if team_iter>0:
#            teams_and_badges="%s ,"%teams_and_badges
#        teams_and_badges="%s%s:%s"%(teams_and_badges,team,new_badges[team_iter])
#        team_iter=team_iter+1
#if team_iter>1:
#        progress_message="Congratulations to these people for being promoted to new badges:%s. [Auto-generated Message]"%teams_and_badges
#else:
#        progress_message="Congratulation to this person for being the only one to get a new badge today:%s. [Auto-generated Message]"%teams_and_badges

#now send a message to every one about new badges      
#if team_iter>0: #it means we have new promotion
#        print "\n"
#        for mobile in intermediary_mobiles:
            #Feedback message
#            print mobile,progress_message
            #myjson2={"recipient":mobile,"message":progress_message}
            #obj=QueueFeedback(myjson2)
            #res=obj.saveFeedbackInDB()    
 


              
     
     
     


score_date=datetime.date.today()-datetime.timedelta(days=1)
score_date_str="%s"%score_date.strftime("%d/%m/%Y")
score_date_str2="%s"%score_date.strftime("%Y-%m-%d")


myjson={'Day':score_date_str2}
obj=RetrievePoints(myjson,'katulentwa@gmail.com',1)
result=obj.assignBadges()

if result==1:
    print "The badge assignment completed successfully"
else:
    print "Badge assignment failed to complete"

