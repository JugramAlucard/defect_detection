import cv2
import numpy as np
 
print(cv2.__version__)
minThres = 6
 
# 读取图像1
img1 = cv2.imread(r'D:\\缺陷检测\\裂缝检测\\crack_detection\\crack_detection\\crack1.png')
img2 = cv2.imread(r'D:\\缺陷检测\\裂缝检测\\crack_detection\\crack_detection\\crack1.png')

# 中值滤波
img1 = cv2.medianBlur(img1, 15)
 
# 图像差分
diff = cv2.absdiff(img1, img2)
cv2.imshow('diff', diff)  # 结果图
 
gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
# 二值化
_, thres = cv2.threshold(gray, minThres, 255, cv2.THRESH_BINARY)
cv2.imshow('thres', thres)
 
# 查找轮廓
contours, hierarchy = cv2.findContours(thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# 输出轮廓个数
print(len(contours))
 
for i in range(0, len(contours)):
    length = cv2.arcLength(contours[i], True)
    # 通过轮廓长度筛选
    if length > 30:
        cv2.drawContours(img2, contours[i], -1, (0, 0, 255), 2)
 
cv2.imshow('result', img2)  # 结果图
cv2.waitKey(0)
cv2.destroyAllWindows()