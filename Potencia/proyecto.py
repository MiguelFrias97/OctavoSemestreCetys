import smtplib
import RPi.GPIO as gpio
import SimpleMFRC522
import time

from threading import *
from datetime import datetime
from datetime import timedelta

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

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
	deltatie = 10
	lastSent = datetime.now() - timedelta(seconds=deltatie)
	while True:
		try:
			## Configurando pines para sensores
			s1 = 16
			s2 = 20
			s3 = 21
			s4 = 26

			gpio.setup(s1,gpio.IN)
			gpio.setup(s2,gpio.IN)
			gpio.setup(s3,gpio.IN)
			gpio.setup(s4,gpio.IN)

			## Datos para realizar envio de correo
			sender = 'seguridad.potencia.ice@gmail.com'
			to = ['miguel.frias@cetys.edu.mx','nataliab@cetys.edu.mx','ariana.landeros@cetys.edu.mx']
			subject = 'Testing mail'
			body = 'I am testing the mail function'

			print(alarm)
			if alarm and (gpio.input(s1) or gpio.input(s2) or gpio.input(s3) or gpio.input(s4)) and abs(datetime.now()-lastSent).total_seconds() > deltatie:
				sendMail(sender,to,subject,body)
				lastSent = datetime.now()
				print('Sent message')
		except KeyboardInterrupt:
			break
		except:
			print('Error sending message')

def disable(dId,dPasswd):
	while True:
		reader = SimpleMFRC522.SimpleMFRC522()

		try:
			id,text = reader.read()
			print(str(id).strip(),'  ',text.strip())
			if dId == str(id).strip() and dPasswd == text.strip():
				lock.acquire()
				alarm = False
				lock.release()
				print('Disabled alarm')

				time.sleep(120)

				print('Active alarm')
				lock.acquire()
				alarm = True
				lock.release()
		except KeyboardInterrupt:
			break
		except:
			print('Error leyendo rfid')

if __name__ == '__main__':
	rfidId = '94376169919'
	rfidPasswd = 'IWWTTFS2019'

	threads = []

	#alarming()
	tAlarm = Thread(target=alarming)
	tAlarm.start()

	tDisable = Thread(target=disable,args=(rfidId,rfidPasswd))
	tDisable.start()

