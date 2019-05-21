import smtplib
import RPi.GPIO as gpio
import SimpleMFRC522
import time

from threading import *
from datetime import datetime
from datetime import timedelta

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

led_alarm = 20 # pin 38
gpio.setup(led_alarm,gpio.OUT)

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
			if alarm and (gpio.input(s1)) and abs(datetime.now()-lastSent).total_seconds() > deltatie:
				body = 'Estimado Usuario,\n\nLa alarma 1 ha sido activada con fecha ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.\n\nPara desactivarla contestar correo con la palabra "poisson". \n\nExcelente dia,Atte. Seguridad ICE'
				print('Se Activo alarma')
				sendMail(sender,to,subject,body)
				lastSent = datetime.now()
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

	for t in threads:
		t.join()
