# Joy Robot
---
---
## Consists of:
##### 1. Raspberry Pi One:
 * Responsible for the __Face Recognition__ operations.
 * Runs __Raspbain OS__.
 * Connects to a camera module.
 * Communicates with Arduino Mega using I2C

##### 2. Raspberry Pi Two:
  * Responsible for the __Voice Commands__.
  * Run __AIY Raspbain__ provided by _Google_ [here](https://github.com/google/aiyprojects-raspbian/releases)
  * Connects to _Google AIY Kit_
  * Controls DC motors

##### 3. Arduino Mega:
  * Controls _servos_ and _Led Matrix_.
  * Takes Commands from Raspberry Pi One through I2C.

---
## Setup
#### Raspberry Pi One [Face Detection]
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

##### 4. additional packages [Recommended]
> sudo apt-get install libpng-devel

> sudo apt-get install libjpeg-turbo-devel

> sudo apt-get install jasper-devel

> sudo apt-get install openexr-devel

> sudo apt-get install libtiff-devel

> sudo apt-get install libwebp-devel




---
---
# I2C Communication scheme
<!-- Table1 -->
|   Code   | meaning            |
| -------- | ------------------ |
| 1        | One face detected  |
| 2        | Two Faces detected |
