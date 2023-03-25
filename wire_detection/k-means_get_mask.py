#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取background, 生成mask（背景中电线会被分为前景、效果不太好
"""

import cv2
import numpy as np

# 读取图像
img = cv2.imread('../test_imgs/img-1.jpg')
# 转换为RGB格式
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# KMeans聚类
# 设置聚类数为2，第一个聚类中心为白色，第二个为黑色
K = 2
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
flags = cv2.KMEANS_RANDOM_CENTERS
Z = gray.reshape((-1, 1))
Z = np.float32(Z)
ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, flags)

# 标记背景区域
label = label.reshape(gray.shape)
background_label = np.argmin(center)
background_mask = np.zeros_like(gray)
background_mask[label == background_label] = 255

for i in range(1000):
  # 开运算，消除细节
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
  background_mask = cv2.morphologyEx(background_mask, cv2.MORPH_OPEN, kernel)

for i in range(1000):
  # 闭运算，填充小孔
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
  background_mask = cv2.morphologyEx(background_mask, cv2.MORPH_CLOSE, kernel)

# 显示结果
cv2.imshow('img & mask', np.hstack((gray,background_mask)))
cv2.waitKey(0)
cv2.destroyAllWindows()











