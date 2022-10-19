import cv2
import numpy as np

frontCap = cv2.VideoCapture(0)
# sideCap = cv2.VideoCapture(1)
# bottomCap = cv2.VideoCapture(2)
while True:
    ret1, frontFrame = frontCap.read()
#     ret2, sideFrame = sideCap.read()
    # ret3, bottomFrame = bottomCap.read()
    if ret1:
        frontFrame = cv2.resize(frontFrame, (640, 480))
#         sideFrame = cv2.resize(sideFrame, (640, 480))
        # bottomFrame = cv2.resize(bottomFrame, (640, 480))
        # cv2.imshow('bottom', bottomFrame)
        cv2.imshow('front', frontFrame)
#         cv2.imshow('side', sideFrame)
    else:
        print('error')
    if cv2.waitKey(1)==ord("q"):
        break
frontCap.release()
# sideCap.release()
# bottomCap.release()
cv2.destroyAllWindows()
