import daemon
import time
#import thread
import threading
import pika
import json
import urllib2,urllib
import logging
from clickatell.rest import Rest

'''
def send_sms(myjson):
	result={}
	values={}
	values["content"]=myjson["content"]
	values["to"]=[myjson["to"]]
	msg_id=myjson["msgID"]

        f= open("/home/ntwa/Documents/Development/Projects/Rabitmqlogs.txt","w+")
        f.write("This is line %s:"%values)
        token='b3itx5JgS-O7nc7xJ9KVlw=='

	try:
                clickatell = Rest(token); 
                response = clickatell.sendMessage(values["to"], values["content"])
                result["message"]="SMS was sent successfully"
 
    	except Exception as error:
                         #print response.code
        	result["message"]="Error in sending a message id='%s' with the following code: %s"%(msg_id,error)
      
    	finally:
    		pass
                f.write("End %s:"%result)
                f.close()
         
    		#write to a log file about the out come
		
       
'''

def send_sms(myjson):
	result={}
	values={}
	values["content"]=myjson["content"]
	values["to"]=[myjson["to"]]
	msg_id=myjson["msgID"]
	url="https://platform.clickatell.com/messages"

	try:
                f= open("/home/ntwa/Documents/Development/Projects/Rabitmqlogs.txt","w+")
                f.write("This is line %s:"%values)
        except Exception as e:
                pass
	
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
    		f.write("End %s:"%result)
                f.close()

    		#write to a log file about the out come



def callback(ch, method, properties, body):
	sms_json=json.loads(body)
        send_sms(sms_json)

        print(" [x] Received %r" % json.loads(body))
        time.sleep(5) # Wait for sixt second before acknowledgement.

        ch.basic_ack(delivery_tag = method.delivery_tag)
        print("Message acknowledged")
    	#try:
    	#	thread.start_new_thread( send_sms, (sms_json, ) )
	#except:
	#	print "Error: unable to start thread"






def startMessageReceiver():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()


 	channel.queue_declare(queue='yote_sms_multithreading')
    
        #channel.basic_qos(prefetch_count=1) # Not to give extra work to a process before it finishes one task
	channel.basic_consume(callback,
                        queue='yote_sms_multithreading')


	#channel.basic_consume(callback,
         #               queue='clickatell_sms',
         #             no_ack=True)

	print(' [*] Waiting for messages. To exit press CTRL+C')
	channel.start_consuming()

def run():
    	#with daemon.DaemonContext():
                #pass
        startMessageReceiver()

if __name__ == "__main__":
    	run()
        #startMessageReceiver()
