#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分水岭算法（watershed algorithm）
""" 

import numpy as np
import cv2  
from matplotlib import pyplot as plt
img = cv2.imread('../test_imgs/cat-1.jpg')
#img = cv2.imread('../test_imgs/big-1.jpg')
assert img is not None, "file could not be read, check with os.path.exists()"
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


#用cv2.threshold()函数来实现Otsu二值化算法
#ret是Otsu二值化算法中返回的阈值，thresh是应用该阈值后得到的二值图像
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


#用形态学操作来消除噪声和连接断开的边缘。
#https://blog.csdn.net/weixin_57440207/article/details/122647000
#闭运算(morphological closing)操作。闭运算可以将边缘的空洞填充，并消除噪声，使得边缘更加连续。
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
#对背景图像进行膨胀操作, 以便后面计算未知区域。
sure_bg = cv2.dilate(opening,kernel,iterations=3)
#距离变换(distance transform):计算图像中每个像素点到最近的边缘(或前景)的距离。 
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
#对前景图像进行二值化（像素值设为0或255）。
#thresh越小，分类越细
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
#ret, sure_fg = cv2.threshold(dist_transform,0.2*dist_transform.max(),255,0)

sure_fg = np.uint8(sure_fg)
#计算未知区域(背景减前景)
unknown = cv2.subtract(sure_bg,sure_fg)

 
gap = np.ones((img.shape[0], 10), np.uint8) * 255
cv2.imshow('gray & thresh',np.hstack((gray,gap, thresh)))
cv2.imshow('sure_fg & sure_bg & unknown', np.hstack(( sure_fg,gap,sure_bg,gap,unknown)))
cv2.waitKey(0)
cv2.destroyAllWindows()
 

#距离小于阈值ret的像素点划分为前景(sure_fg), 其余划分为背景(sure_bg)
# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)
#print('markers-1',markers)
'''
OpenCV中，markers数组的初始化方式是将图像的前景（即目标）区域设为1，背景区域设为0，未知区域（即待分割区域）设为-1。
算法执行过程中，分水岭算法会将像素分成若干个区域，并为每个区域分配一个标记值。
标记值的具体取值可以是任意整数，但不能为0或-1，因为这些值已经被用于表示背景和待分割区域了。
在算法执行过程中，markers数组中的值会随着区域的合并和分离而不断变化，最终得到每个像素的最终标记值
'''
# Add one to all labels so that sure background is not 0, but 1
markers = markers+1
# Now, mark the region of unknown with zero
markers[unknown==255] = 0
#print('markers-2',markers)


#分水岭算法后，所有轮廓的像素点会被标注为-1 
markers = cv2.watershed(img,markers)
img[markers == -1] = [255,0,0] #给轮廓上色，画出分割线
#print('markers-3',markers)

 

mask = np.zeros_like(img)
num_classes = len(np.unique(markers))-1
print("Total number of classes: ", num_classes)
for i in range(num_classes):
  mask[markers == (i+1)] = [(i+1)/num_classes*255, 150, 150]
mask[markers == -1] = [255,0,0]
 
 
plt.imshow(np.hstack((img,mask)))
plt.show()











