import easyocr, cv2, os
import numpy as np

# 이미지 비율 줄이기
def imgResizeByHeight(img, height) :
    realH = img.shape[0]
    realW = img.shape[1]
    ratio = height/realH
    width = int(realW * ratio)
    return cv2.resize(img, (width, height))

# 텍스트박스 이미지 찾기
def getTextBox(img) : 
    contourList = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    # Morphology Transform - 1차
    kernel  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    grad = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
    # Morphology Transform - 2차
    _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (20,1))
    connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel2)
    # contour 찾기
    contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    mask = np.zeros(bw.shape, dtype=np.uint8)
    rgb = img.copy()
    for idx in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[idx])
        mask[y:y+h, x:x+w] = 0
        cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
        r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w*h)
        if r > 0.35 and w > 8 and h > 8 :
            cv2.rectangle(rgb, (x,y), (x+w, y+h), (0, 255, 0), 2)
            contourList.append(contours[idx])
    # cv2.imshow("result", rgb)
    return (rgb, contourList)