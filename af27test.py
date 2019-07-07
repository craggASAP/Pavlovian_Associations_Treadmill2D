#!/usr/bin/python

# adapted from mouse_relay_voltage.py on https://github.com/HanLabBU/movement_recording/blob/master/mouse_relay_voltage.py
# note: run this using python 3
import time
from threading import Thread, Lock
import Adafruit_MCP4725 # using the deprecated Adafruit Python MCP4725 library

# initialize I2C buses (X: SDA 2 SC: 3; Y: SDA 17 SCL 27)
dacX = Adafruit_MCP4725.MCP4725(address=0x60,busnum=1)
dacY = Adafruit_MCP4725.MCP4725(address=0x60,busnum=3)
	

t = 1
t1 = time.time()


while 1:	
	while time.time()-t1<t:
		dxout = int(4096*0)
		dyout = int(4096*1)
		dacX.set_voltage(dxout)
		dacY.set_voltage(dyout)
	t1 = time.time()
	while time.time()-t1<t:
		dxout = int(4096*.5)
		dyout = int(4096*.5)
	t1 = time.time()
	while time.time()-t1<t:
		dxout = int(4096*1)
		dyout = int(4096*0)
	t1 = time.time()
	while time.time()-t1<t:
		dxout = int(4096*.5)
		dyout = int(4096*.5)
	t1 = time.time()
	

