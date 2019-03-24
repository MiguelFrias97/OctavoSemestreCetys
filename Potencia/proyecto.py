import smtplib
def sendMail(sender,to,subject,body):
	message =  """\
	From: %s
	To: %s
	Subject: %s

	%s

	""" % (sender,", ".join(to) if len(to)>1 else to[0],subject,body)

	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com',465)
		server.ehlo()
		server.login(sender,'ElectronicaPotencia')
		server.sendmail(sender,to,message)
	except:
		print('Not working ...')

if __name__=="__main__":
	sender = 'seguridad.potencia.ice@gmail.com'
	to = ['miguel.frias@cetys.edu.mx']
	subject = 'Testing mail'
	body = 'I am testing the mail function'

	sendMail(sender,to,subject,body)
