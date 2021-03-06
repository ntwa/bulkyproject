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
from applogic.manage_sms import ScheduleSMS
from applogic.manage_campaign import ManageCampaign 
from applogic.manage_groups import GroupsManager
from applogic.manage_message_template import ManageMessageTemplates
import csv
import xlwt
import xlrd
from models import AddressBook, MobileDetails,EmailDetails,Groups,GroupMembers
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from xlrd.sheet import ctype_text
import re
from bisect import bisect_left 
  
def binarySearch(a, x): 
    i = bisect_left(a, x) 
    if i != len(a) and a[i] == x: 
        return i 
    else: 
        return -1

def insertionSort(arr): 
  
    # Traverse through 1 to len(arr) 
    for i in range(len(arr)): 
  
        key = arr[i] 
  
        # Move elements of arr[0..i-1], that are 
        # greater than key, to one position ahead 
        # of their current position 
        j = i-1
        while j >=0 and key < arr[j] : 
                arr[j+1] = arr[j] 
                j -= 1
        arr[j+1] = key 


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

def saveCampaigns(myjson,request):
    obj=ManageCampaign(myjson)
    msg=obj.saveOneCampaignInDB(request)#we pass request as it may be needed when uploading reminder file
    print json.loads(msg)
    return msg

def retrieveCampaigns(myjson):
    obj=ManageCampaign(myjson)
    msg=obj.retrieveCampaignDetailsFromDB()
    return msg

def smsScheduling(myjson):
    #myjson={"MobNo":"+255742340759","MessageBody":"Hello, we are testing sending of one SMS."}
    obj=ScheduleSMS(myjson)
    msg=obj.saveOneSMSInDB()
    return msg
def retrieveMessageTemplates(myjson):
    obj=ManageMessageTemplates(myjson)
    msg=obj.retrieveSMSTemplates()
    return msg

def searchArray(item,array):


     for i in range(len(array)):
          if item==array[i]:
               return 1
  
     return -1



