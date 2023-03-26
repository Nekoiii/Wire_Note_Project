#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hough变换检测电线
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import draw_somthing

def hough_line(img,gray,threshold=False,IF_SHOW=True):  
  
  # 边缘检测
  edges = cv2.Canny(gray,50,150,apertureSize = 3)
  
  # 根据图像面积动态调整后面cv2.HoughLines()里的threshold参数
  w=gray.shape[0]
  h=gray.shape[1]
  img_area = w * h  
  if threshold==False:
    if img_area > 500000:
        threshold = 500
    elif  img_area >100000:
        threshold = int(img_area * 0.0005)
    else:
        threshold = 100
    print('img_area',img_area)
  
  # 霍夫变换检测直线
  '''
  1: 表示直线距离rho的精度, 一般取1。
  np.pi/180: 直线角度theta的精度, 一般取np.pi/180。
  threshold: 检测直线的阈值, ，取值越大, 检测到的直线越少。
  maxLineGap: 如果两个线段之间的间隔大于maxLineGap, 则它们被认为是两条不同的直线
  '''
  #lines = cv2.HoughLines(edges,1,np.pi/180,threshold=threshold)
  lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=threshold, 
                          minLineLength=50, maxLineGap=50)
  
  # 绘制检测到的直线
  if lines is not None:
    print(len(lines),'lines detected.')
    '''
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
  else:
    lines=[]
    print('No lines detected.')
  '''
  # 显示结果
  cv2.imshow('Hough Lines',img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  '''

  return(lines)
  
  
def hough_circle(img,gray):
  # 边缘检测
  edges = cv2.Canny(gray, 100, 200, apertureSize=3)
  
  # EHT
  '''
  param1: Canny边缘检测算法的高阈值，用于控制边缘检测的敏感度。
  param2: Hough变换的阈值，用于控制检测直线的强度。
  minRadius: 检测到的圆的最小半径，用于过滤掉较小的圆。
  maxRadius: 检测到的圆的最大半径，用于过滤掉较大的圆。
  '''
  circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 20,
                             param1=100, param2=100, 
                             minRadius=int(0.1*max(gray.shape[:2])), maxRadius=int(0.5*max(gray.shape[:2])))
  print('circles',circles)
  # 绘制检测到的圆
  if circles is not None:
      circles = np.uint16(np.around(circles))
      for i in circles[0, :]:
          # 绘制圆
          cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
          # 绘制圆心
          cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

  # 显示图像
  cv2.imshow('image', img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  
  
  
if __name__ == '__main__':
  img = cv2.imread('../test_imgs/img-1.jpg')
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  lines=hough_line(img,gray)
  #hough_circle(img,gray)  #*本来想试试HoughCircles找有点弧度的电线的但效果不太好而且巨慢
  draw_somthing.draw_lines(img,lines)


