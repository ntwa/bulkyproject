#!/usr/bin/env python
import datetime,calendar
import sys,json
from sqlalchemy import create_engine,distinct,func,asc
from sqlalchemy.orm import sessionmaker
from wellness.applogic.points_module import Points,db
from retrieve_sound import RetrieveSound
from retrieve_intermediary import RetrieveIntermediary,Beneficiary
from collections import OrderedDict
from save_factors import ManageFactors
import os
from wellness.applogic.activity_module import PhysicalActivity
from random import randint
from wellness.applogic.pilot_start import PilotCommencement
from wellness.applogic.food_beverage_module import FoodAndBeverage,Meal,MealComposition,db,dbconn
from wellness.applogic.badges_module import Badges,AttainedUserBadges
from save_comment import SaveComment
from plot_meal_graph import PlotMealGraph
from manage_avatars import ManageAvatars
import os.path

#def bubblesort(A,X,Y,Z,U,V,W,L,M,B,C,Q,R):
def bubblesort(A):  
  for i in range( len( A ) ):
    for k in range( len( A ) - 1, i, -1 ):
      if ( A[k].total_plants> A[k - 1].total_plants):
        swap( A, k, k - 1 )
      elif ((A[k].total_plants== A[k - 1].total_plants) and (A[k].total_points>A[k - 1].total_points)):
        swap( A, k, k - 1 )




  return A
 
def swap( A, x, y ):
  tmp = A[x]
  A[x] = A[y]
  A[y] = tmp


