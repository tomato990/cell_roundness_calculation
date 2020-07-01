import matplotlib.pyplot as plt
from pylsm import lsmreader
import cv2
import numpy as np

CENTER_WEIGHT = 1

BLUR_RANGE = (5,5)
BG_THRESHOLD = 2
AREA_THRESHOLD = 300




lsmFileName = 'MEF morphhology/mfn1-12.lsm'
imageFile = lsmreader.Lsmimage(lsmFileName)
imageFile.open()

img=imageFile.get_image(stack=-1,channel=1)
_, threshold = cv2.threshold(img, BG_THRESHOLD, 255, cv2.THRESH_BINARY)
#threshold = cv2.blur(threshold,BLUR_RANGE)
cv2.imshow("original", img)
cv2.waitKey(0)

drawing = False
ix, iy = -1, -1
def draw_circle(event, x, y, flags,papr):
    global ix, iy, drawing, mode
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        if drawing == True:
            cv2.circle(threshold, (x, y), 2, (0, 0, 0), -5)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing == False

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)
while (1):
    cv2.imshow('image', threshold)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break


contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
font = cv2.FONT_HERSHEY_COMPLEX
i = 0
print(len(contours))
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < AREA_THRESHOLD:
        continue
    area = CENTER_WEIGHT*area
    #approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    #cv2.drawContours(img, [approx], 0, (0), 5)
    #x = approx.ravel()[0]
    #y = approx.ravel()[1]

    M = cv2.moments(cnt)
    x = int(M["m10"] / M["m00"])
    y = int(M["m01"] / M["m00"])
    #cv2.drawContours(threshold, cnt, -1, (128, 0, 0), 1)

    p = cv2.arcLength(cnt, False)
    k = 100* (4*np.pi*area)/(p*p)
    i += 1
    print(str(i) + ","+ str(int(p)) + "," + str(int(area)) + "," + str(k))
    cv2.putText(threshold, str(i), (x, y), font, 0.5, (128,0,0))



cv2.imshow("Threshold", threshold)
cv2.waitKey(0)
cv2.destroyAllWindows()