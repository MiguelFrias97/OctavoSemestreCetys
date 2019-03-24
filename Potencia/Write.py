import RPi.GPIO as gpio
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

try:
	text = raw_input('New data: ')
	print('Now place your tag to write')
	reader.write(text)
	print('Written')
finally:
	gpio.cleanup()