@csrf_exempt 
def dataupdate(request,command_id):#REST API used by the client side of web application to load data for display
     myjson={}
     if command_id =="SS":#Command for sending one SMS
          #myjson={"MessageBody":"Hello. We wish you happy new year...","MobNo":"+255742340759"}
          myjson=json.loads(request.body)
          #myjson={}
          status=smsScheduling(myjson)
          #myjson=json.JSONEncoder().encode(myjson)
          return HttpResponse('%s(%s)' % (request.GET.get('callback'),status), content_type='application/json')

     elif command_id =="SGD":#Command for saving groups' details
          myjson=json.loads(request.body)
          #myjson={}
          status=saveGroups(myjson)
          return HttpResponse('%s(%s)' % (request.GET.get('callback'),status), content_type='application/json')

     elif command_id =="SCD":#Command for saving campaigns' details
          #myjson=json.loads(request.body)
          myjson=json.loads(request.POST.get('json'))
          #result={}
          #request.POST.get('')
        
          #result["message"]="Got here: %s"%campaignname
          #status=json.JSONEncoder().encode(result)
          #myjson={}
          status=saveCampaigns(myjson,request)
          return HttpResponse('%s(%s)' % (request.GET.get('callback'),status), content_type='application/json')
          #return HttpResponse(status, content_type='application/json') #This is for debugging.

     elif command_id =="UAF": #Upload Address File
          myjson={"status": "file uploaded"}

          #addressfile = request.FILES['addressfile']
          #workbook = xlrd.open_workbook(addressfile)
          msg={"message":""}
          try:

               if request.method == 'POST' and request.FILES['addressfile']:
                    addressbookfile = request.FILES['addressfile']
                    fs = FileSystemStorage()
                    filename = fs.save("contacts.xls", addressbookfile)
                    uploaded_file_url = fs.url(filename)
                    path="%s/media/%s"%(os.getcwd(),filename)
                    myjson["status"]="%s. Path=%s"%(myjson["status"],path)
                    #fname=fname = join(dirname(dirname(abspath(__file__))), 'media/',filename)

                    xl_workbook = xlrd.open_workbook(path)
                    sheet_names = xl_workbook.sheet_names() 

                    xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
                    num_rows=xl_sheet.nrows
                    num_columns=xl_sheet.ncols
                    col_counter=0 # count the number of columns we have visited
                    #max_columns=num_columns
                    #sentinal=1
                    strrow=""
                    records=[]
                    col_headers=['contact_id','First Name','Middle Name','Last Name','Gender','DOB','Ward','District','Region','Country','Mobile Phone #1','Mobile Phone #2','Mobile Phone #3','Email Address #1','Email Address #2','Email Address #3']
                    col_headers_order=[]
                    header_counter_on=0
                    col_header_counter=0

                    str_reg_expr="^(?![\s\S])" #A regualar expression for matching empty strings
                    #str_reg_expr2="^(?[\s\S])" #A regualar expression for matching strings with only white spaces
                    
                    #
                    for row_posn in range(num_rows):

                         row=[]
                         col_counter=0
                         row_content=""
                         
                         #print row_posn
                         #print ""
                         #print ""


                         for col_posn in range(num_columns):
                              cell= xl_sheet.cell(row_posn,col_posn)
                              strcontent="%s"%cell.value
                              find=strcontent.find("+")
                              if find>=0:
                                   row_content="%s%s"%(row_content,strcontent[1:])
                                   strcontent="%s"%strcontent[1:] # get rid of + sign
                              else:
                                   row_content="%s%s"%(row_content,strcontent)

                              #row_content="%s%s"%(row_content,strcontent)
                              
                              test_result=re.match(strcontent, str_reg_expr, re.IGNORECASE) # Now check if one cell is empty
                              test_result2=re.match(row_content, str_reg_expr, re.IGNORECASE) # Now check if the entire row is empty
                              
                              if test_result and test_result2:
                                   #print test_result2.groups(0) 
                                   pass
                                   #if col_posn==0:
                                        #print "Empty encountered at cell (%s,%s) and str=%s"%(row_posn,col_posn,strcontent)
                              else:

                                   if searchArray(cell.value,col_headers)>0: #First check if the column is header, if it is header don't append
                                        
                                        if col_posn==0:
                                             #print "Change head counter"
                                             header_counter_on=1 #This means we have started conting headers
                                        col_headers_order.append("%s"%cell.value) 
                                        col_header_counter=col_header_counter+1
                                   elif header_counter_on==0 and test_result2==None: #These are for headers that are not column heading
                                        pass
                          
                                        #print "Row empty but some cells encountered at cell (%s,%s) and str=%s"%(row_posn,col_posn,strcontent)
                                   else:  
                                        #print "There is some content at row cell (%s,%s) and str=%s"%(row_posn,col_posn,strcontent)
                                       #First we have to confirm that we found all necessary headers
                                        if col_header_counter==num_columns:  
                                            pass
                                        else:
                                             #print "%s=%s"%(col_header_counter,num_columns)
                                             #just return error to the user as the naming of column headers don't conform to the ones expected.
                                             myjson["status"]="Error. Process terminated. Not the naming of all column headers conform to the allowed ones ."
                                             os.remove(path) #remove the file once done with it
                                             status=json.JSONEncoder().encode(myjson)
                                             return HttpResponse('%s(%s)' % (request.GET.get('callback'),status), content_type='application/json')



                                        cellvalue= cell.value  

                                         #check if a cell is empty.

                                        if test_result:
                                            #It means the cell was left blank therefore assine "None" to cellvalue
                                            cellvalue=None

                                        row.append(cellvalue)
                                        col_counter=col_counter+1
                                   
                                  
                                   #row.append(cell.value)
                                   #col_counter=col_counter+1

                         #check if the entire row is empty 
                         if col_counter==num_columns: #It means there were no empty columns in this row or the columns don't represent headers.
                              records.append(row)

          
                    error_detected=-1  
                    error_value="None"   
                    row_counter=0 
                    #insert one record at a time
                    fail_to_be_updated_records=[]
                
                    #for rec in records:
                    for row_record in range(len(records)):
                         #Now prep a json object
                         columncounter=0 
                         jsondata={}
                         current_record="None" #This variable is important in cases of errors as it helps in knowing which record was being updated when the error occured
                    
    
                         
                         #for dataval in rec:
                         for dataval in records[row_record]:
                              key="%s"%col_headers_order[columncounter]
                         
                              if col_headers_order[columncounter]=="DOB":
                                  try:
                                        base = datetime.datetime(1899,12,30)
                                        datetime_object = datetime.datetime.strptime(dataval, '%d %b %Y')
                                        date_obj_str=datetime_object.strftime("%Y-%m-%d")
                                        #datetime_object=datetime.datetime.strptime(date_obj_str, "%d/%m/%Y")
                                        #myjson["status"]=date_obj_str
                                        #initial_time=datetime.datetime.strptime(end_time_cluster, "%H:%M")-datetime.timedelta(hours=6)+
                                        #jsondata[key]=(base + datetime.timedelta(int(date_obj_str))).strftime('%Y-%m-%d')
                                        #jsondata[key]=(base + datetime.timedelta(datetime_object)).strftime('%Y-%m-%d')
                                        jsondata[key]=date_obj_str
                                        
                                       
                                  except Exception as e:
                                        error_detected=1
                                        error_value=e
                                        fail_to_be_updated_records.append(row_record)
                                        break # We just skip this record and move to the next
                             
        
                              elif col_headers_order[columncounter]=="contact_id":
                                  jsondata[key]=int(dataval)
          
                              else:
                                  jsondata[key]=dataval
                              columncounter=columncounter+1
                              
                
                         if error_detected>0:
                              pass
                              if error_detected==1:
                                  error_message="The system has encountered error(s)!: '%s'. Make sure your excel file follows the downloaded template format. "%error_value
                                  #skip this record only and go to the next one
                                  #raise ValueError(error_message)
                              else:
                                  raise ValueError("The system has encountered errors!.")
                         else:
                         
                              obj=AddressBookManager(jsondata)

                              loadedmsg=obj.saveContactInDB()


                              msg["message"]=json.loads(loadedmsg)

                         
                              if msg["message"]["opstatus"]["success"]<0:

                                  error_detected=2
                                  raise ValueError("The following error in adding an address: %s"%msg["message"])
                              else:
                                  pass
    

                                  
                      

                

                     



                    '''
                    if error_detected>0:
                         if error_detected==1:
                              error_message="The system has encountered error(s)!: '%s'. Make sure your excel file follows the downloaded template format. "%error_value
                              #raise ValueError(error_message)
                         elif error_detected==2:
                              raise ValueError("The following error in adding an address: %s"%msg["message"])
                         else:
                              raise ValueError("The system has encountered errors!.")
                    
                    '''
                    



                    myjson["status"]="All records were updated successfully"



                    os.remove(path) #remove the file once done with it

          except Exception as e:
                     
                    if len(remain_to_be_updated_records)>0:
                         myjson["status"]="Exception thrown: %s. The Error occured while updating the record with contact_id = '%s'. The following records failed to be updated: %s"%(e,current_record,fail_to_be_updated_records)
                    elif len(records)>0:
                         myjson["status"]="Exception thrown: %s. But all records were updated successfully: %s"%e
                    else:
                         myjson["status"]="Exception thrown: %s, plus, there were no records to update: %s"%e
                    
                    #Show the records that failed to be updated
                   


                #name = addressfile.name
                #attached_file1 = files.get('file1', None)
                #attr1 = data.get('attr1', None)
          
          status=json.JSONEncoder().encode(myjson)
          
          return HttpResponse('%s(%s)' % (request.GET.get('callback'),status), content_type='application/json')
          #return HttpResponse(status, content_type='application/json')

  


