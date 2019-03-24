import smtplib
import RPi.GPIO as gpio

from threading import *

gpio.setmode(gpio.BOARD)

alarm = True
lock = Lock()

def sendMail(sender,to,subject,body):
	message =  """From: %s
To: %s
Subject: %s

%s
""" % (sender,', '.join(to) if len(to)>1 else to[0],subject,body)

	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com',465)
		server.ehlo()
		server.login(sender,'ElectronicaPotencia')
		server.sendmail(sender,to,message)
	except:
		print('Not working ...')

def alarming():
	## Configurando pines para sensores
	s1 = 29
	s2 = 31
	s3 = 33
	s4 = 35

	gpio.setup(s1,gpio.IN)
	gpio.setup(s2,gpio.IN)
	gpio.setup(s3,gpio.IN)
	gpio.setup(s4,gpio.IN)

	## Datos para realizar envio de correo
	sender = 'seguridad.potencia.ice@gmail.com'
	to = ['nataliab@cetys.edu.mx','ariana.landeros@cetys.edu.mx']
	subject = 'Testing mail'
	body = 'I am testing the mail function'

	if alarm and (gpio.input(s1) or gpio.input(s2) or gpio.input(s3) or gpio.input(s4))
		sendMail(sender,to,subject,body)

def disable():
	

if __name__ == "__main__":
	threads = []

	tAlarm = Thread(target=alarming)
	tAlarm.start()

	tDisable = Thread(target=disable)
	tDisable.start()
