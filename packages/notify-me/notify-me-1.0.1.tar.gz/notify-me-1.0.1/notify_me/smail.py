#! /usr/bin/python
import sys,Config
def send(to,subject,body,fromUser=None,cc="",bcc="",):

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    From=fromUser
    try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = From
            #msg['To'] = to one email
            msg['Cc']= cc
            if type(to)==type([]):
                msg['To'] = ', '.join( to) #More than one email
            else:
                msg['To'] = to
            html = body
            part2 = MIMEText(html, 'html')
            msg.attach(part2)
            server = smtplib.SMTP(Config.smtp_host,Config.smtp_port)
            server.ehlo()
            server.starttls()
            server.login(Config.smtp_user, Config.smtp_pass)
            server.sendmail(From, to, msg.as_string())
            if cc!="":
                server.sendmail(From, cc, msg.as_string())
            if bcc!="":
                server.sendmail(From, bcc, msg.as_string())
            server.quit()
	    print "Email Sent"
            return True

    except Exception as exp:
	import traceback
	print traceback.format_exc()
        return False

if __name__=="__main__":
	to=""
	subject="Job done"
	body=""
	fromUser="SGP Notifier<sgpbioinf@gmail.com>"
	cc=""
	bcc=""
	for arg in sys.argv[1:]:
		if "--to" in arg or "-t=" in arg:
			to=arg.split("=")[1]
		elif "--subject" in arg or "-s=" in arg:
                        subject=arg.split("=")[1]
		elif "--from" in arg or "-f=" in arg:
                        fromUser=arg.split("=")[1]
		elif "--body" in arg or "-b=" in arg:
                        body=arg.split("=")[1]
		else:
			print "Invalid Arg '%s'"%arg
			exit(-1)
	if body=="":
		body="<pre>"+"".join(sys.stdin.readlines())+"</pre>"

	send(to,subject,body,fromUser=None,cc="",bcc="",)
		
