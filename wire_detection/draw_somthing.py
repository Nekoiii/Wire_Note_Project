#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import cv2
import numpy as np
import math
import draw_somthing

def draw_lines(img,lines):
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

  cv2.imshow('Lines',img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  
def draw_sheet(img=None,sheet=None):
  img = cv2.imread('../test_imgs/img-1.jpg', cv2.IMREAD_UNCHANGED)
  sheet=cv2.imread('../test_imgs/sheets/symphony.png', cv2.IMREAD_UNCHANGED)
  x, y = 100, 200

  h, w = sheet.shape[:2]  
  #调整sheet大小
  aspect_ratio = h / w
  new_w = int(0.75 * img.shape[1])
  new_h=int(new_w*aspect_ratio)
  sheet=cv2.resize(sheet,(new_w,new_h))
  
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

draw_sheet()
  
  
  
  
  
  
  

