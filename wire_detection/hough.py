#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hough变换检测电线
"""


import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

# 读取图像
#img = cv2.imread('../test_imgs/img-1.jpg')
#img = cv2.imread('../test_imgs/small-1.jpg')
img = cv2.imread('../test_imgs/img-7.jpg')

# 灰度化
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# 边缘检测
edges = cv2.Canny(gray,50,150,apertureSize = 3)

# 计算图像的面积(根据图像面积动态调整后面cv2.HoughLines()里的threshold参数)
w=gray.shape[0]
h=gray.shape[1]
img_area = w * h
# 根据图像面积动态调整 threshold 参数
if img_area > 500000:
    threshold = 500
elif  img_area >100000:
    threshold = int(img_area * 0.0005)
else:
    threshold = 100
print('img_area',img_area)

# 霍夫变换检测曲线
'''
1：表示直线距离rho的精度，一般取1。
np.pi/180：直线角度theta的精度，一般取np.pi/180。
threshold：检测直线的阈值，取值越大，检测到的直线越少。
lines：检测到的直线的最小数量。
'''
#lines = cv2.HoughLines(edges,1,np.pi/180,threshold=threshold)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=threshold, 
                        minLineLength=50, maxLineGap=5)


# 绘制检测到的直线
if lines is not None:
  for line in lines:
      x1, y1, x2, y2 = line[0]
      cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

      # 计算线段长度
      length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
      # 计算线段的角度和距离
      theta = math.atan2(y2 - y1, x2 - x1)
      rho = x1 * math.cos(theta) + y1 * math.sin(theta)
      #print('length,theta,rho',length,theta,rho)
      
      # 在每条线段的中心点标注rho和theta
      cv2.putText(img, f"rho:{rho:.2f}, theta:{theta:.2f}", (int((x1+x2)/2), int((y1+y2)/2)),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

      '''
      rho1 = np.sqrt(x1**2 + y1**2)
      rho2 = np.sqrt(x2**2 + y2**2)
      theta1 = np.arctan2(y1, x1)
      theta2 = np.arctan2(y2, x2)
      rho = (rho1 + rho2) / 2
      theta = (theta1 + theta2) / 2
      a = np.cos(theta)
      b = np.sin(theta)
      x0 = a * rho
      y0 = b * rho
      pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*a))
      pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*a))
      cv2.line(img, pt1, pt2, (255, 255, 255), 2)
      '''
      '''
      rho,theta = line[0] #rho:图像原点(0,0)到该直线的垂线距离，theta:垂线与图像水平轴之间的夹角
      a = np.cos(theta)
      b = np.sin(theta)
      x0 = a*rho
      y0 = b*rho
      length = int(math.sqrt(w*w + h*h))
      x1 = int(x0 + length*(-b))
      y1 = int(y0 + length*(a))
      x2 = int(x0 - length*(-b))
      y2 = int(y0 - length*(a))

      cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
      '''
else:
  print('No lines detected.')

# 显示结果
cv2.imshow('Hough Lines',img)
cv2.waitKey(0)
cv2.destroyAllWindows()