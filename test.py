#!/usr/bin/python

# adapted from mouse_relay_voltage.py on https://github.com/HanLabBU/movement_recording/blob/master/mouse_relay_voltage.py
# this uses hardware PWM, which can only be implemented on 2 dedicated pins, and so can only read input from a single mouse

import time
from threading import Thread, Lock
import pigpio
pi = pigpio.pi()
t1 = time.time()
t = 1

while 1:	
	while time.time()-t1<t:
		pi.hardware_PWM(18,800,1e6)
		pi.hardware_PWM(19,800,1e6*.5)
	t1 = time.time()
	while time.time()-t1<t:
		pi.hardware_PWM(18,800,1e6*.25)
		pi.hardware_PWM(19,800,1e6)
	t1 = time.time()
	

