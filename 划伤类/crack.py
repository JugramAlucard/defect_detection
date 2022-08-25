import cv2
import numpy as np
import heapq
o = cv2.imread('D:\defect\crack\crack_detection\crack_detection\crack.png')
gray = cv2.cvtColor(o, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 72, 150, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cv2.imshow('original', o)
n = len(contours)
area = []
for i in range(n):
    area.append(cv2.contourArea(contours[i]))
max_num_index_list = map(area.index, heapq.nlargest(1, area))
Max = list(max_num_index_list)[0]
print(Max)
contoursImg = np.zeros(o.shape, np.uint8)
contoursImg = cv2.drawContours(contoursImg, contours, Max, (0, 0, 255), -1)
cv2.imshow('the crack', contoursImg)
# cv2.imwrite('the crack.jpg', contoursImg)
cv2.waitKey()
cv2.destroyAllWindows()
