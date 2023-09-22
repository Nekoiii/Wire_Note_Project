#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
watershed检测出的marker中的背景作为天空，然后用hough在里面检测直线
"""
import os
import cv2  
import numpy as np
import math
import glob

import hough  
import main_scripts.draw_somethings.draw_something as draw_something
import watershed

        
 
#目前只应对jpg文件
def detect_wires_1(img_name,IF_SHOW=True):
  img = cv2.imread('../test_imgs/'+img_name+'.jpg')
  img_old=img.copy()
  img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  
  watershed_mask,watershed_mask_color=watershed.get_watershed_mask(img, img_gray,img_name,IF_SHOW)
  
  
  img_mask = cv2.imread('../test_imgs/masks/'+img_name+'_mask.png', cv2.IMREAD_GRAYSCALE)
  if img_mask is None:
      print("Failed to read mask image!")
      img_mask = np.zeros(img.shape[:2], dtype=np.uint8)
  
  
  
  #调转前景背景颜色
  img_mask = img_mask ^ 255  #也可用：img_mask = np.where(img_mask == 0, 255, 0)
  #print('img',img,'\n img_mask',img_mask)
  
  '''
  cv2.imshow('img & mask',np.hstack((img , img_mask)))
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  '''
  
  # img_gray中只留下mask中标注为非零值的区域(只检测背景上的直线)
  img_gray = cv2.bitwise_and(img_gray, img_gray, mask=img_mask)
  
  '''
  print('img_gray(mask)',img_gray)
  cv2.imshow('img_gray', img_gray)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  '''
  
  # 根据mask面积调整threshold 
  count = np.count_nonzero(img_mask == 255)
  #print('count',count)
  if count > 500000:
      threshold = 250
  elif  count >100000:
      threshold = int(count * 0.0005)
  else:
      threshold = 100
  lines=hough.hough_line(img,img_gray,threshold,IF_SHOW)
  img_with_lines=draw_something.draw_lines(img,lines,IF_SHOW) 
  
  
  #在所有检测出的直线平均坐标、平均角度放上音符
  if len(lines)>0:
    img_mask_bool = img_mask.astype(bool)
    lengths=[]
    thetas=[]
    rhos=[]
    x_counter=0
    y_counter=0
    extension_lines=img.copy()
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
      cv2.line(extension_lines, (x1_extended, y1_extended), (x2_extended, y2_extended), (0,0,255), 2)
      #print('cccc-1',(counter_img == 255).sum(),counter_img.shape)
      counter_img[~img_mask_bool] = 0
      extension_lines[~img_mask_bool] = img[~img_mask_bool]
      #print('cccc-2',(counter_img == 255).sum(),diagonal_length)
            
      
      line_length = (counter_img == 255).sum() # *problem:本来想用255的个数来计算线的长度, 但发现出来的数不对
      #print('line_length_0: ',line_length_0,' line_length: ',line_length)

      '''
      cv2.imshow('counter_img',counter_img)
      cv2.waitKey(0)
      cv2.destroyAllWindows()
      '''
      
      # 计算线段的极坐标中角度和距离
      theta = math.atan2(y2 - y1, x2 - x1)
      rho = x1 * math.cos(theta) + y1 * math.sin(theta)
      #print('theta,rho',theta,rho)
      lengths.append(line_length)
      thetas.append(theta)
      rhos.append(rho)
      x_counter+=x1+x2
      y_counter+=y1+y2
  
  
    avg_theta=sum(thetas)/len(thetas)
    angle = -math.degrees(avg_theta) #*注意这里角度是反的
    avg_len=sum(lengths)/len(lengths)
    avg_x=x_counter/(2*len(lengths))
    avg_y=y_counter/(2*len(lengths))
    #print('theta,angle,avg_len,avg_x,avg_y',avg_theta,angle,avg_len,avg_x,avg_y)
    #print('lengths---',lengths,img.shape)
    
    #画音符
    sheet=cv2.imread('../test_imgs/sheets/symphony.png', cv2.IMREAD_UNCHANGED)
    assert sheet is not None, "file could not be read, check with os.path.exists()"
    #img_with_sheet=draw_somthing.draw_sheet(img,sheet,avg_x,avg_y,angle,0.75 * avg_len,IF_SHOW) 
    img_with_sheet=draw_something.draw_sheet(img,sheet,avg_x,avg_y,angle,-1,IF_SHOW) 

    
    output_img=np.vstack((
        np.hstack((img_old,watershed_mask_color,watershed_mask)),
        np.hstack((img_with_lines,extension_lines,img_with_sheet))))



    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../test_imgs', 'output_1')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cv2.imwrite(os.path.join(output_dir, img_name+'_output_1'+'.png'), output_img)
  
def loop_through_jpg_files(folder_path):
    os.chdir(folder_path) # 将当前工作目录更改为所提供的文件夹路径
    for file in glob.glob("*.jpg"): # 查找所有以 .jpg 结尾的文件
        #print('file--',file.split(".")[0])
        detect_wires_1(file.split(".")[0],False)


loop_through_jpg_files('../test_imgs/')      
#detect_wires_1('img-6')
#detect_wires_1('img-6',False)
