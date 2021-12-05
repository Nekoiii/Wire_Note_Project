import numpy as np
import cv2 as cv


# Sobel提取边缘,if_black=1时底色为黑,边缘线为白
def do_sobel(img_path, if_black=False):
    img = cv.imread(img_path, 0)
    x = cv.Sobel(img, cv.CV_16S, 1, 0)
    y = cv.Sobel(img, cv.CV_16S, 0, 1)
    Scale_absX = cv.convertScaleAbs(x)
    Scale_absY = cv.convertScaleAbs(y)
    result = cv.addWeighted(Scale_absX, 0.5, Scale_absY, 0.5, 0)
    if if_black:
        return result
    else:
        return ~result


# 轮廓提取
def do_find_contours(img_path):
    img = cv.imread(img_path)
    # ret, th = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
    # 二值化
    binaryImg = cv.Canny(img, 50, 200)
    # 提取边缘。第二个参数
    contours, hierarchy = cv.findContours(binaryImg, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    # 创建白色幕布
    temp = np.ones(binaryImg.shape, np.uint8) * 255
    # 画出轮廓：temp是白色幕布，contours是轮廓，-1表示全画，然后是颜色，厚度
    cv.drawContours(temp, contours, -1, (0, 255, 0), 3)
    return temp


# 转换为动画风
# https://blog.csdn.net/weixin_44613063/article/details/107901148
def convert_to_anime(img_path):
    img = cv.imread(img_path)
    img_copy = img
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_blur = cv.medianBlur(img_gray, 5)
    img_edge = cv.adaptiveThreshold(img_blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, blockSize=9, C=3)
    # 灰度图片转3通道，用于后续合并
    img_edge = cv.cvtColor(img_edge, cv.COLOR_GRAY2BGR)

    for _ in range(2):
        img_copy = cv.pyrDown(img_copy)
    for _ in range(5):
        img_copy = cv.bilateralFilter(img_copy, d=9, sigmaColor=9, sigmaSpace=7)
    img_copy = cv.resize(img_copy, (img.shape[1], img.shape[0]), interpolation=cv.INTER_CUBIC)
    img_anime = cv.bitwise_and(img_copy, img_edge)
    return img_anime
