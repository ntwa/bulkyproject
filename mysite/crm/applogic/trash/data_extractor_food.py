#!/usr/bin/env python
import datetime,calendar
from datetime import timedelta
import sys,json
from sqlalchemy import create_engine,distinct,func,asc
from sqlalchemy.orm import sessionmaker
from wellness.applogic.food_beverage_module import FoodAndBeverage,db,dbconn
from wellness.applogic.intermediary_module import Intermediary,Beneficiary
import os.path

    

class RetrieveLogData:
    def __init__(self):
        pass

    def getMealsRecorded(self,demarcation_date_str,demarcation_date_str0):
        

        demarcation_date=datetime.datetime.strptime(demarcation_date_str,'%Y-%m-%d').date()
        demarcation_date0=datetime.datetime.strptime(demarcation_date_str0,'%Y-%m-%d').date()
        #print demarcation_date,demarcation_date_str
        #clicked_items=[]
        try:
            engine=db
            #create a Session
            Session = sessionmaker(bind=engine)
            session = Session()

            #res=session.query(distinct(ClickedItemsRecord.intermediary_id).label("id")).all()
            #get all the
            users_count=0
            resusers=session.query(Beneficiary).order_by(Beneficiary.intermediary_id).all()
          
            #Phase 1

            for user in resusers:
                print "%s\t"%user.intermediary_id,

                                  
                resuserfood=session.query(func.count(FoodAndBeverage.id).label("mealscounter")).filter(FoodAndBeverage.beneficiary_id==user.id).filter(FoodAndBeverage.date_consumed>=demarcation_date0).filter(FoodAndBeverage.date_consumed<demarcation_date).first()    
                

                if resuserfood is None:
                    print 0
                else:
                    print "%s\t"%resuserfood.mealscounter


            print "\n\n\n"

            for user in resusers:
                print "%s\t"%user.intermediary_id,

                                  
                resuserfood=session.query(func.count(FoodAndBeverage.id).label("mealscounter")).filter(FoodAndBeverage.beneficiary_id==user.id).filter(FoodAndBeverage.date_consumed>=demarcation_date).first()    
                

                if resuserfood is None:
                    print 0
                else:
                    print "%s\t"%resuserfood.mealscounter



                          
 
        except Exception as e:
            print "Exception thrown in getMealsRecorded: %s"%e 
            #result["R00"]=-1
            #result["R01"]=e
          
          
        print "\n\n\n"
        #self.steps=sum_steps
        session.close()
        engine.dispose()
        dbconn.close()
        
        #return (json.JSONEncoder().encode(result))




obj=RetrieveLogData()

#firstweek
demarcation_date_str='2015-11-13'
demarcation_date_str0='2015-10-25'
result=obj.getMealsRecorded(demarcation_date_str,demarcation_date_str0)

'''
#secondweek
demarcation_date_str='2015-11-26'
demarcation_date_str0='2015-11-13'
result=obj.getClickedItemsRecord(demarcation_date_str,demarcation_date_str0)


#thirdweek
demarcation_date_str='2015-11-08'
demarcation_date_str0='2015-11-01'
result=obj.getClickedItemsRecord(demarcation_date_str,demarcation_date_str0)



#fourthweek
demarcation_date_str='2015-11-15'
demarcation_date_str0='2015-11-08'
result=obj.getClickedItemsRecord(demarcation_date_str,demarcation_date_str0)


#fifthweek
demarcation_date_str='2015-11-22'
demarcation_date_str0='2015-11-15'
result=obj.getClickedItemsRecord(demarcation_date_str,demarcation_date_str0)


#sixthweek
demarcation_date_str='2015-11-29'
demarcation_date_str0='2015-11-22'
result=obj.getClickedItemsRecord(demarcation_date_str,demarcation_date_str0)



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
'''