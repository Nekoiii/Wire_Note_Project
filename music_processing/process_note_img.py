#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理曲谱图片
"""

import cv2
import numpy as np


#把图片中像素>threshold的变为透明,深色的地方都转为白色
def turn_white_to_transparent(png_path,threshold=250):  
    try:
      img = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
      
      
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA  #转RGBA
                         if img.shape[2] == 3 else cv2.COLOR_GRAY2RGBA)
        
      #转换为NumPy数组格式的图像数据
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY) #变成黑白图

      mask = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)[:, :, 0] > threshold
      img[np.where(mask)] = [0, 0, 0, 0]  #白色的地方转为透明
      img[np.where(~mask)] = [255, 255, 255, 255]  #其余都设为白色

      return img
    except Exception as e:
        print("(--turn_white_to_transparent---)Error reloading image:", str(e))
      
      

















