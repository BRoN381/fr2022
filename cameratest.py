import cv2
import numpy as np

frontCap = cv2.VideoCapture(0)
sideCap = cv2.VideoCapture(1)

while True:
	ret1, frontFrame = frontCap.read()
	ret2, sideFrame = sideCap.read()
	frontFrame = cv2.resize(frontFrame, (640, 480))
	frontFrame = cv2.flip(frontFrame, -1)
	sideFrame = cv2.resize(sideFrame, (640, 480))
	if ret1:
		cv2.imshow('front', frontFrame)
		cv2.imshow('side', sideFrame)
	else:
		print('error')
	if cv2.waitKey(1)==ord("q"):
		break
frontCap.release()
sideCap.release()
cv2.destroyAllWindows()
