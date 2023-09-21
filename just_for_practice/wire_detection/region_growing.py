#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
region_growing
"""


import cv2
import numpy as np

# 读取图像
img = cv2.imread('../test_imgs/img-1.jpg', cv2.IMREAD_GRAYSCALE)

# 定义区域生长的函数
def region_growing(img, seed):
    # 定义种子点的邻域
    neighborhood = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # 定义输出图像的大小和类型
    h, w = img.shape[:2]
    res = np.zeros((h, w), dtype=np.uint8)

    # 定义种子点列表和生长列表
    seed_list = [seed]
    grow_list = []

    # 开始生长
    while len(seed_list) > 0:
        # 取出种子点
        cur_point = seed_list.pop(0)
        grow_list.append(cur_point)

        # 遍历种子点的邻域
        for i in range(4):
            x = cur_point[0] + neighborhood[i][0]
            y = cur_point[1] + neighborhood[i][1]

            # 如果邻域点符合生长条件，将其添加到种子点列表中
            if x >= 0 and y >= 0 and x < h and y < w and res[x][y] == 0 and abs(int(img[x][y]) - int(img[cur_point])) < 20:
                res[x][y] = 255
                seed_list.append((x, y))

    return res

# 随机选择一个种子点进行区域生长
seed_point = (50, 50)
seg_img = region_growing(img, seed_point)

# 显示结果
cv2.imshow('Original', img)
cv2.imshow('Segmentation', seg_img)
cv2.waitKey(0)
cv2.destroyAllWindows()






