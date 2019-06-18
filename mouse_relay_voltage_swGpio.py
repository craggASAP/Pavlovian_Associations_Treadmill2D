#!/usr/bin/python

# adapted from mouse_relay_voltage.py on https://github.com/HanLabBU/movement_recording/blob/master/mouse_relay_voltage.py
# this uses software PWM, which can be implemented on any GPIO pin, so can read input from multiple mice

import time
from threading import Thread, Lock
import pigpio
pi = pigpio.pi()

try:
	# distance calibration factor: 
	# let's say it's like 2500 pixels/m 
	# sampling rate is 100Hz (every 10ms)
	# let's make 100% = 1.25 m/s
	# so convert to m/s and then percentage of 1.25 m/s
	pix_m = 2500
	sr = 100
	maxv = 1.25
	distCalib = 1/pix_m*sr/1.25
	
	# Dictionaries/structures containing data for each 'SENSOR'
	mouse1 = {
		'Name': '1',
		'File': file('/dev/input/mouse0'),
		'dx': 0,
		'dy': 0,
		'pinx': 27,
		'piny': 22}
	mouse2 = {
		'Name': '2',
		'File': file('/dev/input/mouse1'),
		'dx': 0,
		'dy': 0,
		'pinx': 5,
		'piny': 6}
	# Declare variables
	transmit_timer = None
	data_lock = Lock()
	gpio_lock = Lock()

	transmit_delay = .001 #.01
	read_delay = .001 #0.001
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
				piny = self.sensor['piny']							
				gpio_lock.acquire()			
				pi.set_PWM_dutycycle(pinx,255*dx*distCalib)
				pi.set_PWM_dutycycle(piny,255*dy*distCalib)																																																									
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
				print('dx' + str(self.sensor['dx']))
				print('dy' + str(self.sensor['dy']))
	print('\tI/O threads defined\n\t...initializing now\n')
			
	# Begin a transmitting thread for each mouse: SEND_OUTPUT
	gpio_out_thread1 = SendOutputThread(mouse1)
	gpio_out_thread2 = SendOutputThread(mouse2)
	gpio_out_thread1.setName('thread_out_mouse1')
	gpio_out_thread2.setName('thread_out_mouse2')
			
	# Begin the sensing thread for each mouse: READ_INPUT
	devread_in_thread1 = ReadInputThread(mouse1)
	devread_in_thread2 = ReadInputThread(mouse2)
	devread_in_thread1.setName('thread_in_mouse1')
	devread_in_thread2.setName('thread_in_mouse2')
	print('\tThreads initialized... starting all threads now\n')

	# Start all threads
	gpio_out_thread1.start()
	gpio_out_thread2.start()
	devread_in_thread1.start()
	devread_in_thread2.start()
			
	# Join all threads to prevent program exit
	gpio_out_thread1.join()
	gpio_out_thread2.join()
	devread_in_thread1.join()
	devread_in_thread2.join()

except KeyboardInterrupt:
        print(e) 

else:
	print('\n\nShutting down safely...')
