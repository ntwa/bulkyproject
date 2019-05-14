#!/usr/bin/env python
import datetime
import sys,json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from save_sms_feedback import QueueFeedback
from collections import OrderedDict

 
myjson={"message":"Hello","url":"no url","pic":"no pic","name":"no name","caption":"no caption","description":"description"}
obj=QueueFeedback(myjson)
result=obj.getQueuedSMS()
print result
msg_ids=json.loads(result)


for msg in msg_ids.items():
  key,msg_id=msg
  print key,msg_id["Id"]
  status_change_result=obj.changeQueuedSMSStatus(msg_id["Id"])
  print status_change_result
          
            

