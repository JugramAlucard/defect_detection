
"""
File: opencv-open-file-color-test.py
 
This Python 3 code is published in relation to the article below:
https://www.bluetin.io/opencv/opencv-color-detection-filtering-python/
 
Website:    www.bluetin.io
Author:     Mark Heywood
Date:	    8/12/2017
Version     0.1.0
License:    MIT
"""
 
from __future__ import division
import cv2
import numpy as np
 
def nothing(*arg):
        pass
img_path = 'D:\Desktop\spot1.png'
# 初始化hsv数值
icol = (0, 0, 0, 55, 255, 255)    
cv2.namedWindow('colorTest')

cv2.createTrackbar('lowHue', 'colorTest', icol[0], 255, nothing)
cv2.createTrackbar('lowSat', 'colorTest', icol[1], 255, nothing)
cv2.createTrackbar('lowVal', 'colorTest', icol[2], 255, nothing)

cv2.createTrackbar('highHue', 'colorTest', icol[3], 255, nothing)
cv2.createTrackbar('highSat', 'colorTest', icol[4], 255, nothing)
cv2.createTrackbar('highVal', 'colorTest', icol[5], 255, nothing)
 
frame = cv2.imread(img_path)
 
while True:
    # 获取滑块hsv
    lowHue = cv2.getTrackbarPos('lowHue', 'colorTest')
    lowSat = cv2.getTrackbarPos('lowSat', 'colorTest')
    lowVal = cv2.getTrackbarPos('lowVal', 'colorTest')
    highHue = cv2.getTrackbarPos('highHue', 'colorTest')
    highSat = cv2.getTrackbarPos('highSat', 'colorTest')
    highVal = cv2.getTrackbarPos('highVal', 'colorTest')
 
    # 显示原图
    cv2.imshow('frame', frame)
    
    # 高斯滤波
    frameBGR = cv2.GaussianBlur(frame, (7, 7), 0)
	
    # 显示滤波图
    cv2.imshow('blurred', frameBGR)
	
    # RGB转HSV
    hsv = cv2.cvtColor(frameBGR, cv2.COLOR_BGR2HSV)
    
    colorLow = np.array([lowHue,lowSat,lowVal])
    colorHigh = np.array([highHue,highSat,highVal])
    mask = cv2.inRange(hsv, colorLow, colorHigh)
    cv2.imshow('mask-plain', mask)
 
    kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernal)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)
 
    cv2.imshow('mask', mask)
    
    # 将mask添加到原图
    result = cv2.bitwise_and(frame, frame, mask = mask)
 

    cv2.imshow('colorTest', result)
	
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    
cv2.destroyAllWindows()