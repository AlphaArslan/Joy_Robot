import numpy as np
import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from smbus2 import SMBus
from adafruit_servokit import ServoKit

################ constants
SALUT_DELAY       = 2                              # in seconds
# I2C address
ARDUINO_ADDRESS   = 0x04

# servo angles
SALUT_RU_ANGLE    = 90                             # Right upper servo angle for SALUT move
SALUT_RL_ANGLE    = 45                             # Right Lower servo angle for SALUT move
SALUT_LU_ANGLE    = 90                             # Left upper servo angle for SALUT move
SALUT_LL_ANGLE    = 135                            # Left Lower servo angle for SALUT move

DEFAULT_RU_ANGLE    = 0
DEFAULT_RL_ANGLE    = 0
DEFAULT_LU_ANGLE    = 180
DEFAULT_LL_ANGLE    = 180

# servo channel number
RIGHT_UPPER_SERVO = 1
RIGHT_LOWER_SERVO = 2
LEFT_UPPER_SERVO  = 3
LEFT_LOWER_SERVO  = 4
HEAD_HOR_SERVO    = 5                              # horizontal
HEAD_VER_SERVO    = 6                              # vertical

# Head Movement
RIGHT_EDGE        = 50
LEFT_EDGE         = 450
HEAD_HOR_SPAN     = 70
DEFAULT_HH_ANGLE  = 90
DEFAULT_HV_ANGLE  = 90

################ Setup
camera = PiCamera()
time.sleep(0.2)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

bus = SMBus(1)
ONE_FACE_CODE = 1
TWO_FACE_CODE = 2

kit = ServoKit(channels=16)

# reset servos
kit.servo[RIGHT_UPPER_SERVO].angle = DEFAULT_RU_ANGLE
kit.servo[LEFT_UPPER_SERVO].angle  = DEFAULT_LU_ANGLE
kit.servo[RIGHT_LOWER_SERVO].angle = DEFAULT_RL_ANGLE
kit.servo[LEFT_LOWER_SERVO].angle  = DEFAULT_LL_ANGLE


################ Functions
def get_frame():
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    frame = rawCapture.array
    return frame

def find_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    return faces

def send_command(faces_number):
    if faces_number is not 0 :
        bus.write_byte(ARDUINO_ADDRESS, ONE_FACE_CODE)
        
def move_servos(faces):
    if len(faces) is 1:
        x = faces[0][2] /2 + faces[0][2] /2
        angle = translate(x, RIGHT_EDGE, LEFT_EDGE, DEFAULT_HH_ANGLE - HEAD_HOR_SPAN, DEFAULT_HH_ANGLE + HEAD_HOR_SPAN)
        kit.servo[HEAD_HOR_SERVO].angle    = angle
        kit.servo[HEAD_VER_SERVO].angle    = 60

        kit.servo[RIGHT_UPPER_SERVO].angle = SALUT_RU_ANGLE
        kit.servo[RIGHT_LOWER_SERVO].angle = SALUT_LU_ANGLE
        time.sleep(SALUT_DELAY)
        kit.servo[RIGHT_UPPER_SERVO].angle = DEFAULT_RU_ANGLE
        kit.servo[RIGHT_LOWER_SERVO].angle = DEFAULT_RL_ANGLE

        kit.servo[HEAD_HOR_SERVO].angle    = DEFAULT_HH_ANGLE
        kit.servo[HEAD_VER_SERVO].angle    = DEFAULT_HV_ANGLE

    elif len(faces) > 1:
        x = faces[0][2] /2 + faces[0][2] /2
        angle = translate(x, RIGHT_EDGE, LEFT_EDGE, DEFAULT_HH_ANGLE - HEAD_HOR_SPAN, DEFAULT_HH_ANGLE + HEAD_HOR_SPAN)
        kit.servo[HEAD_HOR_SERVO].angle    = angle
        kit.servo[HEAD_VER_SERVO].angle    = 60

        kit.servo[RIGHT_UPPER_SERVO].angle = SALUT_RU_ANGLE
        kit.servo[LEFT_UPPER_SERVO].angle  = SALUT_LU_ANGLE
        kit.servo[RIGHT_LOWER_SERVO].angle = SALUT_RL_ANGLE
        kit.servo[LEFT_LOWER_SERVO].angle  = SALUT_LL_ANGLE
        time.sleep(SALUT_DELAY)
        kit.servo[RIGHT_UPPER_SERVO].angle = DEFAULT_RU_ANGLE
        kit.servo[LEFT_UPPER_SERVO].angle  = DEFAULT_LU_ANGLE
        kit.servo[RIGHT_LOWER_SERVO].angle = DEFAULT_RL_ANGLE
        kit.servo[LEFT_LOWER_SERVO].angle  = DEFAULT_LL_ANGLE

        kit.servo[HEAD_HOR_SERVO].angle    = DEFAULT_HH_ANGLE
        kit.servo[HEAD_VER_SERVO].angle    = DEFAULT_HV_ANGLE

def translate(value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        valueScaled = float(value - leftMin) / float(leftSpan)

        return rightMin + (valueScaled * rightSpan)

################ Main
if __name__ == '__main__':
    while True:
        frame = get_frame()
        faces = find_faces(frame)
        faces_number = len(faces)
        print(faces_number)
        try:
            send_command(faces_number)
        except:
            print("Error Sending command to Arduino")
        try:
            move_servos(faces)
        except:
            print("Error Sending command to Servos")
        time.sleep(1)
