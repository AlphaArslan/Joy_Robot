import numpy as np
import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from smbus2 import SMBus


################ Setup
camera = PiCamera()
time.sleep(0.2)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

bus = SMBus(1)
address = 0x04
ONE_FACE_CODE = 1
TWO_FACE_CODE = 2

################ Functions
def get_frame():
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    frame = rawCapture.array
    return frame

def count_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    return len(faces)

def send_command(faces = 0):
    if faces is not 0 :
        if faces is 1 :
            bus.write_byte(address, ONE_FACE_CODE)
        elif faces is 2:
            bus.write_byte(address, TWO_FACE_CODE)

if __name__ == '__main__':
    while True:
        frame = get_frame()
        faces_number = count_faces(frame)
        send_command(faces = faces_number)
        print(faces_number)
        time.sleep(1)
