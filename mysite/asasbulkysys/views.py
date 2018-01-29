from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import logging
import json,sys,urllib2
import datetime,calendar
from django.template.loader import render_to_string
from applogic.manage_contacts import AddressBookManager
from applogic.save_sms import SaveSMS
from applogic.manage_groups import GroupsManager

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    context = RequestContext(request)
    return render_to_response('index.html', context)

# retrieve all contacts
def retrieveAddressBookContent(myjson):
     #myjson={"GroupID":"4"}
     obj=AddressBookManager(myjson)
     contacts=obj.retrieveContactDetailsFromDB() #the returned contacts is an encoded json object    
     return contacts

def retrieveGroups(myjson):
    obj=GroupsManager(myjson)
    msg=obj.retrieveGroupDetailsFromDB()
    return msg


def saveGroups(myjson):
    obj=GroupsManager(myjson)
    msg=obj.saveGroupInDB()
    return msg

def saveSMS(myjson):
    obj=SaveSMS(myjson)
    msg=obj.saveOneSMSInDB()
    return msg

@csrf_exempt 
def dataloader(request,command_id):#REST API used by the client side of web application to load data for display
     myjson={}
     if command_id == "RABC":#RAB stands for Retrieve Address Book Content
          myjson=json.loads(request.body)
          #myjson={"GroupID":"-1","Option":"-1"}
          #myjson={"GroupID":"-1"}  
          alldata=retrieveAddressBookContent(myjson)
          #return HttpResponse(alldata, content_type='application/json')
          return HttpResponse('%s(%s)' % (request.GET.get('callback'),alldata), content_type='application/json')

     elif command_id =="RABT":#RABT stands for Retrieve Address Book Template
          context = RequestContext(request)
          return render_to_response('addressbook.html', context)

     elif command_id =="SS":#Command for sending one SMS
          #myjson={"MessageBody":"Hello. We wish you happy new year...","MobNo":"+255742340759"}
          myjson=json.loads(request.body)
          status=saveSMS(myjson)
          #myjson=json.JSONEncoder().encode(myjson)
          return HttpResponse('%s(%s)' % (request.GET.get('callback'),status), content_type='application/json')
          #return HttpResponse(status, content_type='application/json')

     elif command_id =="RGT":#Command for retrieving template for displaying groups
          context = RequestContext(request)
          return render_to_response('groups.html', context)

     elif command_id =="RGC":#Command for retrieving for retrieving groups' details
          myjson=json.loads(request.body)
          #myjson={}
          status=retrieveGroups(myjson)
          return HttpResponse('%s(%s)' % (request.GET.get('callback'),status), content_type='application/json')
          #return HttpResponse(status, content_type='application/json')



     elif command_id =="SGR":#Command for retrieving for retrieving groups' details
          myjson=json.loads(request.body)
          #myjson={}
          status=saveGroups(myjson)
          return HttpResponse('%s(%s)' % (request.GET.get('callback'),status), content_type='application/json')

     elif command_id =="RGAT":#Command for retrieving template for displaying all contacts. This used for assigning members to groups
          context = RequestContext(request)
          return render_to_response('groupallocation.html', context)

     '''
     elif command_id =="RMG":
         #RMG means retrieve meals goal
         goal=retrieveMealGoal(beneficiary_id)
         return HttpResponse(goal, mimetype='application/json')

     elif command_id =="RAG":
         #RAG means retrieve activity goal
         goal=retrieveActivityGoal(beneficiary_id)
         return HttpResponse(goal, mimetype='application/json') 		
     '''
