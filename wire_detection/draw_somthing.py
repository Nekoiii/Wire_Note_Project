#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import cv2
import numpy as np
import math
import draw_somthing

def draw_lines(img,lines):
  img_draw=img.copy()
  for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img_draw, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # 计算线段长度
    length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    # 计算线段的极坐标中角度和距离
    theta = math.atan2(y2 - y1, x2 - x1)
    rho = x1 * math.cos(theta) + y1 * math.sin(theta)
    #print('length,theta,rho',length,theta,rho)
    
    # 在每条线段的中心点标注rho和theta
    cv2.putText(img_draw, f"rho:{rho:.2f}, theta:{theta:.2f}", (int((x1+x2)/2), int((y1+y2)/2)),
              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
  cv2.imshow('img_draw',img_draw)
  
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  
  
'''
'''
def draw_sheet(img=None,sheet=None,x=100,y=100,angle=0):
  x,y=int(x),int(y)
  
  h, w = sheet.shape[:2]  
  
  #调整sheet大小
  aspect_ratio = h / w
  w = int(0.75 * img.shape[1])
  h=int(w*aspect_ratio)
  sheet=cv2.resize(sheet,(w,h))
  
  #建一个大的图存放sheet,不然旋转后会显示不全
  diagonal_length = math.ceil(math.sqrt(w**2 + h**2))
  new_sheet=np.zeros((diagonal_length, diagonal_length, 4), dtype=np.uint8)
  xx_1=math.ceil(0.5*(diagonal_length-w))
  yy_1=math.ceil(0.5*(diagonal_length-h))
  new_sheet[yy_1:yy_1+h,xx_1:xx_1+w]=sheet
  h, w = new_sheet.shape[:2]
  # 计算旋转矩阵
  center = (w // 2, h // 2)
  M = cv2.getRotationMatrix2D(center, angle, 1.0) 
  # 应用旋转矩阵，旋转图像
  new_sheet = cv2.warpAffine(new_sheet, M, (w, h))
  sheet=new_sheet.copy()
  x,y=int(x-0.5*w),int(y-0.5*h)
  '''
  cv2.imshow("Rotated new_sheet", new_sheet)
  cv2.waitKey(0)
  cv2.destroyAllWindows()  
  '''


  # *要把sheet超出img范围的部分截掉, 不然会报错！
  img_h,img_w=img.shape[:2]
  # 获取在img范围内的sheet部分的坐标
  x_min, y_min = min(max(x, 0),img_w), min(max(y, 0),img_h)
  x_max, y_max = min(x+sheet.shape[1], img_w), min(y+sheet.shape[0], img_h)
  # 获取在sheet范围内对应的部分的坐标
  sheet_x_min, sheet_y_min = x_min - x, y_min - y
  sheet_x_max, sheet_y_max = sheet_x_min + (x_max - x_min), sheet_y_min + (y_max - y_min) 
  
  # 进行绘制，注意要考虑透明通道
  alpha = sheet[:,:,3] / 255.0
  alpha = np.repeat(np.expand_dims(alpha, axis=2), 3, axis=2)
  
  img[y_min:y_max, x_min:x_max] = alpha[sheet_y_min:sheet_y_max, sheet_x_min:sheet_x_max] * sheet[sheet_y_min:sheet_y_max, sheet_x_min:sheet_x_max, :3] + (1-alpha[sheet_y_min:sheet_y_max, sheet_x_min:sheet_x_max]) * img[y_min:y_max, x_min:x_max]


  # 显示结果
  cv2.imshow('result', img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

   
  
  
  
  
  
  

