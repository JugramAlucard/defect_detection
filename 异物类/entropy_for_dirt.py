import math
import cv2
import numpy as np


def calcGrayHist(image):
    rows, cols = image.shape[:2]
    grayHist = np.zeros([256], np.uint64)
    for row in range(rows):
        for col in range(cols):
            grayHist[image[row][col]] += 1
    return grayHist


def thresh_entropy(image):
    rows, cols = image.shape
    # 求灰度直方图
    grayHist = calcGrayHist(image)
    # 归一化灰度直方图，即概率直方图
    normGrayHist = grayHist / float(rows*cols)
    # 1.计算累加直方图
    zeroCumuMoment = np.zeros([256], np.float32)
    for i in range(256):
        if i == 0:
            zeroCumuMoment[i] = normGrayHist[i]
        else:
            zeroCumuMoment[i] = zeroCumuMoment[i-1] + normGrayHist[i]
    # 2.计算各个灰度级的熵
    entropy = np.zeros([256], np.float32)
    for i in range(256):
        if i == 0:
            if normGrayHist[i] == 0:
                entropy[i] = 0
            else:
                entropy[i] = -normGrayHist[i] * math.log10(normGrayHist[i])
        else:
            if normGrayHist[i] == 0:
                entropy[i] = entropy[i-1]
            else:
                entropy[i] = entropy[i-1] - normGrayHist[i] * math.log10(normGrayHist[i])
    # 3.找阈值
    fT = np.zeros([256], np.float32)
    ft1, ft2 = 0, 0
    totalEntropy = entropy[255]
    for i in range(255):
        # 找最大值
        maxFront = np.max(normGrayHist[0:i+1])
        maxBack = np.max(normGrayHist[i+1:256])
        if maxFront == 0 or zeroCumuMoment[i] == 0 or maxFront == 1 or zeroCumuMoment[i] == 1 or totalEntropy == 0:
            ft1 = 0
        else:
            ft1 = entropy[i] / totalEntropy * (math.log10(zeroCumuMoment[i]) / math.log10(maxFront))
        if maxBack == 0 or 1-zeroCumuMoment[i] == 0 or maxBack == 1 or 1-zeroCumuMoment[i] == 1:
            ft2 = 0
        else:
            if totalEntropy == 0:
                ft2 = (math.log10(1-zeroCumuMoment[i])/math.log10(maxBack))
            else:
                ft2 = (1-entropy[i] / totalEntropy)*(math.log10(1-zeroCumuMoment[i])/math.log10(maxBack))
        fT[i] = ft1 + ft2
    # 找最大值的索引，作为得到的阈值
    threshLoc = np.where(fT==np.max(fT))
    thresh = threshLoc[0][0]
    # 阈值处理
    threshold = np.copy(image)
    threshold[threshold>thresh] = 255
    threshold[threshold<=thresh] = 0
    return thresh, threshold

if __name__ == '__main__':
    img = cv2.imread("D:\defect\crack\crack_detection\crack_detection\dirt.png", 0)
    thresh, threshImg = thresh_entropy(img)
    cv2.imwrite('D:\defect\crack\crack_detection\crack_detection\img8_entropy.png', threshImg)
    cv2.imshow('thresh', threshImg)
    cv2.waitKey()
