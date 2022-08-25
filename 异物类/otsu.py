import math
import cv2
import numpy as np

def calc_gray_hist(image):
    rows, cols = image.shape[:2]
    gray_hist = np.zeros([256], np.uint64)
    for i in range(rows):
        for j in range(cols):
            gray_hist[image[i][j]] += 1
    return gray_hist

def otsu_thresh(image):
    rows, cols = image.shape[:2]
    # 计算灰度直方图
    gray_hist = calc_gray_hist(image)
    # 归一化灰度直方图
    norm_hist = gray_hist / float(rows*cols)
    # 计算零阶累积矩, 一阶累积矩
    zero_cumu_moment = np.zeros([256], np.float32)
    one_cumu_moment = np.zeros([256], np.float32)
    for i in range(256):
        if i == 0:
            zero_cumu_moment[i] = norm_hist[i]
            one_cumu_moment[i] = 0
        else:
            zero_cumu_moment[i] = zero_cumu_moment[i-1] + norm_hist[i]
            one_cumu_moment[i] = one_cumu_moment[i - 1] + i * norm_hist[i]
    # 计算方差，找到最大的方差对应的阈值
    mean = one_cumu_moment[255]
    thresh = 0
    sigma = 0
    for i in range(256):
        if zero_cumu_moment[i] == 0 or zero_cumu_moment[i] == 1:
            sigma_tmp = 0
        else:
            sigma_tmp = math.pow(mean*zero_cumu_moment[i] - one_cumu_moment[i], 2) / (zero_cumu_moment[i] * (1.0-zero_cumu_moment[i]))
        if sigma < sigma_tmp:
            thresh = i
            sigma = sigma_tmp
    # 阈值分割
    thresh_img = image.copy()
    thresh_img[thresh_img>thresh] = 255
    thresh_img[thresh_img<=thresh] = 0
    return thresh, thresh_img


if __name__ == '__main__':
    image = cv2.imread('D:\defect\crack\crack_detection\crack_detection\dirt.png', 0)
    thresh, thresh_img = otsu_thresh(image)
    print(thresh)
    # cv2.imwrite('./images/img7_otsu.jpg', thresh_img)
    cv2.imshow('thresh', thresh_img)
    cv2.waitKey()
