# Treadmill2D
Scripts for reading velocity from 2D treadmill ball using Raspberry Pi. Adapted from https://github.com/HanLabBU/movement_recording/mouse_relay_voltage.py

## NOTES
- this reads the x- and y-velocity from the optical mouse, and transmits it as a voltage (via PWM) via the raspberry pi output pins to be read directly via the NiDaq card
- Python 2.7
- pigpio (http://abyz.me.uk/rpi/pigpio/download.html)

## Scripts
### mouse_relay_display.py
- reads in mouse activity and displays dx and dy to the command prompt

### mouse_relay_voltage_hwGpio.py
- reads in mouse activity and sends out voltage using the hardware PWM pins (only 2 pins available: GPIO 18 and GPIO 19)

### mouse_relay_voltage_swGpio.py
- reads in mouse activity and sends out voltage using the software PWM pins (can be any GPIO, here GPIO 5, GPIO 6, GPIO 22, and GPIO 27)
  



