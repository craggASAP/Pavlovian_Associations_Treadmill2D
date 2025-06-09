# Supplemental Phyton Code for "Distinct spatially organized striatum-wide acetylcholine dynamics for the learning and extinction of Pavlovian associations"

------------------
## Contents
* [Project Overview](#project-overview)
* [File Structure](#file-structure)
* [Data Availability](#data-availability)
* [System Requirements](#system-requirements)
* [License and citation](#license-and-citation)
* [Acknowledgements](#acknowledgements)

------------------
## Project Overview

This repository contains scripts for reading velocity from 2D treadmill ball using Raspberry Pi. The scripts read the x- and y-velocity from the optical mouse, transmits it as a voltage via the raspberry pi output pins to be converted through the DAC MCP4725 and then read into Matlab via the NiDaq card. These scripts were adapted from [Han Lab](https://github.com/HanLabBU/movement_recording/mouse_relay_voltage.py) and used in the study [Distinct spatially organized striatum-wide acetylcholine dynamics for the learning and extinction of Pavlovian associations.](https://www.nature.com/articles/s41467-025-60462-5).

------------------
## File Structure

The following files are included in this repository:

### mouse_display_mouse0.py
- reads in mouse activity from /dev/input/mouse0 and displays dx and dy to the command prompt

### mouse_display_mouse1.py
- reads in mouse activity from /dev/input/mouse1 and displays dx and dy to the command prompt

### mouse_relayVoltage2_mouse0.py
- reads in mouse activity from /dev/input/mouse0 and sends out voltage using the I2C buses (to output to digital-to-analog converter MCP4725). Note that this uses the Raspberry Pi's I2C built-in I2C bus, as well as an added one on GPIO17 and GPIO27. Output is 0-3.3V, absolute value of velocity multipled by a conversion factor to convert to voltage. The sign (+/-) gets output separately via a digital pin (0=neg, 1=pos).

### mouse_relayVoltage2_mouse1.py
- reads in mouse activity from /dev/input/mouse1 and sends out voltage using the I2C buses (to output to digital-to-analog converter MCP4725). Note that this uses the Raspberry Pi's I2C built-in I2C bus, as well as an added one on GPIO17 and GPIO27. Output is 0-3.3V, absolute value of velocity multipled by a conversion factor to convert to voltage. The sign (+/-) gets output separately via a digital pin (0=neg, 1=pos).

------------------
## Data Availability

Both raw datasets and processed and organized datasets are available at [Zenodo](https://zenodo.org/records/14728851) in separate .zip folders for each figure.

------------------
## System Requirements

Any operating system able of running Phyton 2.7. 

**Hardware requirement** : Run these scripts on the Raspberry Pi.

**Software requirement**:  Phyton can be installed on machines running Windows, macOS or Linux. Install [Adafruit Python MCP4725 Library](https://github.com/adafruit/Adafruit_Python_MCP4725). 

------------------
##  License and Citation
 
If you use use this code in your research, please cite: 

Safa Bouabid, Liangzhu Zhang, Mai-Anh T. Vu, Kylie Tang, Benjamin M. Graham , Christian A. Noggle, Mark W. Howe. (2025) [Distinct spatially organized striatum-wide acetylcholine dynamics for the learning and extinction of Pavlovian associations.](https://www.nature.com/articles/s41467-025-60462-5).

This repository is released under the [MIT License](https://opensource.org/license/mit) - see the [LICENSE](LICENSE) file for details.

------------------
## Acknowledgements

This research was funded in part by Aligning Science Across Parkinson’s **[ASAP-020370]** through the Michael J. Fox Foundation for Parkinson’s Research (MJFF).

