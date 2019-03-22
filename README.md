# Joy Robot
---
---
## Consists of:
##### 1. Raspberry Pi One:
 * Responsible for the __Face Recognition__ operations.
 * Runs __Raspbain OS__.
 * Connects to a camera module.
 * I2C bus master.

##### 2. Raspberry Pi Two:
  * Responsible for the __Voice Commands__.
  * Run __AIY Raspbain__ provided by _Google_ [here](https://github.com/google/aiyprojects-raspbian/releases)
  * Connects to _Google AIY Kit_
  * Controls DC motors

##### 3. Arduino Mega:
  * Controls _Led Matrix_.
  * Takes Commands from Raspberry Pi One through I2C.

---
## Setup
###  - Raspberry Pi One [Face Detection]
##### 1. Enable Camera module:
> sudo raspi-config

then go to interfaces and enable camera module

> reboot

##### 2. Enable I2C Interface
> sudo raspi-config

Go to Interfacing Options
Choose I2C and Enable it

##### 3. Installing Python Library:

> sudo pip3 install numpy

> sudo pip3 install opencv-python

> sudo pip3 install "picamera[array]"

> sudo pip3 install smbus2

> sudo pip3 install adafruit-circuitpython-servokit

##### 4. System packages
> sudo apt-get install libjasper-dev

> sudo apt-get install openexr

> sudo apt-get install libwebp-dev

> sudo apt-get install libjpeg-dev libpng-dev libtiff-dev

> sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev

> sudo apt-get install libxvidcore-dev libx264-dev

> sudo apt-get install libgtk-3-dev

> sudo apt-get install libcanberra-gtk*

> sudo apt-get install libatlas-base-dev gfortran

> sudo apt-get install libqt4-dev

##### 5. Add to startup
_Raspberry Pi One_

_rename the project folder to "project"_

>chmod 755 launcher.sh

test the launcher
>sh launcher.sh

open _crontab_
>sudo crontab -e

add this line at the end
>@reboot sh /home/pi/project/launcher.sh &

reboot
>reboot
