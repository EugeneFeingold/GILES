#!/usr/bin/python



import cwiid
import time
import serial


port = serial.Serial("/dev/ttyAMA0", baudrate=38400, timeout=3.0)
port.write(chr(64))
port.write(chr(192))


#connecting to the Wiimote. This allows several attempts 
# as first few often fail. 
print 'Press 1+2 on your Wiimote now...' 
wm = None 
i=2 
while not wm: 
  try: 
    wm=cwiid.Wiimote() 
  except RuntimeError: 
    if (i>10): 
      quit() 
      break 
    print "Error opening wiimote connection" 
    print "attempt " + str(i) 
    i +=1 

print "CONNECTED!"

wm.rpt_mode = cwiid.RPT_BTN
wm.led = 1

prevm1 = 0
prevm2 = 0


while True:
	try:
		m1 = 0
		m2 = 0
		mult = 1
	
		buttons = wm.state['buttons']
		if (buttons & cwiid.BTN_B):
			print "B"
			mult = 2
		
		if (buttons & cwiid.BTN_1):
			print "1"
			m1 = m1 + 31
			m2 = m2 + 31 
		
		if (buttons & cwiid.BTN_2):
			print "2"
			m1 = m1 - 31
			m2 = m2 - 31
		
		if (buttons & cwiid.BTN_UP):
			print "up"
			m1 = m1 - 16
			m2 = m2 + 16
		
		if (buttons & cwiid.BTN_DOWN):
			print "down"
			m1 = m1 + 16
			m2 = m2 - 16
		
		m1 = min(m1, 63)
		m1 = max(m1, -63)
		m2 = min(m2, 63)
		m2 = max(m2, -63)
		
		m1 = m1 * mult
		m2 = m2 * mult
	
		m1 = prevm1 + (prevm1 - m1) / 2
		m2 = prevm2 + (prevm2 - m2) / 2
	
		port.write(chr(64 + m1))
		port.write(chr(192 + m2))
	except:
		port.write(chr(64))
		port.write(chr(192))
  
  
  
