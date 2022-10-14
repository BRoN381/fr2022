import cv2
import numpy as np
waterCap = cv2.VideoCapture(0)
maskLowwerBound = [[  3,177,164], [  0,  85,  67], [  0,121,121], [  0,158,192], [ 12,184, 91], [ 95, 49,83], [  0,  0,  0]]
maskUpperBound  = [[ 57,255,234], [ 15, 255, 255], [ 11,255,255], [ 10,255,255], [ 31,255,192], [112,255,188], [179,127, 43]]
maskName = dict.fromkeys(['signMask', 'potMask', 'tubeMask', 'redSideMask', 'yellowSideMask', 'blueSideMask', 'blackSideMask', 'redWaterMask', 'yellowWaterMask', 'blueWaterMask', 'blackWaterMask']) 

colorCode = 9
while True:
 ret, waterFrame = waterCap.read()
 if ret:
  waterFrame = cv2.resize(waterFrame, (640, 480))
  waterHsv = cv2.cvtColor(waterFrame,cv2.COLOR_BGR2HSV)
  for i in range(7, 11): #mask water four color
   mask = cv2.inRange(waterHsv,np.array(maskLowwerBound[i-4]),np.array(maskUpperBound[i-4]))
   maskName[list(maskName)[i]] = cv2.bitwise_and(waterHsv,waterHsv,mask=mask)
   maskName[list(maskName)[i]] = cv2.cvtColor(maskName[list(maskName)[i]],cv2.COLOR_HSV2BGR)
   maskName[list(maskName)[i]] = cv2.cvtColor(maskName[list(maskName)[i]],cv2.COLOR_BGR2GRAY)
  contours, hierarchy = cv2.findContours(maskName[list(maskName)[colorCode]], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  for cnt in contours:
   area = cv2.contourArea(cnt)
   if area > 7000:  
    cv2.drawContours(waterFrame, cnt, -1, (128, 0, 128), 3) 
    vertices = cv2.approxPolyDP(cnt, cv2.arcLength(cnt, True) * 0.02, True)
    corners = len(vertices)
    x, y, w, h = cv2.boundingRect(vertices)
    cv2.circle(waterFrame, (x, y), 10, (255, 255, 255), -1)
    print(x+w/2, y+h/2)
  maskName[list(maskName)[colorCode]] = cv2.cvtColor(maskName[list(maskName)[colorCode]],cv2.COLOR_GRAY2BGR)
  hor = np.hstack((waterFrame, maskName[list(maskName)[colorCode]]))
  cv2.imshow('result', hor)
  # hor2 = np.hstack((maskName[list(maskName)[7]], maskName[list(maskName)[8]]))
  # hor3 = np.hstack((maskName[list(maskName)[9]], maskName[list(maskName)[10]]))
  # ver = np.vstack((hor2, hor3))
  # cv2.imshow('result', ver)
 else:
  break

 if cv2.waitKey(1)==ord("q"):
  break

waterCap.release()
cv2.destroyAllWindows()