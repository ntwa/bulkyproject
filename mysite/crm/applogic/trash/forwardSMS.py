from save_sms_feedback import QueueFeedback
import json
import urllib2,urllib

class SMS:
   def __init__(self):
      pass
   
   
   def send(self,msg_id,mob,msg):
      
      mob = mob[:1].replace('0', '27') + mob[1:]
      values = {'user' : 'wellnessapp',
          'password' : 'AbGXWETGaKdEdD',
          'api_id' : '3543084',
           'to':mob,
           'text':msg}
         
      url="http://api.clickatell.com/http/sendmsg?"+urllib.urlencode(values)

      
      req = urllib2.Request(url)
      req.add_header("User-Agent",'Mozilla/5.0')

      req.add_header("Content-type",'application/x-www-form-urlencoded')

      page = urllib2.urlopen(req)
      result=page.read()
      searchstr="ID:"
      try:
      
         
          index=result.index(searchstr,0)
          if index>=0:
             print "Success"
             page.close()
             return 1
      except Exception as e:
          print "Message was not forwarded"
          page.close()
          return -1
     

          

   def startForwardSMS(self):
      myjson={}
      obj= QueueFeedback(myjson)
      msgs=obj.getQueuedSMS()
      msgs=json.loads(msgs)
      message_waiting=0
      for res in msgs.items():
          message_waiting=1
          key,rec=res
          msg_id=rec["Id"]
          mobile=rec["Mobile"]
          msg=rec["Message"]
          sendStatus=self.send(msg_id,mobile,msg)
          if sendStatus>0:
             obj.changeQueuedSMSStatus(msg_id)
             print "Message Sent"
          
      if message_waiting==0:
         print "There are no messages in the queue"
        

      return myjson



obj=SMS()
result=obj.startForwardSMS()
print result
