#!/usr/bin/env python
import datetime,time,calendar
import sys,json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from save_sms_feedback import QueueFeedback
from collections import OrderedDict
from manage_message_template import ManageMessageTemplates


class ManageSettings:
     def __init__(self,myjson):
          self.myjson=myjson

     def manageSMSTemplateCategory(self):
          obj=ManageMessageTemplates(myjson)
          msg=obj.saveTemplateCategoryInDB()
          return msg

     def manageSMSTemplates(self):
          obj=ManageMessageTemplates(myjson)
          msg=obj.saveSMSTemplateInDB()
          return msg
     def manageSMSSignature(self):
          obj=ManageMessageTemplates(myjson)
          msg=obj.configureSMSSignature()
          return msg
     def retrievePrimarySMSSignature(self):
          obj=ManageMessageTemplates(myjson)
          msg=obj.getPrimarySignature()
          return msg

          
   

     
#myjson={"CategoryId":5,"CategoryName":"Driving Safety Reminders"}
     
#myjson={"CategoryId":5,"TemplateId":-1,"TemplateContent":"Hi @@firstname@@! Drive safely."}     
#obj=ManageSettings(myjson)
#msg=obj.manageSMSTemplateCategory()
#msg=obj.manageSMSTemplates()
#msg=obj.retrievePrimarySMSSignature()
#print msg

