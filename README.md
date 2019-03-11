# Joy Robot
---
---
## Consists of:
##### 1. Raspberry Pi One:
 * Responsible for the __Face Recognition__ operations.
 * Runs __Raspbain OS__.
 * Connects to a camera module.

##### 2. Raspberry Pi Two:
  * Responsible for the __Voice Commands__.
  * Run __AIY Raspbain__ provided by _Google_ [here](https://github.com/google/aiyprojects-raspbian/releases)
  * Connects to _Google AIY Kit_

##### 3. Arduino Mega:
  * Controls _servos_ and _DC motors_.
  * Communicates with Raspberry Pi One & Two.

---
## Setup
#### Raspberry Pi One [Face Detection]
##### 1. Enable Camera module:
> sudo raspi-config

then go to interfaces and enable camera module

> reboot

##### 2. Installing Python Library:

> sudo pip3 install numpy

> sudo pip3 install opencv-python

> pip install "picamera[array]"
