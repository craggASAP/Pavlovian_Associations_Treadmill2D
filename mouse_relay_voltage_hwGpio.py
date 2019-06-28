#!/usr/bin/python

# adapted from mouse_relay_voltage.py on https://github.com/HanLabBU/movement_recording/blob/master/mouse_relay_voltage.py
# this uses hardware PWM, which can only be implemented on 2 dedicated pins, and so can only read input from a single mouse

import time
from threading import Thread, Lock
import pigpio
pi = pigpio.pi()

try:
	# distance calibration factor: 
	# 1 ball rotation is about 1000 mouse units
	# for now let's say that's 1/2 m
	# sampling rate is 100Hz (every 10ms)
	# let's make 100% = 1.5 m/s
	# so convert to m/s and then percentage of 1.25 m/s

	# can't send negative voltages, so let's have a pin 
	# sends 1 if it's negative, 0 otherwise

	pix_m = 2000
	maxv = 1.5
	

	# Dictionaries/structures containing data for each 'SENSOR'
	mouse1 = {
		'Name': '1',
		'File': file('/dev/input/mouse0'),
		'dx': 0,
		'dy': 0,
		'pinx': 18,
		'xsign': 5,
		'piny': 19,
		'ysign': 6}	
	# Declare variables
	transmit_timer = None
	data_lock = Lock()
	gpio_lock = Lock()

	transmit_delay = .01 #.01
	read_delay = .001 #0.001
	
	distCalib = 1/pix_m/transmit_delay/maxv
	print('mouse_relay.py: \n\tMain thread initialized\n\tDefining I/O threads\n')


	# SENDOUTPUTTHREAD - class for sending data as voltage (PWM) over gpio pins, subclass of Thread class
	class SendOutputThread(Thread):
		# Call parent (Thread) constructor with additional argument: SENSOR
		def __init__(self, sensor):
		        Thread.__init__(self)	        
		        self.sensor = sensor
		# Running code goes in 'run' method, called by obj.start() method
		def run(self):
			while True:
				# acquire and reset dx/dy data
				data_lock.acquire()
				dx = self.sensor['dx']				
				self.sensor['dx'] = 0
				dy = self.sensor['dy']
				self.sensor['dy'] = 0
				data_lock.release()								
				# convert to a percentage and write out to pins as % duty cycle
				pinx = self.sensor['pinx']
				signx = self.sensor['signx']
				piny = self.sensor['piny']
				signy = self.sensor['signy']							
				gpio_lock.acquire()		
				pi.hardware_PWM(pinx,800,1e6*min([abs(dx)*distCalib,1])) # make it 1 if it's over 1
				if dx<0: # if it's negative, send this pin
					pi.hardware_PWM(pinx,800,1e6)
				else:
					pi.hardware_PWM(signx,800,0)
				pi.hardware_PWM(signy,800,1e6*min([abs(dy*distCalib),1])) # make it 1 if it's over 1
				if dy<0: # if it's negative, send this pin
					pi.hardware_PWM(signy,800,1e6)
				else:
					pi.hardware_PWM(signy,800,0)
				gpio_lock.release()			
				# Delay for transmission period (10 msec)
				time.sleep(transmit_delay)		

	# READINPUTTHREAD - class to read raw input from linux /dev/mouseX files
	class ReadInputThread(Thread):
		# Call parent (Thread) constructor with additional argument: SENSOR
		def __init__(self, sensor):
		        Thread.__init__(self)	        
		        self.sensor = sensor
		# Running code goes in 'run' method, called by obj.start() method
		def run(self):
			while True:
				newdx = newdy = 0
				# Read raw values from mouse device file in linux filesystem
				dev_file = self.sensor['File']
				status, newdx, newdy = tuple(ord(c) for c in dev_file.read(3))
				# Define conversion to signed integer
				def to_signed(n):
					return n - ((0x80 & n) << 1)
				# Add accumulated readings
				if status:
#					print(status)
					data_lock.acquire()
					self.sensor['dx'] += to_signed(newdx)
					self.sensor['dy'] += to_signed(newdy)
					data_lock.release()
				time.sleep(read_delay)
#				print('dx' + str(self.sensor['dx']))
#				print('dy' + str(self.sensor['dy']))
	print('\tI/O threads defined\n\t...initializing now\n')
			
	# Begin a transmitting thread for each mouse: SEND_OUTPUT
	gpio_out_thread1 = SendOutputThread(mouse1)
	gpio_out_thread1.setName('thread_out_mouse1')
			
	# Begin the sensing thread for each mouse: READ_INPUT
	devread_in_thread1 = ReadInputThread(mouse1)
	devread_in_thread1.setName('thread_in_mouse1')
	print('\tThreads initialized... starting all threads now\n')

	# Start all threads
	gpio_out_thread1.start()
	devread_in_thread1.start()
			
	# Join all threads to prevent program exit
	gpio_out_thread1.join()
	devread_in_thread1.join()

except KeyboardInterrupt:
        print(e) 

else:
	print('\n\nShutting down safely...')
