#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
watershed检测出的marker中的背景作为天空，然后用hough在里面检测直线
"""
import cv2  
import numpy as np
import hough  
import draw_somthing
import math


img_name='img-8'
img = cv2.imread('../test_imgs/'+img_name+'.jpg')
img_mask = cv2.imread('../test_imgs/masks/'+img_name+'_mask.png', cv2.IMREAD_GRAYSCALE)
if img_mask is None:
    print("Failed to read mask image!")
    img_mask = np.zeros(img.shape[:2], dtype=np.uint8)
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#print('img',img,'\n img_mask',img_mask)

 #调转前景背景颜色
img_mask = img_mask ^ 255  #也可用：img_mask = np.where(img_mask == 0, 255, 0)
#print('img',img,'\n img_mask',img_mask)

'''
cv2.imshow('img & mask',np.hstack((img , img_mask)))
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

 # 在标注为非零值的区域进行 Hough 检测直线
img_hough = cv2.bitwise_and(img_gray, img_gray, mask=img_mask)

'''
print('img_hough(mask)',img_hough)
cv2.imshow('img_hough', img_hough)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''


# 根据mask面积调整threshold 
count = np.count_nonzero(img == 255)
if count > 5000:
    threshold = 250
elif  count >1000:
    threshold = int(count * 0.05)
else:
    threshold = 100
lines=hough.hough_line(img,img_hough,threshold)
draw_somthing.draw_lines(img,lines) 



'''
'''
if len(lines)>0:
  img_mask_bool = img_mask.astype(bool)
  lengths=[]
  thetas=[]
  rhos=[]
  x_counter=0
  y_counter=0
  for index,line in enumerate(lines):
    counter_img=np.zeros_like(img)
    x1, y1, x2, y2 = line[0]
    diagonal_length = math.sqrt(counter_img.shape[0]**2 + counter_img.shape[1]**2)
    # 计算线段两端点的延长点坐标
    dx = (x2 - x1) * int(diagonal_length)
    dy = (y2 - y1) * int(diagonal_length)
    x1_extended = x1 - dx
    y1_extended = y1 - dy
    x2_extended = x2 + dx
    y2_extended = y2 + dy
    
    cv2.line(counter_img, (x1_extended, y1_extended), (x2_extended, y2_extended), (255,255,255), 1)
    counter_img[~img_mask_bool] = 0
    
    # 计算255的个数
    line_length = np.count_nonzero(counter_img == 255)
    
    #print('line ',index,' length: ',line_length)
    '''
    cv2.imshow('counter_img',counter_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
    
    # 计算线段的极坐标中角度和距离
    theta = math.atan2(y2 - y1, x2 - x1)
    rho = x1 * math.cos(theta) + y1 * math.sin(theta)
    #print('theta,rho',theta,rho)
    lengths.append(line_length)
    thetas.append(theta)
    rhos.append(rho)
    x_counter+=x1+x2
    y_counter+=y1+y2


  avg_theta=sum(thetas)/len(lengths)
  angle = -math.degrees(avg_theta) #不知道为什么是反的
  avg_len=sum(lengths)/len(lengths)
  avg_x=x_counter/(2*len(lengths))
  avg_y=y_counter/(2*len(lengths))
  print('theta,angle,avg_len,avg_x,avg_y',avg_theta,angle,avg_len,avg_x,avg_y)
  
  sheet=cv2.imread('../test_imgs/sheets/symphony.png', cv2.IMREAD_UNCHANGED)
  lines_img=draw_somthing.draw_sheet(img,sheet,avg_x,avg_y,angle) 



