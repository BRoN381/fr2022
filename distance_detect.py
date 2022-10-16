import cv2
cap=cv2.VideoCapture(2)#讀取電腦攝影機鏡頭，0是電腦鏡頭編號
#cap=cv2.VideoCapture("cut.mp4")#讀取影片
while True:#顯示影片
    ret, frame = cap.read()  # 讀取影片每一幀，cap.read()回傳兩個值，第一個為布林值，取得道的下一幀
    if ret:
        frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
        cv2.imshow("vedio", frame)
    else:
        break
    if cv2.waitKey(1)==ord("q"):#鍵盤上按鍵按下q時，影片中止
        break