import numpy as np
import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera


################ Setup
camera = PiCamera()
time.sleep(0.2)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

################ Functions
def get_frame():
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    frame = rawCapture.array
    return frame

def count_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)

    return str(len(faces))

if __name__ == '__main__':
    while True:
        frame = get_frame()
        faces_number = count_faces(frame)
        print(faces_number)
        time.sleep(1)
