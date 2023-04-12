#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理曲谱图片
"""

import cv2
import numpy as np


#把图片中像素>threshold的变为透明,深色的地方都转为白色
def turn_white_to_transparent(png_path,threshold=250):
    #print('turn_white_to_transparent----')
  
    try:
      img = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
      if img is not None:
          img= cv2.imread(png_path, cv2.IMREAD_UNCHANGED)


          if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
          elif img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
            
          '''
          cv2.imshow('img',img)
          cv2.waitKey(0)
          cv2.destroyAllWindows()
          '''
            
          #转换为NumPy数组格式的图像数据
          gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
          _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
          thresh_rgba = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGBA)
          
          mask = thresh_rgba[:, :, 0] > threshold
          img[np.where(mask)] = [0, 0, 0, 0]  #白色的地方转为透明
          img[np.where(~mask)] = [255, 255, 255, 255]  #其余都设为白色

          return img

      else:
          raise Exception("Failed to read image from file")
    except Exception as e:
        print("Error reloading image:", str(e))
      
      

















