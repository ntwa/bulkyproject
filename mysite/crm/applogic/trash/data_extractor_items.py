#!/usr/bin/env python
import datetime,calendar
from datetime import timedelta
import sys,json
from sqlalchemy import create_engine,distinct,func,asc
from sqlalchemy.orm import sessionmaker
from wellness.applogic.clicked_items_module import ClickedItemsRecord,db,dbconn
import os.path

    

class RetrieveLogData:
    def __init__(self):
        pass

    def getClickedItemsRecord(self,demarcation_date_str,demarcation_date_str0):
        

        demarcation_date=datetime.datetime.strptime(demarcation_date_str,'%Y-%m-%d').date()
        demarcation_date0=datetime.datetime.strptime(demarcation_date_str0,'%Y-%m-%d').date()
        #print demarcation_date,demarcation_date_str
        clicked_items=[]
        try:
            engine=db
            #create a Session
            Session = sessionmaker(bind=engine)
            session = Session()

            #res=session.query(distinct(ClickedItemsRecord.intermediary_id).label("id")).all()
            #get all the items first
            resitems=session.query(distinct(ClickedItemsRecord.itemname).label("itemname")).order_by(ClickedItemsRecord.itemname).all()
            #now store all the items in an array
            print "User\t",
            for item in resitems:
                clicked_items.append(item.itemname)
                print "%s\t"%item,
            print ""
            users_count=0
            resusers=session.query(distinct(ClickedItemsRecord.intermediary_id).label("id")).order_by(ClickedItemsRecord.usergroup).order_by(ClickedItemsRecord.intermediary_id).all()
          

            for user in resusers:
                print "%s\t"%user.id,
                    # iterate throug items for this user
                    #count logbook items first for this use 
                    #Logbook
                for itemname in clicked_items:
                    
                    resuseritems=session.query(func.count(ClickedItemsRecord.itemname).label("itemcounter")).filter(ClickedItemsRecord.intermediary_id==user.id).filter(ClickedItemsRecord.datecaptured>=demarcation_date0).filter(ClickedItemsRecord.usergroup==1).filter(ClickedItemsRecord.itemname==itemname).first()    
                    if resuseritems is None:
                        print "NIL\t",
                    else:
                        print "%s\t"%resuseritems.itemcounter,
                print ""
                print "%s\t"%user.id,
                    #Gamification
                for itemname in clicked_items:
                    resuseritems=session.query(func.count(ClickedItemsRecord.itemname).label("itemcounter")).filter(ClickedItemsRecord.intermediary_id==user.id).filter(ClickedItemsRecord.datecaptured>=demarcation_date0).filter(ClickedItemsRecord.usergroup==2).filter(ClickedItemsRecord.itemname==itemname).first()    
                    if resuseritems is None:
                        print "NIL\t",
                    else:
                        print "%s\t"%resuseritems.itemcounter,   
                #Go to new line to start another record
                print ""                 


               
              
                     

                      
 
        except Exception as e:
            print "Exception thrown in getClickedItemsRecord: %s"%e 
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
result=obj.getClickedItemsRecord(demarcation_date_str,demarcation_date_str0)

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