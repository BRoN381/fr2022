import cv2
import numpy as np
cap=cv2.VideoCapture(0)#讀取電腦攝影機鏡頭，0是電腦鏡頭編號

def find(img):
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower=np.array([3,209,137])
    upper=np.array([[9,255,245]])
    mask=cv2.inRange(hsv,lower,upper)
    result=cv2.bitwise_and(img,img,mask=mask)
    findSign(mask)
    cv2.imshow("result",result)

def findSign(img):
    __, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 回傳兩個值，第一個值是輪廓，第二個值是階層
    # x,y,w,h=-1,-1,-1,-1
    for cnt in contours:
        # print(cnt)#輪廓點的數字,顯示在run的結果
        cv2.drawContours(imgContour, cnt, -1, (0, 255, 0), 3)  # (畫在哪,要畫的輪廓,要畫的輪廓是第幾個-1表每一個都畫,顏色,粗度)
        area = cv2.contourArea(cnt)  # 輪廓面積
        if area > 10000:  # 扣除雜訊
            peri = cv2.arcLength(cnt, True)  # 輪廓邊長(輪廓,輪廓是否閉合)
            vertices = cv2.approxPolyDP(cnt, peri * 0.02, True)  # 用多邊形近似輪廓(輪廓,近似值,輪廓是否閉合)會回傳多邊形頂點
            corners = len(vertices)  # 有幾個頂點
            x, y, w, h = cv2.boundingRect(vertices)  # 回傳四個值:左上角的x、左上角的y值、寬度、高度
            if corners==3:#是個三角形
                #cv2.putText(imgContour,"triangle",(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                newapp = np.ravel(vertices)
                flag_y = 0
                flag_x = 0
                sec_y = 0
                sec_x = 0
                for i in range(1, corners, 2):
                    if newapp[i] > flag_y:
                        flag_y = newapp[i]
                        flag_x = newapp[i - 1]
                    elif newapp[i] > sec_y:
                        sec_y = newapp[i]
                        sec_x = newapp[i-1]
                if flag_x - sec_x < w/4:
                    cv2.putText(imgContour, "right", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif flag_x - sec_x > w/4:
                    cv2.putText(imgContour, "left", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif corners==4:#是個正方形
                cv2.putText(imgContour, "rectangle", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif corners == 8:  # 是個正方形
                cv2.putText(imgContour, "circle", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


while True:#顯示影片
    ret, frame = cap.read()  # 讀取影片每一幀，cap.read()回傳兩個值，第一個為布林值，取得道的下一幀
    if ret:
        imgContour=frame.copy()
        # cv2.imshow("vedio",frame)
        img = cv2.resize(frame, (640, 480))
        find(img)
        cv2.imshow("contour", imgContour)
    else:
        break
    if cv2.waitKey(1)==ord("q"):#鍵盤上按鍵按下q時，影片中止
        break










# approx = cv2.approxPolyDP(i, arclen*0.02, True)
#             if len(approx) == 7:
#                 cv2.drawContours(imgcontours, i, -1,(153,204,0), 7)
#                 x1, y1, w1, h1 = cv2.boundingRect(approx)
#
#                 if abs(maximum - secmaximum) < w1/4:
#                     cv2.putText(imgcontours, "left", (x1+w1+10, y1+30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,153), 2)
#                     return 1
#                 else:
#                     cv2.putText(imgcontours, "right", (x1+w1+10, y1+30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,153), 2)
#                     return 2