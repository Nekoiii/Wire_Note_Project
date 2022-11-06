#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
原理:https://www.cnblogs.com/php-rearch/p/6760683.html
python实现:https://github.com/alyssaq/hough_transform/blob/master/hough_transform.py
"""


import numpy as np
import math
import scipy.ndimage as ndi
import matplotlib.image as ima
import matplotlib.pyplot as plt
import cv2

#import os
#print(os.getcwd())#查看当前路径


def rgb2gray(rbg_img):  # RGB彩图转灰度图(convert a color image to grayscale)  
  
  return np.dot(rbg_img[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)# RGB转灰度的常用参数[0.2989, 0.5870, 0.1140]     


#向量点积公式：a•b = |a||b|cosθ

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
  

imgpath = 'sky_1.jpeg'
image=np.array(plt.imread(imgpath)) 
plt.imshow(image)
img_gray_array=rgb2gray(image)
plt.imshow(img_gray_array)
hough_transform(img_gray_array)






