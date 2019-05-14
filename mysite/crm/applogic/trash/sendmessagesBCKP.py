import urllib2,urllib


values = {'user' : 'wellnessapp',
          'password' : 'AbGXWETGaKdEdD',
          'api_id' : '3543084',
           'to':'27738472538',
           'text':'Sending message with python'}

url="http://api.clickatell.com/http/sendmsg?"+urllib.urlencode(values)


req = urllib2.Request(url)
req.add_header("User-Agent",'Mozilla/5.0')

req.add_header("Content-type",'application/x-www-form-urlencoded')

page = urllib2.urlopen(req)
print page.info()

page.close()
#response = urllib2.urlopen('http://www.pythonforbeginners.com/')
#print response.info()
#html = response.read()
# do something
#response.close()  # best practice to close the file
