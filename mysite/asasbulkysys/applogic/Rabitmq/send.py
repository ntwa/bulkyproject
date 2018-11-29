#!/usr/bin/env python
import pika
import json


message={}
message["to"]="+255742340759"
message["content"]="This is a text message to be relayed"
message["msgID"]="Default"
message_out=json.JSONEncoder().encode(message)
 #out=json.dumps(message),

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='clickatell_sms')
for i in range(10):
     pass
     channel.basic_publish(exchange='',
                      routing_key='clickatell_sms',
                      body=message_out)
     print(" [x] Sent '%s' to '%s'"%(message["content"],message["to"]))
connection.close()
