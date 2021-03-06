#!/usr/bin/env python
import time
import pika
import json
import urllib2,urllib
import logging





def send_sms(myjson):
        result={}
	values={}
	values["content"]=myjson["content"]
	values["to"]=[myjson["to"]]
	msg_id=myjson["msgID"]
        #print values
        
	url="https://platform.clickatell.com/messages"
	try:
		
		data=json.JSONEncoder().encode(values)
		req = urllib2.Request(url, data)
		req.add_header("Content-type",'application/json')
		req.add_header("Accept",'application/json')
		                   
		req.add_header('Authorization', 'b3itx5JgS-O7nc7xJ9KVlw==')
		                    
		response = urllib2.urlopen(req)
		                 
		data = json.load(response)  
		#json.loads(json.JSONEncoder().encode(data))["messages"][0]["accepted"]
		accepted_status=json.loads(json.JSONEncoder().encode(data))["messages"][0]["accepted"]
		msg_error_status=json.loads(json.JSONEncoder().encode(data))["messages"][0]["error"]
		snd_error_status=json.loads(json.JSONEncoder().encode(data))["error"]
		                 #print data
		                 
		if accepted_status == True and msg_error_status==None and snd_error_status==None:
		
		    result["message"]="SMS was sent successfully"
		    result["status"]=1
		                      #self.changeQueuedSMSStatus(msg_id)
		else:
		    result["message"]="SMS failed to send due to the following error: '%s'"%snd_error_status
		    result["status"]=-6
    	except urllib2.URLError as err: 
        	result["message"]="Error: '%s' occurred in sending msg with id='%s'. Check if you are connected to the Internet. If the problem persists contact the developer"%(err,msg_id)           
       
                        
                                
                           
    	except Exception as error:
                         #print response.code
        	result["message"]="Error in sending a message id='%s' with the following code: %s"%(msg_id,error)
      
    	finally:
    		#pass
                print result

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='clickatell_sms')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % json.loads(body))
    send_sms(json.loads(body))

channel.basic_consume(callback,
                      queue='clickatell_sms',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
