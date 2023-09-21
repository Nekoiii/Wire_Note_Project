#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鼠标在图片上绘制mask
"""
import cv2
import numpy as np

# 定义变量
drawing = False
points = []
index = 0 #标记现在画的是第几个区域
img_path="../test_imgs/img-1.jpg"
img = cv2.imread(img_path)
img_old=img.copy()
mask = np.zeros_like(img[:,:,0])
mask_old = np.zeros_like(img[:,:,0])
color = np.random.randint(0, 255, (100, 3)) #生成一个100行3列的二维数组，数组中的每个元素都是0到255之间的随机整数


# 定义回调函数
def draw(event, x, y, flags, param):
    global drawing, points,  index, color,img,mask,mask_old,img_old
    #print('masks',masks)

    if event == cv2.EVENT_LBUTTONDOWN: #按下鼠标,开始绘制
        img_old=img.copy()
        drawing = True
        points = [(x, y)]
    
    elif event == cv2.EVENT_MOUSEMOVE: #移动鼠标,
        if drawing == True:
            #画线(连接当前点和上一个点)
            cv2.line(img, points[-1], (x, y), color[index].tolist(), 2)
            points.append((x, y))
    
    elif event == cv2.EVENT_LBUTTONUP: #放开鼠标,首尾相连闭合图形
        mask_old=mask.copy()
        drawing = False
        cv2.line(img, points[-1], points[0], color[index].tolist(), 2)
        points.append(points[0])
        index += 1
        
        #把mask中对应区域填充为白色
        points_array = np.array(points)  #将points中的点的坐标转换成数组    
        pts = points_array.reshape((-1, 1, 2))  #每个点的行向量组合成一个列表      
        print('points',points,'points_array',points_array,'pts',pts)#pts打印出的结果中有三重方括号，第一重方括号表示轮廓列表，第二重方括号表示轮廓的一个点列表，第三重方括号表示一个点的横纵坐标。
        cv2.fillPoly(mask,[pts],(255,255,255)) 

    elif event == cv2.EVENT_RBUTTONDOWN: #右键点击, 撤销上一次的绘制
        mask=mask_old.copy()
        img=img_old.copy()
                 
# 创建窗口并绑定回调函数
cv2.namedWindow("draw-mask")
cv2.setMouseCallback("draw-mask", draw)

# 循环处理
while True:
    cv2.imshow("draw-mask", img)
    key = cv2.waitKey(1) & 0xFF  #获得键盘输入的ASCII码值。一个整数的二进制表示占据了32位，但是cv2.waitKey（）只会返回32位整数中的低8位。按位与运算符&可以用来获得这个低8位。0xFF的二进制表示为11111111，使用按位与运算符&可以将32位整数的高24位全部清零，只留下低8位
    if key == ord("c") : #c完成绘制
        break
    elif key == ord("q"): #q退出
        masks = []
        break
     
cv2.imshow("mask", mask)
cv2.waitKey(0)
#print('mask',mask)

# 释放资源
cv2.destroyAllWindows()







