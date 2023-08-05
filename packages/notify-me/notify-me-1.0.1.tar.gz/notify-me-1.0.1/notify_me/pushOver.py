import httplib, urllib
import Config
def push(message):
	print "PushOver running"
	if Config.pushOver_App!="":
		conn = httplib.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json",
		  urllib.urlencode({
			"token": Config.pushOver_App,
			"user": Config.pushOver_User,
			"message": message,
		  }), { "Content-type": "application/x-www-form-urlencoded" })
		return conn.getresponse()
	else:
		return "PushOver not enabled"
		
if __name__=="__main__":
	import sys
	push(sys.argv[1])
