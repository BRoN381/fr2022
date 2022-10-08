import cv2
import numpy as np
import serial

#ser = serial.Serial('', 9600)

leftdiff = 0
rightdiff = 0
pixelcount = []
for i in range(640):
    pixelcount.append(0)
motorspeed = ['2'] # 1 = left, 2 = mid, 3 = right
boundary = [0, 0, 0, 0]
arrowcount = [0, 0, 0]
turnratio = 0.5
left = 0
right = 0
moveratio = 0
# serialOutput = ""


def cupdetect(frame):
    #mask for grass
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([0, 0, 255])
    upper_bound = np.array([255, 225, 255])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    frame = cv2.bitwise_and(frame, frame, mask=mask)
    height = frame.shape[0]
    width = frame.shape[1]
    firstcoor = 0
    output = 0
    upbound = 120
    lowbound = 280
    boundary = [0, 0, 0, 0]
    for i in range(0, width, 3):
        pixel = 0
        pixelcount[i] = 0
        num = np.uint8(0)
        #chop the image
        for j in range(upbound, lowbound, 3):
            if (frame[j][i][0] != num or frame[j][i][1] != num or frame[j][i][2] != num):
                pixel += 1
        if pixel > 25:
            pixelcount[i] = pixel
        #clear if density too small
            if firstcoor == 0:
                firstcoor = i
        elif firstcoor != 0:
            if i - firstcoor < 10:
                for j in range(firstcoor, i):
                    pixelcount[j] = 0
            firstcoor = 0
        #find range for left and right
        if i < 320:
            if pixelcount[i] != 0:
                if boundary[0] == 0:
                    boundary[0] = i
                else:
                    boundary[1] = i
        elif i >= 320:
            if pixelcount[i] != 0:
                if boundary[2] == 0:
                    boundary[2] = i
                else:
                    boundary[3] = i
    leftdiff = boundary[1] - boundary[0]
    rightdiff = boundary[3] - boundary[2]
    print('boundary:', boundary)
    print('leftdiff:', leftdiff, 'rightdiff:', rightdiff)
    if abs(leftdiff-rightdiff) > 70:
        if leftdiff-rightdiff>0:
            output = '3'
        else:
            output = '1'
    else:
        output = '2'
    moveratio = (leftdiff-rightdiff)*turnratio
    #show density
    for i in range(640):
        if pixelcount[i] != 0:
            frame = cv2.line(frame, (i, 480), (i, 480-pixelcount[i]), (255, 255, 0), 1)
    frame = cv2.line(frame, (boundary[0], 480), (boundary[0], 0), (0, 0, 255), 1)
    frame = cv2.line(frame, (boundary[1], 480), (boundary[1], 0), (0, 0, 255), 1)
    frame = cv2.line(frame, (boundary[2], 480), (boundary[2], 0), (0, 0, 255), 1)
    frame = cv2.line(frame, (boundary[3], 480), (boundary[3], 0), (0, 0, 255), 1)
    frame = cv2.line(frame, (0, upbound), (640, upbound), (0, 0, 255), 1)
    frame = cv2.line(frame, (0, lowbound), (640, lowbound), (0, 0, 255), 1)
    if abs(leftdiff-rightdiff) < 25:
        cv2.putText(frame, "go straight", (10, 480-10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
    elif leftdiff > rightdiff:
        cv2.putText(frame, "turn right", (10, 480-10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
    else:
        cv2.putText(frame, "turn left", (10, 480-10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
    print(motorspeed)
    left = 128 - moveratio 
    right = 128 + moveratio
    left_str = str(int(left))
    right_str = str(int(right))
    if right < 100:
        right_str = '0' + right_str
    if left < 100:
        left_str = '0' + left_str
    serialOutput = left_str + right_str + "000" 
    #ser.write(serialOutput)
    print(serialOutput)
    cv2.imshow('cup', frame)

cap = cv2.VideoCapture(1)
counter = 0

while True:
    ret, frame = cap.read()
    imgcontours = frame.copy()
    resize = cv2.resize(frame, (640, 480))
    cupdetect(resize)  
    if cv2.waitKey(1) == ord('q'):
        break
    # try:
    #     ret, frame = cap.read()
    #     imgcontours = frame.copy()
    #     resize = cv2.resize(frame, (640, 480))
    #     cupdetect(resize)  
    #     if cv2.waitKey(1) == ord('q'):
    #         break
    # except KeyboardInterrupt():
    #     break

cap.release()
cv2.destroyAllWindows()