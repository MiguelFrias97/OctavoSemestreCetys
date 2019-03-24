import RPi.GPIO as gpio
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

try:
	id,text = reader.read()
	print(id)
	print(text)
finally:
	gpio.cleanup()