class TeamFeatures:

  def __init__(self,team_name,team_members,url,trees,flowers,total_plants,usage_points,bonus_points,badge,badge_url,beneficiary_id,fishnum,fishsize,aquariumcomments,gardencomments,total_points,avatarurl,complete_garden_path,plantsize):

    self.team_name=team_name
    self.team_members=team_members
    self.url=url
    self.trees=trees
    self.flowers=flowers
    self.total_plants=total_plants
    self.usage_points=usage_points
    self.bonus_points=bonus_points
    self.badge=badge
    self.badge_url=badge_url
    self.beneficiary_id=beneficiary_id
    self.fishnum=fishnum
    self.fishsize=fishsize
    self.aquariumcomments=aquariumcomments
    self.gardencomments=gardencomments
    self.total_points=total_points
    self.avatarurl=avatarurl
    self.complete_garden_path=complete_garden_path
    self.plantsize=plantsize

    

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


    def getSteps(self,beneficiary_id):
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


    def getCurrentRank(self):
      result={}
      try:

        engine=db
        #create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        '''
        if self.last_date_specified==1:
            day=self.myjson["Day"]
            if day != "Today":

              day=datetime.date.today()
                #res2=session.query(AttainedUserBadges,Badges).filter(AttainedUserBadges.intermediary_id==self.intermediary_id).filter(AttainedUserBadges.status!=1).filter(AttainedUserBadges.badge_id==Badges.rank).filter(AttainedUserBadges.dateattained<=day).filter(func.max(AttainedUserBadges.badge_id)==Badges.rank).first()
              res2=session.query(func.min(AttainedUserBadges.badge_id).label("max_badge")).filter(AttainedUserBadges.intermediary_id==self.intermediary_id).filter(AttainedUserBadges.dateattained<=day).first()
              if res2 is None:
                result["Rank"]=11
                result["Message"]="Badge position retrieved successfully"
                return (json.JSONEncoder().encode(result))
              else:
                max_badge=res2.max_badge
                result["Rank"]=max_badge
                result["Message"]="Badge position retrieved successfully"
                return (json.JSONEncoder().encode(result))
                #res2=session.query(AttainedUserBadges,Badges).filter(AttainedUserBadges.intermediary_id==self.intermediary_id).filter(AttainedUserBadges.status!=1).filter(AttainedUserBadges.badge_id==Badges.rank).filter(AttainedUserBadges.dateattained<=day).filter(func.max(AttainedUserBadges.badge_id)==Badges.rank).first()
            #else:
            #  res2=session.query(AttainedUserBadges,Badges).filter(AttainedUserBadges.intermediary_id==self.intermediary_id).filter(AttainedUserBadges.status==1).filter(AttainedUserBadges.badge_id==Badges.rank).first()
        
        #else:
        '''
        res2=session.query(AttainedUserBadges,Badges).filter(AttainedUserBadges.intermediary_id==self.intermediary_id).filter(AttainedUserBadges.status==1).filter(AttainedUserBadges.badge_id==Badges.rank).first()
        
        if res2 is None:
          rank=11# means there is no badge
        else:
          attainedrec,existingbadges=res2
          rank=existingbadges.rank

        result["Rank"]=rank
        result["Message"]="Badge position retrieved successfully"

      except Exception as e:
        print "Exception thrown: %s"%e
        result["Rank"]=-1
        result["Message"]=e
      print "Rank=",rank
      return (json.JSONEncoder().encode(result))

    def countRecordedMeals(self,beneficiary_id):
      result={}

      try:
        
        engine=db
        #create a Session
        Session = sessionmaker(bind=engine)
        session = Session()
        res = session.query(func.count(FoodAndBeverage.id).label("mealscounter")).filter(FoodAndBeverage.beneficiary_id==beneficiary_id).first()
        if res.mealscounter is None:
          awarded_points=0;
        else:
          awarded_points=res.mealscounter



        result["NumberOfMeals"]=awarded_points
        result["Message"]="Meals count obtained successfully"


      except Exception as e:
        result["NumberOfMeals"]=-1
        result["Message"]=e

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
                                


            #res=session.query(func.count(distinct(Points.datecaptured)).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).first()

            if self.last_date_specified==1:
                day=self.myjson["Day"]
                if day=="Today":
                   day=datetime.date.today()
                
                #res=session.query(func.count((Points.datecaptured)).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured<=day).first() 
                res=session.query(func.count((Points.datecaptured)).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured<=day).first()   
                 #res= session.query(func.sum(Points.scoredpoints).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured<=day).first()
            #get points by number of days an application has been used.
            #res=session.query(func.count(distinct(Points.datecaptured)).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured<=day).first()
            else:
                #res= session.query(func.sum(Points.scoredpoints).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).first()
                res=session.query(func.count((Points.datecaptured)).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).first()

            

            
            
            retrieved_points_sum=0# initialize how many distinct dates are in the database
                      
            
            
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



    def assignUrl(self,rank):
      
      if rank==1:

        badges_urls="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/queen.jpeg"
      elif rank==2:
        badges_urls="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/princess.jpeg"
  
      elif rank==3:
         
        badges_urls="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/duchess.jpeg"
             
      elif rank==4:
        badges_urls="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/grandmaster.jpeg"
                
      elif rank==5:
        badges_urls="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniormaster.jpeg"

      elif rank==6:            
        badges_urls="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/master.jpeg"

      elif rank==7:
        badges_urls="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/juniormaster.jpeg"
  
      elif rank==8:
        badges_urls="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniorservant.jpeg"

      elif rank==9:
        badges_urls="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/servant.jpeg"

      elif rank==10:
        badges_urls="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/slave.jpeg"

      else:
        badges_urls="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/default.jpeg"
      return badges_urls
              
    def retrieveIndividualBadge(self):
         
         #print "Got here==RIB",self.intermediary_id
         result={}

         try:

              num=randint(2,49)
              obj=RetrieveSound(num)
              res=obj.retrieveSoundUrl()
              res=json.loads(res)
                
              sound_url=res["url"]  


              engine=db

              #create a Session
              Session = sessionmaker(bind=engine)
              session = Session()


              day="Not specified"
              if self.last_date_specified==1:

                day=self.myjson["Day"]

                if day != "Today":
        
                  #res2=session.query(AttainedUserBadges,Badges).filter(AttainedUserBadges.intermediary_id==self.intermediary_id).filter(AttainedUserBadges.status!=1).filter(AttainedUserBadges.badge_id==Badges.rank).filter(AttainedUserBadges.dateattained<=day).filter(func.max(AttainedUserBadges.badge_id)==Badges.rank).first()
                  res2=session.query(func.min(AttainedUserBadges.badge_id).label("max_badge")).filter(AttainedUserBadges.intermediary_id==self.intermediary_id).filter(AttainedUserBadges.date_attained<=day).first()
                  #print res2.max_badge,self.intermediary_id
                  if res2.max_badge is None:
                    #result["Rank"]=11
                    rank=11
                    badge="No badge"
                    badges_urls="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/default.jpeg"
                    result["R00"]={"D0":"Badge Acquired","D1":badges_urls,"D2":sound_url,"D3":badge,"D4":rank}
                    
                    return (json.JSONEncoder().encode(result))
                
                  else:
                    max_badge=res2.max_badge
                    badges_urls=self.assignUrl(max_badge)
                    res2=session.query(Badges).filter(Badges.rank==max_badge).first()
                    badge=res2.badgename

                    result["R00"]={"D0":"Badge Acquired","D1":badges_urls,"D2":sound_url,"D3":badge,"D4":max_badge}
                    result["Message"]="Badge position retrieved successfully"
                    print  result["R00"]
                    return (json.JSONEncoder().encode(result))


                           
              varmyjson={'Day':"Today"}
              myjson={'Fname':'Dummy','Lname':'Dummy','Username':self.intermediary_id}
              obj=RetrieveIntermediary(myjson)
              res=obj.isAssignedBeneficiary()

              beneficiary_tuple=json.loads(res)
              b_id=beneficiary_tuple["Id"]
              print "Got here"
              if b_id==None :
                  b_id=0
                  #raise ValueError('This individual is not assigned a beneficiary')
      
        
              #print "Got here!!==RIB",self.intermediary_id 
                
              badges_urls=[]



              res2=session.query(AttainedUserBadges,Badges).filter(AttainedUserBadges.intermediary_id==self.intermediary_id).filter(AttainedUserBadges.status==1).filter(AttainedUserBadges.badge_id==Badges.rank).first()
              
              if res2 is None:
                rank=11
                badge="No Badge"
              else:
                attainedres,badgeres=res2
                rank=badgeres.rank#get the current rank
                badge=badgeres.badgename


        
              
              badges_urls=self.assignUrl(rank)

                       
           
              result={"R00":{"D0":"Badge Acquired","D1":badges_urls,"D2":sound_url,"D3":badge,"D4":rank}}

              
              

         except Exception as e:
              print e
              message="An exception was thrown in function retrieveIndividualScore(): %s"%e
              result={"R00":{"D0":message,"D1":"http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/default.jpeg","D2":"Error","D3":e,"D4":11}}


         
         return (json.JSONEncoder().encode(result))



    def getUpdatedAquariumComments(self):
      result={}

      try:
        teamname=self.myjson["TeamName"]
        #teamname="Cameroon"
      except Exception as e:
        result["P00"]={"Q0":-1,"Q1":"No Comment","Q2":e}
        return (json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))


      try:

        engine=db
        #create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        #get an intermediary id based on team name

        res=session.query(Beneficiary).filter(Beneficiary.team_name==teamname).first()
        
        if res is None:
          result["P00"]={"Q0":-1,"Q1":"No Comment","Q2":-1}
          return (json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))
        else:
          intermediary_id=res.intermediary_id
          beneficiary_id=res.id

        
        myjson={}
        obj=SaveComment(myjson,beneficiary_id,intermediary_id)# interme
              
        res=obj.getComments("Aquarium")

        aquariumcomments=json.loads(res)
        

        return (json.JSONEncoder().encode(OrderedDict(sorted(aquariumcomments.items(), key=lambda t: t[0]))))




      except Exception as e:

        result["P00"]={"Q0":-1,"Q1":"No Comment","Q2":e}
        return (json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))



    def getUpdatedGardenComments(self):
      result={}

      try:
        teamname=self.myjson["TeamName"]
        #teamname="Cameroon"
      except Exception as e:
        result["P00"]={"Q0":-1,"Q1":"No Comment","Q2":e}
        return (json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))


      try:

        engine=db
        #create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        #get an intermediary id based on team name

        res=session.query(Beneficiary).filter(Beneficiary.team_name==teamname).first()

        if res is None:
          result["P00"]={"Q0":-1,"Q1":"No Comment","Q2":-1}
          return (json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))
        else:
          intermediary_id=res.intermediary_id
          beneficiary_id=res.id


        myjson={}
        obj=SaveComment(myjson,beneficiary_id,intermediary_id)# interme

        res=obj.getComments("Garden")

        gardencomments=json.loads(res)


        return (json.JSONEncoder().encode(OrderedDict(sorted(gardencomments.items(), key=lambda t: t[0]))))




      except Exception as e:

        result["P00"]={"Q0":-1,"Q1":"No Comment","Q2":e}
        return (json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))

    #get all messages posted in the board
    def getUpdatedComments(self):
      result={}


      try:

        
        intermediary_id=None
        beneficiary_id=None


        myjson={}
        obj=SaveComment(myjson,beneficiary_id,intermediary_id)# interme

        res=obj.getComments("ChatRoom")

        chatroomcomments=json.loads(res)


        return (json.JSONEncoder().encode(OrderedDict(sorted(chatroomcomments.items(), key=lambda t: t[0]))))




      except Exception as e:

        result["P00"]={"Q0":-1,"Q1":"No Comment","Q2":e}
        return (json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))





    def retrieveScoreGardensUrls(self):
        result={}
        try:
            
             day=self.myjson["Day"]
                                 
        except Exception as e:
             #print "Content-type: text/html\n" 
             result["message"]="Error%s"%e.message
             return (json.JSONEncoder().encode(result))

        
        if day is not None:
            if day=="Today":
                today_date=datetime.date.today()
                date_str="%s"%today_date 
            else:
                date_str="%s"%day
        else:
             result["message"]="Error: The option '%s' is invalid"%day
             return (json.JSONEncoder().encode(result))
             
             
             
        
        
        myjson={'Fname':'Dummy','Lname':'Dummy','Username':'dummy'}
        obj=RetrieveIntermediary(myjson)
        res=obj.retrieveIntermediaryInDB()
        
        intermediaries_tuple=json.loads(res)
        intermediaries_emails=""
        intermediary_names=""
        #orig_emails=[]
        beneficiary_id=0
        beneficiary_names=""
        posn=0
        gardens=[]
        competitors_counter=0
        
        garden_label=date_str.replace("-","_")   
        first_posn=0
        second_posn=0

        key2="D"    
        trees=0
        flowers=0
        fishnum=0
        fish_size=0.0
        total_plants=""
        url=""
        usage_points=""
        bonus_points=""
        badge=""
        badge_url=""
        team_members=""
      
        team_name=""
        team_features=[]
        for record in intermediaries_tuple.items():
             
             
             key,user =record
            
             if(user["D2"]=="None"):
                 continue
             else:
                  
                 
                  #orig_emails.append(user["D1"]) #keep original email addresses
                  orig_email=user["D1"]
             
                  user["D1"]=user["D1"].replace("@","_at_")
                  user["D1"]=user["D1"].replace(".","_dot_")
                  
                  intermediary_email=user["D1"]
                  intermediary_names=user["D0"]
                  beneficiary_names=user["D2"][0:user["D2"].index('.')]# get the name only
                  myjson={'Fname':'Dummy','Lname':'Dummy','Username':orig_email}
                  obj=RetrieveIntermediary(myjson)
                  result2=obj.isAssignedBeneficiary()
                   
                  beneficiary_tuple=json.loads(result2)
                  usergroupres=obj.getUserGroup()
                  usergroupres=json.loads(usergroupres)
                  usergroup=usergroupres["Group"]                 
                  if usergroup == 1:
                      continue
                  team_identifier="%s_%s"%(beneficiary_tuple["Id"],garden_label)
                  beneficiary_id=team_identifier  #Beneficiary 

                
                  file_path="django_facebook/images/garden/%s/%s_%s.jpeg"%(intermediary_email,beneficiary_tuple["Id"],garden_label)
                  
                  #file_name="%s_%s"%(beneficiary_id,garden_label)
                  url=file_path # url
                  complete_path="/var/www/apps/static/%s"%url







                  
                  team_name=beneficiary_tuple["TeamName"] # Team Name
                  
                  one_team_members="(%s, %s)"%(intermediary_names,beneficiary_names) # put together team members
            


                  team_members=one_team_members  #Team Members
                 
                
                   
                  varmyjson={'Day':day}
		  
                                   
                  clickPointsObj=RetrievePoints(varmyjson,orig_email,self.last_date_specified)
                  resclickpoints=clickPointsObj.retrieveIntermediaryClickPoints()
                  resclickpoints=json.loads(resclickpoints)
                  
                  clickpoints=int(resclickpoints["points"])
                  
                  clickpoints=clickpoints*1000

                
                   
                  usage_points=clickpoints  #Usage Points
                  
                  ressteps=clickPointsObj.getSteps(beneficiary_tuple["Id"])
                  ressteps=json.loads(ressteps)
                   

                  stepspoints=int(ressteps["steps"]/ressteps["dates_counter"])
                 
                  
                  
                  bonus_points=stepspoints  #Bonus points

                  total_points=usage_points+bonus_points
                  
                     
                  
                  resbadge=clickPointsObj.retrieveIndividualBadge()
                  resbadge=json.loads(resbadge)
                  
                  #get badge name for this individual
                  badge=resbadge["R00"]["D3"] #Badge

                  #get a badge url for this person
                  badge_url=resbadge["R00"]["D1"] #Badge URL

                                    

                  trees=int(10*(11-resbadge["R00"]["D4"])) # the number of trees in a garden
                  fishnum=int(11-resbadge["R00"]["D4"]) # the number of fish in a tank


                  #fishsize=float(float(fishnum)/float(10)) # fish size is determined by how many fish are in the tank. The more fish the bigger the size. This weill also be used to detrmine the quality of a fish tank
                  
                  myjson={"Day":"All"}
                  obj=PlotMealGraph(myjson,beneficiary_tuple["Id"])
                  res=obj.getMealsRatioFactor()  
                  res=json.loads(res)

                  fishsize=float(res["D0"]) # fish size is determined by the number of meals recorded relatively to the highest number of meal recorded and ratio of fruits and Veges vs the largest portion of fruits and veges
                  #print "Badge=%s"%(11-resbadge["R00"]["D4"])
                  plantsize=float(float(11-resbadge["R00"]["D4"])/10.0)
                  #print plantsize

                  resmealcounter=self.countRecordedMeals(beneficiary_tuple["Id"])
                  resmealcounter=json.loads(resmealcounter)

                  flowers=(10*resmealcounter["NumberOfMeals"]) # number of flowers in the garden

                  
                  #print file_name,trees, flowers
             
                  #total=trees+flowers
                  
                  #total_plants=fishnum*10 # these are the total points
                  #total_plants=int(total_plants*fishsize)
                  total_plants=(trees+flowers)
                  
                  total_plants=int(total_plants*plantsize)
                   

                  obj=SaveComment(myjson,beneficiary_tuple["Id"],orig_email)
              
                  res=obj.getComments("Aquarium")

                  aquariumcomments=json.loads(res)

                 
                  res=obj.getComments("Garden")

                  gardencomments=json.loads(res)


                  #newaquariumcomments=json.loads(newaquariumcomments)
                  avatarmyjson={"IntermediaryId":orig_email}
                  avatarobj=ManageAvatars(avatarmyjson)
                  res=avatarobj.getAvatarUrl()
                  avatardata=json.loads(res)
                  avatarurl=avatardata["AvatarUrl"]
                    
                

              
                  #res=obj.getComments("Garden")

                  #gardencomments=json.loads(res)


                  one_team_features=TeamFeatures(team_name,team_members,url,trees,flowers,total_plants,usage_points,bonus_points,badge,badge_url,beneficiary_tuple["Id"],fishnum,fishsize,aquariumcomments,gardencomments,total_points,avatarurl,complete_path,plantsize)
                  team_features.append(one_team_features)


                  posn=posn+1
                  
        posn=0      
      
    
           
        #bubblesort(total_plants,team_name,team_members,urls,beneficiary_ids,tree_array,flower_array,usage_points,bonus_points,badges,badges_urls,fish_array,fish_size_array)
        bubblesort(team_features)
        posn=0
        file_path_alt="django_facebook/images/garden/blank.jpg"
        for one_team in team_features:
            urls_tuple={}
            if first_posn<10:
              key1="R0"
            else:
              key1="R"     
              
            urls_tuple[key2+"%s"%second_posn]="%s"%one_team.team_name # D0 team name
            second_posn=second_posn+1  

            urls_tuple[key2+"%s"%second_posn]="%s"%one_team.team_members # D1 team members
            second_posn=second_posn+1 
            
            urls_tuple[key2+"%s"%second_posn]=one_team.url #D2 url for garden
            if os.path.isfile(one_team.complete_garden_path):
              pass
            else: #if the garden doesn't exist put a blank
            #if one_team.total_plants==0:
              urls_tuple[key2+"%s"%second_posn]=file_path_alt
              print "Garden for %s doesn't exist"%one_team.team_members
              
            second_posn=second_posn+1
            
            

            urls_tuple[key2+"%s"%second_posn]="%s"%one_team.trees  #D3 Number of trees
            second_posn=second_posn+1
            
            urls_tuple[key2+"%s"%second_posn]="%s"%one_team.flowers  # D4 Number of flowers
            second_posn=second_posn+1
            
            urls_tuple[key2+"%s"%second_posn]="%s"%one_team.total_plants  #D5 Total number of plants including flowers and tree
            second_posn=second_posn+1
            

            urls_tuple[key2+"%s"%second_posn]="%s"%one_team.usage_points #D6 Number of days an application has been used multiply by 1000 by a team. 
            second_posn=second_posn+1
 
 
            urls_tuple[key2+"%s"%second_posn]="%s"%one_team.bonus_points  #D7 average steps walked by an individual
            second_posn=second_posn+1

            urls_tuple[key2+"%s"%second_posn]="%s"%one_team.badge #D8 Badge name
            second_posn=second_posn+1
            
            urls_tuple[key2+"%s"%second_posn]="%s"%one_team.badge_url #D9 Badge Url
            second_posn=second_posn+1


            urls_tuple[key2+"%s"%second_posn]="%s"%one_team.beneficiary_id  #D10 Beneficiary ID
            second_posn=second_posn+1



            urls_tuple[key2+"%s"%second_posn]="%s"%one_team.fishnum # D11 Number of fish in the tank.
            second_posn=second_posn+1


            urls_tuple[key2+"%s"%second_posn]="%s"%one_team.fishsize #D12 size of fish in the tank
            second_posn=second_posn+1




            urls_tuple[key2+"%s"%second_posn]=OrderedDict(sorted(one_team.aquariumcomments.items(), key=lambda t: t[0])) #D13 Aquarium comments
            second_posn=second_posn+1
            

            urls_tuple[key2+"%s"%second_posn]=OrderedDict(sorted(one_team.gardencomments.items(), key=lambda t: t[0])) #D14 Garden comments
            second_posn=second_posn+1


            urls_tuple[key2+"%s"%second_posn]="%s"%one_team.total_points #D15 Total points
            second_posn=second_posn+1


            urls_tuple[key2+"%s"%second_posn]="%s"%one_team.avatarurl #D16 Avatar
            second_posn=second_posn+1  


            urls_tuple[key2+"%s"%second_posn]="%s"%one_team.plantsize #D17 Plant Size
            second_posn=second_posn+1            

            
            second_posn=0
            result[key1+"%s"%first_posn]=(OrderedDict(sorted(urls_tuple.items(), key=lambda t: t[0])))
            first_posn=first_posn+1
            posn=posn+1
        
             
        return (json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))
         

              
  

myjson={"Day":"Today"} 
obj=RetrievePoints(myjson,'tumie',1)
#result=obj.retrieveIndividualBadge()
result=obj.retrieveScoreGardensUrls()
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
