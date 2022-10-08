import cv2
from getcontours import getContours
import numpy as np
import serial
from cup import cupdetect

ser = serial.Serial('', 9600)
state = 1

cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()
    imgcontours = frame.copy()
    resize = cv2.resize(frame, (640, 480))

    if(state == 0):
        getContours(resize, state)
        #detect shape, direction

    elif(state == 1):
        getContours(resize, state)
        #detectcolor
    
    elif(state == 2):
        getContours(resize, state)
        #fruitdetect

    elif(state == 3):
        getContours(resize, state)

    elif(state == 4):
        getContours(resize, state)

    elif(state == 5):
        getContours(resize, state)
        #getcolor

    elif(state == 6):
        getContours(resize, state)
        #waterspay
    
    elif(state == 7):
        getContours(resize, state)

    elif(state == 8):
        getContours(resize, state)

    elif(state == 9):
        getContours(resize, state)

    #use case
    



    





