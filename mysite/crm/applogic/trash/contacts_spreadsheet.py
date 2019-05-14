#import xlwt

class SupportingSpreadsheet:
	def __init__(self):
          pass
	
	def createWorkBook(self):
		book = xlwt.Workbook()

    	#sheet = book.add_sheet('Sheet 1')
    	#sheet.write(0, 0, 'sample')
    	#book.save('Sample.xls')




obj=SupportingSpreadsheet()
obj.createWorkBook()