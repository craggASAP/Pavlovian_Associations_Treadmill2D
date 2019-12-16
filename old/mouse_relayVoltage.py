#!/usr/bin/python

# adapted from mouse_relay_voltage.py on https://github.com/HanLabBU/movement_recording/blob/master/mouse_relay_voltage.py
import time
from threading import Thread, Lock
import Adafruit_MCP4725 # using the deprecated Adafruit Python MCP4725 library


# Declare variables
transmit_timer = None
data_lock = Lock()
ppm = 400.*25./63.5*100. # num pixels per meter - ish
maxv = 3.5 # max velocity (m/s)
transmit_delay = .01 #.01
read_delay = .001 #0.001
distCalib = 1./float(ppm)/transmit_delay/float(maxv)/2.
#distCalib = 1./float(ppm)/transmit_delay/float(maxv)

# initialize I2C buses (X: SDA 2 SC: 3; Y: SDA 17 SCL 27)
dacX = Adafruit_MCP4725.MCP4725(address=0x60,busnum=1)
dacY = Adafruit_MCP4725.MCP4725(address=0x60,busnum=3)
	

try:
	# distance calibration factor: what percent of maximum velocity?
	# so take # pixels / (pixels per meter) / (max velocity*transmit delay)
	# and let's make 0 = 50% = 1.65V
	
	# Dictionaries/structures containing data for each 'SENSOR'
	mouse1 = {
		'Name': '1',
		'File': file('/dev/input/mouse0'),
		'dx': 0,
		'dy': 0}

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
				dx = float(self.sensor['dx'])
				self.sensor['dx'] = 0
				dy = float(self.sensor['dy'])
				self.sensor['dy'] = 0
				data_lock.release()								
				# convert to a a voltage output (12byte so 2^12=4096) 
				dxout = int(4096*(.5+dx*distCalib))
				dyout = int(4096*(.5+dy*distCalib))
				#dxout = int(4096*abs(dx)*distCalib)
				#dyout = int(4096*abs(dy)*distCalib)
				dacX.set_voltage(dxout)
				dacY.set_voltage(dyout)
				
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
