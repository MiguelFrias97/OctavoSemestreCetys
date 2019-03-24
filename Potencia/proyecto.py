import smtplib
import RPi.GPIO as gpio
import SimpleMFRC522
import time

from threading import *

gpio.setmode(gpio.BCM)

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
	s1 = 5 # pin 29
	s2 = 6 # pin 31
	s3 = 13 # pin 33
	s4 = 19 # pin 35

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

def disable(dId,dPasswd):
	reader = SimpleMFRC522.SimpleMFRC522()

	try:
		id,text = reader.read()
		if dId == id and dPasswd == text:
			lock.acquire()
			alarm = False
			lock.release()

		time.sleep(5)

		lock.acquire()
		alarm = True
		lock.release()
	except:
		pass

if __name__ == "__main__":
	threads = []

	rfidId = ''
	rfidPasswd = ''

	tAlarm = Thread(target=alarming)
	tAlarm.start()

	tDisable = Thread(target=disable,args=(rfidID,rfidPasswd))
	tDisable.start()
