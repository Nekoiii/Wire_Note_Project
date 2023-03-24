#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分水岭算法（watershed algorithm）
""" 

import os
import numpy as np
import cv2  
from matplotlib import pyplot as plt
img_name='img-1'
img_path='../test_imgs/'+img_name+'.jpg'
img = cv2.imread(img_path)
assert img is not None, "file could not be read, check with os.path.exists()"
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


#用cv2.threshold()函数来实现Otsu二值化算法
#ret是Otsu二值化算法中返回的阈值，thresh是应用该阈值后得到的二值图像
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


#用形态学操作来消除噪声和连接断开的边缘。
#https://blog.csdn.net/weixin_57440207/article/details/122647000
#闭运算(morphological closing)操作。闭运算可以将边缘的空洞填充，并消除噪声，使得边缘更加连续。
kernel = np.ones((3,3),np.uint8)
#cv2.MORPH_OPEN: 开运算(先腐蚀,再膨胀)。
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
#对背景图像进行膨胀操作, 以便后面计算未知区域。
sure_bg = cv2.dilate(opening,kernel,iterations=3)
#距离变换(distance transform):计算图像中每个像素点到最近的边缘(或前景)的距离。 
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
#对前景图像进行二值化（像素值设为0或255）。
#thresh越小，分类越细
#ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
ret, sure_fg = cv2.threshold(dist_transform,0.2*dist_transform.max(),255,0)

sure_fg = np.uint8(sure_fg)
#计算未知区域(背景减前景)
unknown = cv2.subtract(sure_bg,sure_fg)

 
gap = np.ones((img.shape[0], 10), np.uint8) * 255
cv2.imshow('gray & thresh',np.hstack((gray,gap, thresh)))
cv2.imshow('opening & sure_fg & sure_bg & unknown', np.hstack(( opening,gap,sure_fg,gap,sure_bg,gap,unknown)))
cv2.waitKey(0)
cv2.destroyAllWindows()
 

#距离小于阈值ret的像素点划分为前景(sure_fg), 其余划分为背景(sure_bg)
# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)
#print('markers-1',markers)
'''
初始时将 markers数组中的所有像素初始都为-1(未分类)。然后从markers中某个像素开始，将其周围
像素根据其灰度值和梯度值与当前像素进行比较，并将相邻像素中灰度值和梯度值较小的标记为同一区域。
如果有多个区域的像素灰度值和梯度值都与当前像素相同，则选择其中标记值最小的区域。
标记值的具体取值可以是任意整数，但不能为0或-1，因为这些值已经被用于表示背景和待分割区域了。
'''
# Add one to all labels so that sure background is not 0, but 1
markers = markers+1
# Now, mark the region of unknown with zero
markers[unknown==255] = 0
print('markers-2',markers)


'''
-1：表示该像素属于未标记的区域（比如轮廓）。
0：表示该像素属于背景区域。
1：原本的背景区域。
>1：表示该像素属于该正整数对应的区域。
'''
#在cv2.watershed中,矩阵边框上的像素也被会分为-1,所以这里要用cv2.copyMakeBorde先加一个边框，后面再删掉
markers = cv2.copyMakeBorder(markers, 5, 5, 5, 5, cv2.BORDER_REPLICATE)
img=cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_REPLICATE)
markers = cv2.watershed(img,markers)
markers = markers[5:-5, 5:-5]
img = img[5:-5, 5:-5]
print('markers-3_1',markers)
img[markers == -1] = [255,0,0] #给轮廓上色，画出分割线
print('markers-3_2',markers)

 

mask = np.zeros_like(img)
unique_labels=np.unique(markers)
num_classes = len(unique_labels)-1
print("Total number of classes: ", num_classes,'\n unique_labels:',unique_labels)

'''
for i in range(num_classes):
  mask[markers == (i+1)] = [(i+1)/num_classes*255, 150, 150]
mask[markers == -1] = [255,0,0]
plt.imshow(np.hstack((img,mask)))
plt.show()
'''

#mask中黑色背景，白色前景
mask[(markers == -1)|(markers == 1)] = [0, 0, 0]
mask[(markers != 1) & (markers != -1)] = [255,255,255]
plt.imshow(np.hstack((img,mask)))
plt.show()



'''
markers = np.uint8(markers)
print('markers',markers)
# 获取每个区域的面积等信息
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(markers)
print('num_labels:',num_labels,'\n labels:\n', labels,'\n stats:\n',stats,'\n centroids:\n', centroids )
# 输出每个区域的面积
for i in range(num_labels):
     print('Area of region', i, ':', stats[i, cv2.CC_STAT_AREA])
'''
 

print('mask',mask)
print('markers-4',markers)
#保存markers和mask
# 构建目标文件夹路径
markers_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../test_imgs', 'markers')
mask_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../test_imgs', 'masks')
# 创建目标文件夹
if not os.path.exists(markers_dir):
    os.makedirs(markers_dir)
if not os.path.exists(mask_dir):
    os.makedirs(mask_dir)

# 保存图片到目标文件夹
cv2.imwrite(os.path.join(markers_dir, img_name+'_marker'+'.png'), markers)
cv2.imwrite(os.path.join(mask_dir, img_name+'_mask'+'.png'), mask)









