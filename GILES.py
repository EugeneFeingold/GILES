#!/usr/bin/python

import time
import serial
import pygame
import RPi.GPIO as GPIO
from pygame.locals import *

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.output(18, GPIO.LOW)

initSuccess = False
while not initSuccess:
    try:
        pygame.init()
        j = pygame.joystick.Joystick(0)
        j.init()
        if not (j is None):
            initSuccess = True
    except:
        initSuccess = False


port = serial.Serial("/dev/ttyAMA0", baudrate=38400, timeout=3.0)
port.write(chr(64))
port.write(chr(192))

prevm1 = 0
prevm2 = 0

GPIO.output(18, GPIO.HIGH)

while True:
	try:
		for event in pygame.event.get():
			try:
				if event.type == QUIT:
					port.write(chr(64))
					port.write(chr(192))
					pygame.quit()

				maxspeed = 18.0

				m1 = int(j.get_axis(0)*maxspeed)
				m2 = int(j.get_axis(1)*maxspeed)
				
				print "COORD: %s %s" % (str(m1), (m2))

				port.write(chr(64 + m1))
				port.write(chr(192 + m2))
			except:
				print "exception!!!"
				GPIO.output(18, GPIO.LOW)
				port.write(chr(64))
				port.write(chr(192))
				exit()
	except:
		print "double exception!!!"
		port.write(chr(64))
		port.write(chr(192))
		GPIO.output(18, GPIO.LOW)
		exit()