#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
霍夫变换原理和实现：
https://www.cnblogs.com/php-rearch/p/6760683.html
python代码参考：
https://github.com/alyssaq/hough_transform/blob/master/hough_transform.py
直接用opencv实现：
https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html

几乎不使用opencv检测长方形：
原理: https://www.homeworkhelponline.net/blog/programming/find-rectangles，github: https://github.com/HomeworkHelpOnline/Python-Find_Rectangles
np.where(): https://blog.csdn.net/qq754772661/article/details/107122996/
"""
import numpy as np
import scipy.signal as sp
import math
import matplotlib.pyplot as plt
import cv2

import hough_functions

 
img_path = 'imgs/sky_1.jpeg' #*注:Spyder里记得在Files窗口打开目录文件夹啊!
img=np.array(plt.imread(img_path)) 
#plt.imshow(img)
img_gray=hough_functions.rgb2gray(img)
img_gray = hough_functions.blur_image(img_gray) 
edged = cv2.Canny(img_gray, 30, 130)#cv2.Canny():边缘检测

#有时图片会自带边框, 为忽略掉它们这里把边沿5px都设为0
borderLen = 5 
lenx, leny = edged.shape
edged[0:borderLen,0:leny] = 0
edged[lenx-borderLen:lenx,0:leny] = 0
edged[0:lenx,0:borderLen] = 0
edged[0:lenx,leny-borderLen:leny] = 0
plt.imshow(edged)  

#plt.subplots():一纸绘多图。nrows:横轴分成的区域,ncols:纵轴分成的区域,plot_number:当前的绘图区,figsize:绘图区大小
fig, ax1 = plt.subplots(ncols=1, nrows=1, figsize=(8, 4))
ax1.set_axis_off()  #set_axis_off():不显示X轴和Y轴
ax1.imshow(edged, cmap="bone")#这里"bone"是一种颜色
fig.savefig("Rectangles_edged.jpg")#savefig():保存图片


rho,theta = hough_functions.hough_transform(edged,rho_res=1,theta_res=1,
                            thresholdVotes=30,filterMultiple=5,thresholdPixels=0)


#plt.imshow(img_gray)
hough_transform(img_gray)

accumulator, thetas, rhos = hough_transform(img_gray)
#print("thetas: ",thetas,"rhos: ",rhos)
show_hough_line(img_gray, accumulator, thetas, rhos, save_path='hough_line_output.png')

plotHoughLines()




