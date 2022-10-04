    grey = cv2.cvtColor(imgcontours, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (5,5), 0)
    edge = cv2.Canny(blur, 100, 255)