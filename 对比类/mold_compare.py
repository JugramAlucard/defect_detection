from matplotlib import pyplot as plt
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

#字符添加函数
def ImgText_CN(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, np.ndarray)): 
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype(r'C:\Windows\Fonts\simsun.ttc', textSize, encoding="utf-8")         
    draw.text((left, top), text, textColor, font=fontText)     
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

#对比函数
def compare(result,img0,i):
    if result >0.9:                              #相关性大于这个阈值的才可以被判断为合格
        detect=ImgText_CN(img0, 'Qualified', 10, 10, textColor=(255, 0, 0), textSize=100)
    else:
        detect=ImgText_CN(img0, 'Not Qualified', 10, 10, textColor=(255, 0, 0), textSize=100)
    cv2.imshow("Detect_%d"%(i),detect)          
    key = cv2.waitKey(0)
    if key==27: 
        print(key)
        cv2.destroyAllWindows()

#创建灰度直方图    
def create_hist(img):
    img = cv2.imread(img)              
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    #将图片转化为8bit灰度图

    plt.imshow(img_gray, cmap=plt.cm.gray)               
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])    #灰度直方图 
    plt.figure()
    plt.title("Grayscale Histogram")
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")
    plt.plot(hist)
    plt.xlim([0, 256])
    plt.show()
    return hist

hist1=create_hist("D:\\mvi\\data_seg-B\\1A.png")              #给标准样品绘制直方图
for i in range(1,4):
    print(i)                                #打印图片序号
    img_path = "D:\\mvi\\data_seg-B\\" + str(i) + "A.png"                             

    img=cv2.imread(img_path,1)         
    hist2=create_hist(img_path)       #给测试样品绘制直方图     
    match1 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)   #返回巴氏距离
    match2 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)         #返回相关性
    print("Bhattacharyya distance:%s, correlation:%s" %(match1, match2))
    print("\n")
    compare(match2,img,i)                             #比较并绘制