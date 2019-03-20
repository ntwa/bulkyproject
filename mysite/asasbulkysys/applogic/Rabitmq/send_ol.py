#!/usr/bin/env python
import pika
import json
import time
import datetime


message={}
message["to"]="+255742340759"
message["content"]="Testing sending of several messages"
message["msgID"]="Default"

#message_out=json.JSONEncoder().encode(message)
#out=json.dumps(message),

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

current_time=datetime.datetime.now()

channel.queue_declare(queue='yote_sms')
delay_range=0
for i in range(5):
     time.sleep(2)
     time_for_send=current_time+datetime.timedelta(seconds=delay_range)
     message["TimeStamp"]="%s"%time_for_send

     message_out=json.JSONEncoder().encode(message)
     channel.basic_publish(exchange='',
                      routing_key='yote_sms',
                      body=message_out)
     print(" [x] Sent '%s' to '%s'"%(message["content"],message["to"]))
     delay_range=delay_range+5 #We increment delay_range by 5 seconds
connection.close()
