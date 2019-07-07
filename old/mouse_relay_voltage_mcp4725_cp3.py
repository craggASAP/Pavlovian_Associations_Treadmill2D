#!/usr/bin/python

# adapted from mouse_relay_voltage.py on https://github.com/HanLabBU/movement_recording/blob/master/mouse_relay_voltage.py
# using: 
# python3
# bitbangio (instead of busio so we can use software I2C)
# Adafruit_CircuitPython_MCP4725 library
# ran into issues using bitbangio: no module named 'machine'

import time
from threading import Thread, Lock
import bitbangio
import adafruit_mcp4725

try:
	# distance calibration factor: what percent of maximum velocity?
	# so take # pixels / (pixels per meter) / (max velocity*transmit delay)
	# and let's make 0 = 50% = 1.65V
	
	# Dictionaries/structures containing data for each 'SENSOR'
	mouse = {
		'Name': '1',
		'File': open('/dev/input/mouse0'),
		'dx': 0,
		'dy': 0,
		'xbusSDA': 2,
		'xbusSCL': 3,
		'ybusSDA': 17,
		'ybusSCL': 27}
	
	# initialize I2C buses (X: SDA 2 SC: 3; Y: SDA 17 SCL 27)
	i2cX = bitbangio.I2C(3,2)
	i2cY = bitbangio.I2C(27,17)
	
	# initialize MCP4725
	dacX = adafruit_mcp4725(i2cX)
	dacY = adafruit_mcp4725(i2cY)
		
	# Declare variables
	transmit_timer = None
	data_lock = Lock()
	ppm = 3937 # num pixels per meter
	maxv = 1.5 # max velocity (m/s)
	transmit_delay = .01 #.01
	read_delay = .001 #0.001
	distCalib = 1/ppm/transmit_delay/maxv/2

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
				# convert to a percentage and write out to pins as normalized value (0-1.0)
				dxout = .5+dx*distCalib
				dyout = .5+dy*distCalib				
				dacX.normalized_value = dxout
				dacY.normalized_value = dyout
				
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
