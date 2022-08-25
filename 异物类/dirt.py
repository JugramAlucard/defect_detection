import cv2
import numpy as np

img = cv2.imread('D:\defect\crack\crack_detection\crack_detection\dirt.png')
cv2.imshow('src',img)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

mean = cv2.medianBlur(gray,201)
cv2.imshow('mean',mean)

#diff = cv2.absdiff(gray, mean)
diff = gray - mean
cv2.imshow('diff',diff)
cv2.imwrite('diff.jpg',diff)
_,thres_low = cv2.threshold(diff,150,255,cv2.THRESH_BINARY)#二值化
_,thres_high = cv2.threshold(diff,220,255,cv2.THRESH_BINARY)#二值化
thres = thres_low - thres_high
cv2.imshow('thres',thres)

k1 = np.zeros((18,18,1), np.uint8)
cv2.circle(k1,(8,8),9,(1,1,1),-1, cv2.LINE_AA)
k2 = np.zeros((20,20,1), np.uint8)
cv2.circle(k2,(10,10),10,(1,1,1),-1, cv2.LINE_AA)

opening = cv2.morphologyEx(thres, cv2.MORPH_OPEN, k1)
cv2.imshow('opening',opening)
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, k1)
cv2.imshow('closing',closing)

contours,hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for cnt in contours:
  (x, y, w, h) = cv2.boundingRect(cnt)
  if w > 5 and h > 5:
      #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
      cv2.drawContours(img,contours,-1,(0,0,255),2)

      cv2.drawContours(img,cnt,2,(0,0,255),2)

cv2.imshow('result',img)

cv2.waitKey(0)
cv2.destroyAllWindows()
print('Done!')