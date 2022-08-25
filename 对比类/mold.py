#导入必要的包
# coding=utf-8
import os
import cv2

# 底板图案
bottom_pic = 'unit.png'
# 上层图案
top_pic = 'mold.pmg'


bottom = cv2.imread(bottom_pic)
top = cv2.imread(top_pic)
# 权重越大，透明度越低
overlapping = cv2.addWeighted(bottom, 1, top, 0.5, 0)

cv2.namedWindow('img',cv2.WINDOW_NORMAL)
cv2.imshow('img',overlapping)

# 保存叠加后的图片
img_file = "D:/mvi"
if not os.path.exists(img_file):
	os.mkdir(img_file)
cv2.imwrite(img_file + "/" + "mold_pic.jpg", overlapping)
# cv2.imwrite("mold_pic.jpg", overlapping)

