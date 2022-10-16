import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def getContours(img,imgContour):
    _, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = 1000
        if area > areaMin:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print(len(approx))
            x , y , w, h = cv2.boundingRect(approx)
            # cv2.rectangle(imgContour, (x , y ), (x + w , y + h ), (0, 255, 0), 5)

            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)
                        # x , y , w, h = cv2.boundingRect(approx)
            if(len(approx) == 4):
                # switch state 
                # changestate()
                print('4')
                # return 0
            elif(len(approx) == 3):
                # determine left, right
                cv2.drawContours(imgContour, cnt, -1,(153,204,0), 7)
                x1, y1, w1, h1 = cv2.boundingRect(approx)
                newapp = np.ravel(approx)
                max = 0
                secmax = 0

                for j in range(0, len(newapp)):
                    if newapp[j] > max:
                        max = newapp[j]
                    elif newapp[j] > secmax:
                        secmax = newapp[j]

                if abs(max - secmax) < w1/2:
                    cv2.putText(imgContour, "left", (x1+w1+10, y1+30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,153), 2)
                    # turn left
                else:
                    cv2.putText(imgContour, "right", (x1+w1+10, y1+30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,153), 2)
                    # turn right
                 #changestate()
            elif(len(approx) == 8):
                print("circle")
                #changestate()

            cv2.rectangle(imgContour, (x , y ), (x + w , y + h ), (0, 255, 0), 5)
            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)

while True:
    cap = cv2.VideoCapture(0)
    success, img = cap.read()
    
    img = cv2.resize(img, (640, 480))
    imgContour = img.copy()
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray,100,255)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    getContours(imgDil,imgContour)
    # imgStack = stackImages(0.8,([img,imgCanny],
    #                             [imgDil,imgContour]))
    cv2.imshow("Result", imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break