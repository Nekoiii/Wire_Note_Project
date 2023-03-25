#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
watershed检测出的marker中的背景作为天空，然后用hough在里面检测直线
"""
import cv2  
import numpy as np
import hough  

img_name='img-7'
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

print('img_hough',img_hough)
cv2.imshow('img_hough', img_hough)
cv2.waitKey(0)
cv2.destroyAllWindows()

hough.hough_line(img,img_hough)
 
 



