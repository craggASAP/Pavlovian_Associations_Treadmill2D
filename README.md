# Treadmill2D
Scripts for reading velocity from 2D treadmill ball using Raspberry Pi. Adapted from https://github.com/HanLabBU/movement_recording/mouse_relay_voltage.py. Reads the x- and y-velocity from the optical mouse, and transmits it as a voltage (via PWM) via the raspberry pi output pins to be read directly via the NiDaq card

## NOTES
- Put these scripts on the Raspberry Pi
- Python 2.7
- Download/install pigpio (http://abyz.me.uk/rpi/pigpio/download.html)

## Scripts
### mouse_display.py
- reads in mouse activity and displays dx and dy to the command prompt

### mouse_relayVoltage.py
- reads in mouse activity and sends out voltage using the I2C buses (to output to digital-to-analog converter MCP4725). Note that this uses the Raspberry Pi's I2C built-in I2C bus, as well as an added one on GPIO17 and GPIO27. Output is 0-3.3V, with 0 set as 1.65V, and a conversion factor to convert velocity to a voltage.

### mouse_relayVoltage2.py
- reads in mouse activity and sends out voltage using the I2C buses (to output to digital-to-analog converter MCP4725). Note that this uses the Raspberry Pi's I2C built-in I2C bus, as well as an added one on GPIO17 and GPIO27. Output is 0-3.3V, absolute value of velocity multipled by a conversion factor to convert to voltage. The sign (+/-) gets output separately via a digital pin (0=neg, 1=pos).



