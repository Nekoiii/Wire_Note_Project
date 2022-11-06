#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
霍夫变换原理和实现：
https://www.cnblogs.com/php-rearch/p/6760683.html
python代码参考：
https://github.com/alyssaq/hough_transform/blob/master/hough_transform.py
直接用opencv实现：
https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html

不使用opencv检测长方形：
原理: https://www.homeworkhelponline.net/blog/programming/find-rectangles，github: https://github.com/HomeworkHelpOnline/Python-Find_Rectangles
np.where(): https://blog.csdn.net/qq754772661/article/details/107122996/
"""


import numpy as np
import scipy.signal as sp
import math
import matplotlib.pyplot as plt
import cv2

#import os
#print(os.getcwd())#查看当前路径


def rgb2gray(rbg_img):  #RGB彩图转灰度图(convert a color img to grayscale)  
  #np.dot(): 计算向量点积
  #RGB转灰度的常用参数[0.2989, 0.5870, 0.1140]     
  return np.dot(rbg_img[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)

def blur_image(img_gray): #滤波函数。类似于cv里的filter2d()
    #skipped first line and first column to keep it more simple (it's zeroed out anyway).
    #for every pixel we change it with the average of 4 pixels.
    kernel = np.ones((2,2),np.float32)/4  #Blurring kernel
    res=sp.convolve2d(img_gray,kernel,mode='same')#scipy.signal.convolve2d():进行卷积
    return np.round(res).astype(np.uint8)
  
#进行霍斯变换
def hough_transform(img, angle_step=1,value_threshold=5):
  thetas = np.deg2rad(np.arange(-90.0, 90.0, angle_step))#np.deg2rad()角度制转弧度制 
  width, height = img.shape
  diag_len = int(round(math.sqrt(width * width + height * height)))
  rhos = np.linspace(-diag_len, diag_len, diag_len * 2)#np.linspace()创建等差数列
  
  #一些常用值
  cos_theta = np.cos(thetas)
  sin_theta = np.sin(thetas)
  num_thetas = len(thetas)

  # Hough accumulator array of theta vs rho
  accumulator = np.zeros((2 * diag_len, num_thetas))
  are_edges = cv2.Canny(img,50,150,apertureSize = 3)
  
  y_idxs, x_idxs = np.nonzero(are_edges)  # np.nonzero()返回array中非零元素索引
  
  # Vote in the hough accumulator
  xcosthetas = np.dot(x_idxs.reshape((-1,1)), cos_theta.reshape((1,-1)))
  ysinthetas = np.dot(y_idxs.reshape((-1,1)), sin_theta.reshape((1,-1)))
  rhosmat = np.round(xcosthetas + ysinthetas) + diag_len
  rhosmat = rhosmat.astype(np.int16)
  for i in range(num_thetas):
      rhos,counts = np.unique(rhosmat[:,i], return_counts=True)
      accumulator[rhos,i] = counts
  return accumulator, thetas, rhos

#绘制映射到霍夫空间的图像
def show_hough_line(img, accumulator, thetas, rhos, save_path=None):
  fig, ax = plt.subplots(1, 2, figsize=(10, 10))

  ax[0].imshow(img, cmap=plt.cm.gray)
  ax[0].set_title('Input img')
  ax[0].axis('img')

  ax[1].imshow(
      accumulator, cmap='jet',
      extent=[np.rad2deg(thetas[-1]), np.rad2deg(thetas[0]), rhos[-1], rhos[0]])
  ax[1].set_aspect('equal', adjustable='box')
  ax[1].set_title('Hough transform')
  ax[1].set_xlabel('Angles (degrees)')
  ax[1].set_ylabel('Distance (pixels)')
  ax[1].axis('img')

  # plt.axis('off')
  if save_path is not None:
      plt.savefig(save_path, bbox_inches='tight')
  plt.show()
  
def plotHoughLines(rho,theta,img):
  a = np.cos(theta)
  b = np.sin(theta)
  x0 = a*rho
  y0 = b*rho

  fig2, ax1 = plt.subplots(ncols=1, nrows=1)
  ax1.imshow(img)
  
  for i in range (0, len(rho)):   
      ax1.plot( [x0[i] + 1000*(-b[i]), x0[i] - 1000*(-b[i])],
                [y0[i] + 1000*(a[i]), y0[i] - 1000*(a[i])], 
                'xb-',linewidth=3)
  
  ax1.set_ylim([img.shape[0],0])
  ax1.set_xlim([0,img.shape[1]])
  
  plt.show()
  

img_path = 'sky_1.jpeg'
img=np.array(plt.imread(img_path)) 
#plt.imshow(img)
img_gray=rgb2gray(img)
img_gray = blur_image(img_gray) 

edged = cv2.Canny(img_gray, 30, 130) 


#plt.imshow(img_gray)
hough_transform(img_gray)

accumulator, thetas, rhos = hough_transform(img_gray)
#print("thetas: ",thetas,"rhos: ",rhos)
show_hough_line(img_gray, accumulator, thetas, rhos, save_path='hough_line_output.png')

plotHoughLines()




