#!/usr/bin/env python
import pika
import json
import time
import datetime


message={}



message["msgID"]="Default"

outgoing=[]
outgoing.append("Happy festive season out dearest customer. We are testing bulky SMS. Ignore this. Ntwa")
outgoing.append("I wish you happy holidays. We are testing a bulky SMS system. From Ntwa")
outgoing.append("Merry Xmass and happy new year friend. I am testing a bulky SMS System.  Ntwa.")
outgoing.append("Hello Friend. I am just testing sending of Bulky SMS. Ntwa")
outgoing.append("Hi there. Just Ignore my message. I am just testing Bulky SMS System. Ntwa") 
outgoing.append("Happy festive season friend. I am testing a Bulky SMS system. Ntwa")
outgoing.append("Happy holidays. We are testing a bulky SMS system. From Ntwa")
outgoing.append("Merry Xmass and happy new year friend. I am testing a bulky SMS System.  Ntwa.")
outgoing.append("Hello Friend. I am just testing sending of Bulky SMS. Ntwa")
outgoing.append("Happy festival season. I am testing a Bulky SMS system. Ntwa")
outgoing.append("Hi there. Just Ignore my message. I am just testing Bulky SMS System. Ntwa") 

contact_list=[]
contact_list.append("+255742340759")
contact_list.append("+255767686894")
contact_list.append("+255785732088")
contact_list.append("+255767547566")
contact_list.append("+255752333235")
contact_list.append("+255754711174")
contact_list.append("+255753008565")
contact_list.append("+255767555000")
contact_list.append("+255746194043")
contact_list.append("+255784965853")
contact_list.append("+255788212020")

#message_out=json.JSONEncoder().encode(message)
#out=json.dumps(message),

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#current_time=datetime.datetime.now()

channel.queue_declare(queue='yote_sms_multithreading')
delay_range=0
size=len(contact_list)
for i in range(11):
     right_most_posn=size-i-1
     message["to"]=contact_list[i]
     message["content"]=outgoing[right_most_posn]
     #time.sleep(1)
     #current_time=datetime.datetime.now()
     #time_for_send=current_time+datetime.timedelta(seconds=delay_range)
     #time_for_send=current_time
     #message["TimeStamp"]="%s"%time_for_send
     #message["content"]="Me: '%s'. Tarehe ya kutuma message: %s"%(message["content"],time_for_send)
     message_out=json.JSONEncoder().encode(message)
     channel.basic_publish(exchange='',
                      routing_key='yote_sms_multithreading',
                      body=message_out)
     print(" [x] Sent '%s' to '%s'"%(message["content"],message["to"]))
     #delay_range=delay_range+5 #We increment delay_range by 5 seconds
connection.close()