@csrf_exempt 
def dataloader(request,command_id):#REST API used by the client side of web application to load data for display
     myjson={}
     if command_id == "RABC":#RAB stands for Retrieve Address Book Content
          myjson=json.loads(request.body)
          #myjson={"GroupID":"-1","Option":"-1"}
          #myjson={"GroupID":"-1"}  
          alldata=retrieveAddressBookContent(myjson)
          #return HttpResponse(alldata, content_type='application/json') #This is for debugging.
          return HttpResponse('%s(%s)' % (request.GET.get('callback'),alldata), content_type='application/json')

     elif command_id =="RABT":#RABT stands for Retrieve Address Book Template
          context = RequestContext(request)
          return render_to_response('addressbook.html', context)


          #return HttpResponse(status, content_type='application/json')



     elif command_id =="RCT":#Command for retrieving template for displaying campaigns
          context = RequestContext(request)
          return render_to_response('campaigns.html', context)

     elif command_id == "ROCT":#Command for retrieving template for display one campaign for editing
          context = RequestContext(request)
          return render_to_response('campaign_edit.html', context)


     elif command_id =="RCC":#Command for retrieving content for campaigns 
          myjson=json.loads(request.body)
          #myjson={}
          status=retrieveCampaigns(myjson)
          return HttpResponse('%s(%s)' % (request.GET.get('callback'),status), content_type='application/json')
                
                
          #return HttpResponse(status, content_type='application/json')

     elif command_id =="RGT":#Command for retrieving template for displaying groups
          context = RequestContext(request)
          return render_to_response('groups.html', context)


     elif command_id =="RSTT":#Command for retrieving template for displaying settings
          context = RequestContext(request)
          return render_to_response('settings.html', context)    

    

     elif command_id =="RGC":#Command for retrieving for retrieving groups' details
          myjson=json.loads(request.body)
          #myjson={}
          status=retrieveGroups(myjson)
          return HttpResponse('%s(%s)' % (request.GET.get('callback'),status), content_type='application/json')
          #return HttpResponse(status, content_type='application/json')



     elif command_id =="RGAT":#Command for retrieving template for displaying all contacts. This used for assigning members to groups
          context = RequestContext(request)
          return render_to_response('groupallocation.html', context)

     elif command_id =="RMSGT":#Retrieve Message Templates
          myjson=json.loads(request.body)
          #myjson={}
          #myjson={"CategoryId":4,"TemplateId":-1,"TemplateContent":"Happy holidays @@firstname@@! We value you as our esteemed customer. Thank you for your support."}   
          status=retrieveMessageTemplates(myjson)
          return HttpResponse('%s(%s)' % (request.GET.get('callback'),status), content_type='application/json')

          #return HttpResponse(status, content_type='application/json')

     elif command_id == "RDDN": #this template is for new reminders hence it won't have any dates in it.
          #Reminder Download Data template
          #With the template, we can specify reminders lets for expiry of driving licence or expiry of road insurance. For instance each car, a driver need to be notified 
          #myjson=json.loads(request.body)
          json_object = request.GET['jsonObj']
          json_object_1=json.loads(json_object)

          json_extra=request.GET['extraJson']
          json_extra_1=json.loads(json_extra)


          existing_campaign=json_extra_1["Existing"] #This differentiates editing of existing campaign to a new campaign .An existing campaign may arlead have some reminders.


          response = HttpResponse(content_type='application/ms-excel')
          response['Content-Disposition'] = 'attachment; filename="reminders.xls"'


          wb = xlwt.Workbook(encoding='utf-8')
          ws = wb.add_sheet('UsersWithReminders')


          row_num = 2
           
          #font style for first header 
          font_style = xlwt.XFStyle()
          font_style.font.bold = True
          font_style.font.height = 320
          font_style.num_format_str= '@'


          date_format = xlwt.XFStyle()
          date_format.num_format_str = 'dd/mm/yyyy'
          #date_format.align="horiz center"


          number_format=xlwt.XFStyle()
          number_format.num_format_str='0'
          #umber_format.align="horiz center"
          
          #ws.write(0, 0, "Mambo Yote SMS Address Book", font_style)
          #ws.write_merge(0, 1, 0, 8, "Mambo Yote SMS Address Book", font_style)
          #json_object_1[0]["value"]  len(json_object_1)

          ws.write_merge(0, 1, 0, 15, "Individual Reminders" ,xlwt.easyxf("pattern: pattern solid, fore_color light_blue ; font: color white, height 320, bold True; align: horiz center; borders: top_color red, bottom_color red, right_color red, left_color red, left thin, right thin, top thin, bottom thin;"))
          
          if existing_campaign==1:
              columns = ['contact_id','First Name', 'Last Name', 'Reminder Expiry Date','Days of Running','Deadline for Action',"Reason For Reminder","Existing Reminder"]
          else:
              columns = ['contact_id','First Name', 'Last Name', 'Reminder Expiry Date','Days of Running','Deadline for Action',"Reason For Reminder"]
          #If expiry date not specified then the deadline for action takes precedence as the expiry date. 
          #font style for columns' headings
          font_style = xlwt.XFStyle()
          font_style.font.bold = True
          font_style.font.height = 280
          #ont_style.align="horiz center"
          font_style.num_format_str= '@'
          for col_num in range(len(columns)):
               #ws.write(row_num, col_num, columns[col_num], font_style)

               cwidth = ws.col(col_num).width
               if (len(columns[col_num])*367) > cwidth:  
                    ws.col(col_num).width = (len(columns[col_num])*367)+400 


               #ws.write_merge(row_num, row_num+1, col_num, col_num, columns[col_num], font_style)
               ws.write_merge(row_num, row_num+1, col_num, col_num, columns[col_num], xlwt.easyxf("pattern: pattern solid, fore_color light_orange; font: color black, height 240, bold True; align: horiz center; borders: top_color red, bottom_color red, right_color red, left_color red, left thin, right thin, top thin, bottom thin;"))
               
               #xlwt.easyxf("pattern: pattern solid, fore_color yellow; font: color white; align: horiz right")

          row_num = row_num+1     

         

              # Sheet body, remaining rows
          font_style = xlwt.XFStyle()
          font_style.num_format_str= '@'
          group_ids=[]
          contact_ids=[]
          number_of_groups=len(json_object_1)#
          number_existing_groups=len(json_extra_1)
          number_of_contacts=0
          if number_of_groups ==0 and number_existing_groups=0:
              pass
              #The search everyone
          elif number_existing_groups==0:
              #Then number of groups is not equal to zero, since this can be reached only if the above fails becuase number of groups is not equal to zero 
              pass  
          elif number_of_groups ==0:
               #number of existing group is not equal to zero, since this can be reached only if the above fails becuase number of existing groups is not equal to zero       
          else:
              #here it means both existing groups set and selected groups set are not empty

              #The start with groups that existed

              for group_posn  in range(number_existing_groups):

                  selected_group_id=int(json_extra_1[group_posn]["value"])# retrieve one group at a time

                  #group_ids.append(selected_group_id)
                  #group_members=GroupMember.objects.all().filter(group=selected_group_id)
                  if selected_group_id==0:
                      #rows=AddressBook.objects.all().values_list('contact_id','first_name','last_name')# get all people in the address book
                      rows=AddressBook.objects.values_list('contact_id','first_name','last_name').filter(individualizedreminders__group=selected_group_id)

                  else:

                      rows=AddressBook.objects.values_list('contact_id','first_name','last_name').filter(groupmembers__group=selected_group_id)
                  
        
                  #rows=group_members.AddressBook.objects.all()
                  
                  for row in rows:
                      row_num += 1
                      last_column=0

                      contact_id=row[0] # we want to remove duplicates, lets a person who belong to more that one group and atleast two of his/her groups have been selected
                      if binarySearch(contact_ids, contact_id) is -1:
                          contact_ids.append(contact_id)
                          insertionSort(contact_ids)
                          number_of_contacts=number_of_contacts+1
                      else:
                          continue #Move to the next row because the retirved row is a repitition of an existing contact_id


                      for col_num in range(len(row)):


                              #if columns[col_num]=='contact_id': #col_num==0:
                              #     ws.write(row_num, col_num, row[col_num], number_format)

                              #elif columns[col_num]=='DOB':#col_num==5:
                               #It means we dealing with date hence it should be formated as date
                              #     ws.write(row_num, col_num, row[col_num], date_format)
                              #else:
                          ws.write(row_num, col_num, row[col_num], font_style)
                          last_column=last_column+1
                      ws.write(row_num, col_num+1, '01 Jan 2010', date_format)
                      ws.write(row_num, col_num+2, 7, number_format)
                      ws.write(row_num, col_num+3, '01 Jan 2010', date_format)




              for group_posn  in range(number_of_groups):

                  selected_group_id=int(json_object_1[group_posn]["value"])# retrieve one group at a time


                  #group_ids.append(selected_group_id)
                  #group_members=GroupMember.objects.all().filter(group=selected_group_id)
                  if selected_group_id==0:
                      rows=AddressBook.objects.all().values_list('contact_id','first_name','last_name')# get all people in the address book

                  else:

                      rows=AddressBook.objects.values_list('contact_id','first_name','last_name').filter(groupmembers__group=selected_group_id)
                  
        
                  #rows=group_members.AddressBook.objects.all()
                  
                  for row in rows:
                      row_num += 1
                      last_column=0

                      contact_id=row[0] # we want to remove duplicates, lets a person who belong to more that one group and atleast two of his/her groups have been selected
                      if binarySearch(contact_ids, contact_id) is -1:
                          contact_ids.append(contact_id)
                          insertionSort(contact_ids)
                          number_of_contacts=number_of_contacts+1
                      else:
                          continue #Move to the next row because the retirved row is a repitition of an existing contact_id


                      for col_num in range(len(row)):


                              #if columns[col_num]=='contact_id': #col_num==0:
                              #     ws.write(row_num, col_num, row[col_num], number_format)

                              #elif columns[col_num]=='DOB':#col_num==5:
                               #It means we dealing with date hence it should be formated as date
                              #     ws.write(row_num, col_num, row[col_num], date_format)
                              #else:
                          ws.write(row_num, col_num, row[col_num], font_style)
                          last_column=last_column+1
                      ws.write(row_num, col_num+1, '01 Jan 2010', date_format)
                      ws.write(row_num, col_num+2, 7, number_format)
                      ws.write(row_num, col_num+3, '01 Jan 2010', date_format)


                  

                   
          #rows = IndividualizedReminders.objects.all().values_list('contact_id','reminder_deadline_date', 'middle_name','last_name', 'gender','birth_date','ward','district','region','country')
          

          #font_style.font.align="horiz center"

          '''
          #rows = IndividualizedReminders.objects.all().values_list('contact_id','reminder_deadline_date', 'middle_name','last_name', 'gender','birth_date','ward','district','region','country')
          
          for row in rows:
               row_num += 1
               last_column=0
               total_mobiles=0
               for col_num in range(len(row)):
                    if columns[col_num]=='contact_id': #col_num==0:
                         ws.write(row_num, col_num, row[col_num], number_format)

                    elif columns[col_num]=='DOB':#col_num==5:
                         #It means we dealing with date hence it should be formated as date
                         ws.write(row_num, col_num, row[col_num], date_format)
                    else:
                         ws.write(row_num, col_num, row[col_num], font_style)
                    last_column=last_column+1

               #Get all the mobile numbers for this contact  
               no_mobiles=0   
               subrows=MobileDetails.objects.values_list('mobile_number').filter(contact_id=row[0])
               for subrow in subrows:
                   
                    for col_num in range(len(subrow)):
                         ws.write(row_num, last_column, subrow[0], font_style)  
                         last_column=last_column+1
                         no_mobiles+=1

               while no_mobiles<3:#Just skip columns for missing mobiles
                    last_column+=1
                    no_mobiles+=1



               #Get all the email addresses for this contact  
               no_email_addresses=0
               subrows=EmailDetails.objects.values_list('email_address').filter(contact_id=row[0])
               for subrow in subrows:
                    
                    for col_num in range(len(subrow)):
                         ws.write(row_num, last_column, subrow[0], font_style)  
                         last_column=last_column+1
                         no_email_addresses+=1

               while no_email_addresses<3:#Just skipp columns for missing mobiles
                    last_column+=1
                    no_email_addresses+=1

          '''

          if number_of_contacts==0:
              wb_error = xlwt.Workbook(encoding='utf-8')
              ws_error = wb_error.add_sheet('UsersWithRemindersError')

              ws_error.write_merge(0, 1, 0, 15, "Error: The groups you have selected have no members" ,xlwt.easyxf("pattern: pattern solid, fore_color white; font: color red, height 320, bold True; align: horiz center; borders: top_color red, bottom_color red, right_color red, left_color red, left thin, right thin, top thin, bottom thin;"))
              wb_error.save(response)
          else:
              wb.save(response)




          return response
      


          


     elif command_id =="ADD":
      
           #Address Data Download
          response = HttpResponse(content_type='application/ms-excel')
          response['Content-Disposition'] = 'attachment; filename="contacts.xls"'


          wb = xlwt.Workbook(encoding='utf-8')
          ws = wb.add_sheet('Users')


          row_num = 2
           
          #font style for first header 
          font_style = xlwt.XFStyle()
          font_style.font.bold = True
          font_style.font.height = 320
          font_style.num_format_str= '@'


          date_format = xlwt.XFStyle()
          date_format.num_format_str = 'dd/mm/yyyy'
          #date_format.align="horiz center"


          number_format=xlwt.XFStyle()
          number_format.num_format_str='0'
          #umber_format.align="horiz center"
          
          #ws.write(0, 0, "Mambo Yote SMS Address Book", font_style)
          #ws.write_merge(0, 1, 0, 8, "Mambo Yote SMS Address Book", font_style)
          ws.write_merge(0, 1, 0, 15, "Mambo Yote SMS Address Book",xlwt.easyxf("pattern: pattern solid, fore_color light_blue ; font: color white, height 320, bold True; align: horiz center; borders: top_color red, bottom_color red, right_color red, left_color red, left thin, right thin, top thin, bottom thin;"))
          
          columns = ['contact_id','First Name', 'Middle Name', 'Last Name', 'Gender','DOB','Ward','District','Region','Country',"Mobile Phone #1","Mobile Phone #2","Mobile Phone #3",'Email Address #1','Email Address #2','Email Address #3']

          #font style for columns' headings
          font_style = xlwt.XFStyle()
          font_style.font.bold = True
          font_style.font.height = 280
          #ont_style.align="horiz center"
          font_style.num_format_str= '@'
          for col_num in range(len(columns)):
               #ws.write(row_num, col_num, columns[col_num], font_style)

               cwidth = ws.col(col_num).width
               if (len(columns[col_num])*367) > cwidth:  
                    ws.col(col_num).width = (len(columns[col_num])*367)+400 


               #ws.write_merge(row_num, row_num+1, col_num, col_num, columns[col_num], font_style)
               ws.write_merge(row_num, row_num+1, col_num, col_num, columns[col_num], xlwt.easyxf("pattern: pattern solid, fore_color light_orange; font: color black, height 240, bold True; align: horiz center; borders: top_color red, bottom_color red, right_color red, left_color red, left thin, right thin, top thin, bottom thin;"))

               #xlwt.easyxf("pattern: pattern solid, fore_color yellow; font: color white; align: horiz right")

          row_num = row_num+1

              # Sheet body, remaining rows
          font_style = xlwt.XFStyle()
          font_style.num_format_str= '@'
          #font_style.font.align="horiz center"



          rows = AddressBook.objects.all().values_list('contact_id','first_name', 'middle_name','last_name', 'gender','birth_date','ward','district','region','country')
          
          for row in rows:
               row_num += 1
               last_column=0
               total_mobiles=0
               for col_num in range(len(row)):
                    if columns[col_num]=='contact_id': #col_num==0:
                         ws.write(row_num, col_num, row[col_num], number_format)

                    elif columns[col_num]=='DOB':#col_num==5:
                         #It means we dealing with date hence it should be formated as date

                         ws.write(row_num, col_num, row[col_num].strftime('%d %h %Y'), date_format)
                    else:
                         ws.write(row_num, col_num, row[col_num], font_style)
                    last_column=last_column+1

               #Get all the mobile numbers for this contact  
               no_mobiles=0   
               subrows=MobileDetails.objects.values_list('mobile_number').filter(contact_id=row[0])
               for subrow in subrows:
                   
                    for col_num in range(len(subrow)):
                         ws.write(row_num, last_column, subrow[0], font_style)  
                         last_column=last_column+1
                         no_mobiles+=1

               while no_mobiles<3:#Just skip columns for missing mobiles
                    last_column+=1
                    no_mobiles+=1



               #Get all the email addresses for this contact  
               no_email_addresses=0
               subrows=EmailDetails.objects.values_list('email_address').filter(contact_id=row[0])
               for subrow in subrows:
                    
                    for col_num in range(len(subrow)):
                         ws.write(row_num, last_column, subrow[0], font_style)  
                         last_column=last_column+1
                         no_email_addresses+=1

               while no_email_addresses<3:#Just skipp columns for missing mobiles
                    last_column+=1
                    no_email_addresses+=1




          wb.save(response)




          return response
      



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
