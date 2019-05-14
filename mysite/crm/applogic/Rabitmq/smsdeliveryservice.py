#!/usr/bin/env python
import logging
from logging.handlers import SysLogHandler
import time
from service import find_syslog, Service

#import for code responsible for consuming messages from producers and send it out through SMS gateway 
import thread
import pika
import json
import urllib2,urllib


class SMSDeliveryService(Service):
	def __init__(self, *args, **kwargs):
		super(SMSDeliveryService, self).__init__(*args, **kwargs)
		self.logger.addHandler(SysLogHandler(address=find_syslog(),
		facility=SysLogHandler.LOG_DAEMON))
		self.logger.setLevel(logging.INFO)
	def run(self):
		if not self.got_sigterm():
			self.logger.info("I'm working...")
                        print "Working.."
			#time.sleep(5)
                        startMessageReceiver()
                else:
                        print "Not working"



if __name__ == '__main__':
	import sys
	if len(sys.argv) != 2:
		sys.exit('Syntax: %s COMMAND' % sys.argv[0])
	cmd = sys.argv[1].lower()
	service = SMSDeliveryService('my_service', pid_dir='/tmp')
        try:
		if cmd == 'start':
			service.start()
		elif cmd == 'stop':
			service.stop()
		elif cmd == 'status':
			if service.is_running():
		  		print "Service is running."
			else:
				print "Service is not running."
		else:
			sys.exit('Unknown command "%s".' % cmd)
	except Exception as e:
		print "Exception thrown: %s"%e




