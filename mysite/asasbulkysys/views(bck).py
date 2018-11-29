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
from applogic.manage_campaign import ManageCampaign 
from applogic.manage_groups import GroupsManager
from applogic.manage_message_template import ManageMessageTemplates
import csv
import xlwt
import xlrd
from models import AddressBook, MobileDetails
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from xlrd.sheet import ctype_text
import re


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

def saveCampaigns(myjson):
    obj=ManageCampaign(myjson)
    msg=obj.saveOneCampaignInDB()
    return msg

def retrieveCampaigns(myjson):
    obj=ManageCampaign(myjson)
    msg=obj.retrieveCampaignDetailsFromDB()
    return msg

def saveSMS(myjson):
    #myjson={"MobNo":"+255742340759","MessageBody":"Hello, we are testing sending of one SMS."}
    obj=SaveSMS(myjson)
    msg=obj.saveOneSMSInDB()
    return msg
def retrieveMessageTemplates(myjson):
    obj=ManageMessageTemplates(myjson)
    msg=obj.retrieveSMSTemplates()
    return msg

@csrf_exempt 
def dataupdate(request,command_id):#REST API used by the client side of web application to load data for display
     myjson={}
     if command_id =="SS":#Command for sending one SMS
          #myjson={"MessageBody":"Hello. We wish you happy new year...","MobNo":"+255742340759"}
          myjson=json.loads(request.body)
          #myjson={}
          status=saveSMS(myjson)
          #myjson=json.JSONEncoder().encode(myjson)
          return HttpResponse('%s(%s)' % (request.GET.get('callback'),status), content_type='application/json')

     elif command_id =="SGD":#Command for saving groups' details
          myjson=json.loads(request.body)
          #myjson={}
          status=saveGroups(myjson)
          return HttpResponse('%s(%s)' % (request.GET.get('callback'),status), content_type='application/json')

     elif command_id =="SCD":#Command for saving campaigns' details
          myjson=json.loads(request.body)
          #myjson={}
          status=saveCampaigns(myjson)
          return HttpResponse('%s(%s)' % (request.GET.get('callback'),status), content_type='application/json')

     elif command_id =="UAF":
          myjson={"status": "file uploaded"}

          #addressfile = request.FILES['addressfile']
          #workbook = xlrd.open_workbook(addressfile)
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
                    col_headers=['contact_id','First Name','Middle Name','Last Name','Gender','DOB','Mobile Phone #1','Mobile Phone #2','Mobile Phone #3']
                    col_headers_order=[]
                    header_counter_on=0
                    col_header_counter=0

                    
                    

                    for row_posn in range(num_rows):

                         row=[]
                         col_counter=0
                         strcontent=""
                         for col_posn in range(num_columns):
                              cell= xl_sheet.cell(row_posn,col_posn)
                              strcontent="%s%s"%(strcontent,cell.value)
                              '''
                              if  (xl_sheet.cell_type(row_posn, col_posn) == xlrd.XL_CELL_EMPTY or xl_sheet.cell_type(row_posn,col_posn) == xlrd.XL_CELL_BLANK) and header_counter_on==0: 
                                   #Ignore all rows that have atleast one empty column and they are part of the header
                                   print "Ignored before header"
                                   break
                              elif xl_sheet.cell_type(row_posn, 0) == xlrd.XL_CELL_EMPTY or xl_sheet.cell_type(row_posn,col_posn) == xlrd.XL_CELL_BLANK:
                                   #deal with blanks after header
                                   print "Ignored after header"
                                   break
                              elif cell.value==col_headers[0] or cell.value==col_headers[1] or cell.value==col_headers[2] or cell.value==col_headers[3] or cell.value==col_headers[4] or cell.value==col_headers[5] or cell.value==col_headers[6] or cell.value==col_headers[7] or cell.value==col_headers[8]: #First check if the column is header, if it is header don't append
                                   if col_posn==0:
                                        header_counter_on=1 #This means we have started conting headers
                                   col_headers_order.append(cell.value) 
                                   col_header_counter=col_header_counter+1
                              else:
                                   #print "%s"%cell.value,
                                   row.append(cell.value)
                                   col_counter=col_counter+1
                         #Once we have counted all headers to match the number of column header then col_header counter will always be false meaning that no exception will be raised when dealing with records.
                         if col_header_counter<len(col_headers) and header_counter_on ==1 : #True if we had already started counting header, but the number we have counted has not reached the number of headers needed in a template
                              raise ValueError("Error: The column header format is not recognizable. Please use the downloaded template from the system")

                            '''
                        
                         #^(([',. - +]*[0-9]*[a-z]*)?)+$

                         str_reg_expr="^(?![\s\S])"


                         test_result=re.match(strcontent, str_reg_expr, re.IGNORECASE) # Now check if the string is non-empty

                         if test_result:
                              print "Empty encountered at row%s and str=%s"%(row_posn,strcontent)
                         else:
                              pass
                              

                         if col_counter==num_columns: #It means there were no empty columns in this row or the columns don't represent headers.
                              records.append(row)
                    if len(records)>0:
                         print records

                        


                              #There increment r









                    '''
                    row = xl_sheet.row(row_posn)  # 1st row
                    print row
                    for idx, cell_obj in enumerate(row):
                         cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
                         print('(%s) %s %s' % (idx, cell_type_str, cell_obj.value))

                    '''     

                    '''
                    while sentinal==1:
                         for i in range(max_columns):
                              strrow="Got here=%s"
                              if  xl_sheet.cell_type(row_posn, 0) == xlrd.XL_CELL_EMPTY or xl_sheet.cell_type(row_posn,0) == xlrd.XL_CELL_BLANK: 
                                   sentinal=0 # meaning that we have encountered blank somewhere hence there are probably no more records
                                   strrow="Got Deeper%s and cell value=%s"%(xl_sheet.cell_type(row_posn, 0),xl_sheet.cell(row_posn,i).value)
                                   break
                              cell= xl_sheet.cell(row_posn,i)
                              strrow="%s %s"%(strrow,cell.value)

                         strrow="%s \n"%strrow
                         row_posn+1 #Move to the next row

                    '''

                    myjson["status"]="%s"%strrow



                    os.remove(path) 

          except Exception as e:
                    myjson["status"]="%s failed. Reason: %s."%(myjson["status"],e)









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
          #return HttpResponse(alldata, content_type='application/json')
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
          font_style.num_format_str= "@"


          date_format = xlwt.XFStyle()
          date_format.num_format_str = 'dd/mm/yyyy'

          
          #ws.write(0, 0, "Mambo Yote SMS Address Book", font_style)
          #ws.write_merge(0, 1, 0, 8, "Mambo Yote SMS Address Book", font_style)
          ws.write_merge(0, 1, 0, 8, "Mambo Yote SMS Address Book",xlwt.easyxf("pattern: pattern solid, fore_color light_blue ; font: color white, height 320, bold True; align: horiz center; borders: top_color red, bottom_color red, right_color red, left_color red, left thin, right thin, top thin, bottom thin;"))
          
          columns = ['contact_id','First Name', 'Middle Name', 'Last Name', 'Gender','DOB',"Mobile Phone #1","Mobile Phone #2","Mobile Phone #3"]

          #font style for columns' headings
          font_style = xlwt.XFStyle()
          font_style.font.bold = True
          font_style.font.height = 280
          font_style.font.align="horiz center"

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

          rows = AddressBook.objects.all().values_list('contact_id','first_name', 'middle_name','last_name', 'gender','birth_date')
          
          for row in rows:
               row_num += 1
               last_column=0
               total_mobiles=0
               for col_num in range(len(row)):
                    if last_column==5:
                         #It means we dealing with date hence it should be formated as date
                         ws.write(row_num, col_num, row[col_num], date_format)
                    else:
                         ws.write(row_num, col_num, row[col_num], font_style)
                    last_column=last_column+1

               #Get all the mobile numbers for this contact     
               subrows=MobileDetails.objects.values_list('mobile_number').filter(contact_id=row[0])
               for subrow in subrows:
                    for col_num in range(len(subrow)):
                         ws.write(row_num, last_column, subrow[0], font_style)  
                         last_column=last_column+1

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
