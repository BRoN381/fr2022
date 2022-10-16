import numpy as np
import cv2
import serial
import threading
from time import sleep
from cup_detect import cupdetect

def run(cap):
    while True:
        ret, frame = cap.read()
        imgcontours = frame.copy()
        resize = cv2.resize(frame, (640, 480))
        sleep(0.2)
        cupdetect(resize)  
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

cap = cv2.VideoCapture(0)
counter = 0
motorThread = threading.Thread(target = run, args = (cap, ))

motorThread.start()

# Main Thread







