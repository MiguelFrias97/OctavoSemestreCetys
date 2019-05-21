import smtplib
import RPi.GPIO as gpio
import SimpleMFRC522
import time
import re

from threading import *
from datetime import datetime
from datetime import timedelta
from readEmail import *

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

led_alarm = 20 # pin 38
gpio.setup(led_alarm,gpio.OUT)

alarm = True
lock = Lock()
lock_isActive = Lock()
active = False ## Esta variable indica si alguien paso por la puerta y activo la alarma

def readMail():
	global lock
	global active

	reactive = 16 # pin 36
	gpio.setup(reactive,gpio.OUT,initial=gpio.HIGH)

	while True:
		try:
			mail = FetchEmail('imap.gmail.com','seguridad.potencia.ice@gmail.com','ElectronicaPotencia')
			mails = mail.fetch_unread_messages()

			responses = {}
			index = 1
			for m in mails:
				r = []
				if m.is_multipart():
					for payload in m.get_payload():
						r.append(payload.get_payload())
				else:
					r.append(payload.get_payload())
			responses['correo'+str(index)] = r
			index += 1

			for key in responses:
				body = responses[key][0]
				print(body)
				if active and len(re.findall(r'Desactivar Alarma Poisson',body)):
					print('Si se armo')
					gpio.output(reactive,gpio.LOW)
					time.sleep(1)
					gpio.output(reactive,gpio.HIGH)
					lock.acquire()
					active = False
					lock.release()
			mail.close()
			time.sleep(1)
		except KeyboardInterrupt:
			break
		except:
			pass

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
	global alarm
	global lock
	global led_alarm

	deltatie = 10
	lastSent = datetime.now() - timedelta(seconds=deltatie)

	s1 = 21 # pin 40
	gpio.setup(s1,gpio.IN)

	gpio.output(led_alarm,gpio.HIGH)

	## Datos para realizar envio de correo
	sender = 'seguridad.potencia.ice@gmail.com'
	to = ['miguel.frias@cetys.edu.mx','nataliab@cetys.edu.mx','ariana.landeros@cetys.edu.mx']
	subject = 'Alarm Notification Mail'

	while True:
		try:
			if alarm and not(active)  and (gpio.input(s1)) and abs(datetime.now()-lastSent).total_seconds() > deltatie:
				body = 'Estimado Usuario,\n\nLa alarma 1 ha sido activada con fecha ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.\n\nPara desactivarla contestar correo con la palabra "poisson". \n\nExcelente dia,\nAtte. Seguridad ICE'
				print('Se Activo alarma')
				sendMail(sender,to,subject,body)
				lastSent = datetime.now()
				print('Sent message')
				lock.acquire()
				active = True
				lock.release()
		except KeyboardInterrupt:
			break
		except:
			print('Error sending message')

def disable(dId,dPasswd):
	global alarm
	global lock
	global led_alarm

	reader = SimpleMFRC522.SimpleMFRC522()
	while True:
		try:
			id,text = reader.read()
			print(str(id).strip(),'  ',text.strip())
			if dId == str(id).strip() and dPasswd == text.strip():
				lock.acquire()
				alarm = False
				lock.release()
				gpio.output(led_alarm,gpio.LOW)
				print('Disabled alarm')

				time.sleep(120)

				print('Active alarm')
				lock.acquire()
				alarm = True
				lock.release()
				gpio.output(led_alarm,gpio.HIGH)
		except KeyboardInterrupt:
			break
		except:
			print('Error leyendo rfid')

def disableIndoor():
	global alarm
	global lock
	global led_alarm

	disable = 12
	gpio.setup(disable,gpio.IN)
	while True:
		try:
			if gpio.input(disable):
				lock.acquire()
				alarm = False
				lock.release()
				gpio.output(led_alarm,gpio.LOW)
				print('Disabled alarm')

				time.sleep(120)

				print('Active alarm')
				lock.acquire()
				alarm = True
				lock.release()
				gpio.output(led_alarm,gpio.HIGH)
		except KeyboardInterrupt:
			break
		except:
			print('Error con la sedactivacion indoor')



if __name__ == '__main__':
	rfidId = '94376169919'
	rfidPasswd = 'IWWTTFS2019'

	threads = []

	tAlarm = Thread(target=alarming)
	threads.append(tAlarm)
	tAlarm.start()

	tDisable = Thread(target=disable,args=(rfidId,rfidPasswd))
	threads.append(tDisable)
	tDisable.start()

	tDisableIndoor = Thread(target=disableIndoor)
	threads.append(tDisableIndoor)
	tDisableIndoor.start()

	tReadMail = Thread(target=readMail)
	threads.append(tReadMail)
	tReadMail.start()

	for t in threads:
		t.join()
