#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
霍夫变换原理和实现：
https://www.cnblogs.com/php-rearch/p/6760683.html
python代码参考：
https://github.com/alyssaq/hough_transform/blob/master/hough_transform.py
直接用opencv实现：
https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html


*重要参考代码-几乎不使用opencv的检测长方形:(几乎是copy了这里的)
https://www.homeworkhelponline.net/blog/programming/find-rectangles，
https://github.com/HomeworkHelpOnline/Python-Find_Rectangles
*重要参考代码-基于霍夫变换进行线检测
https://blog.csdn.net/algorithmPro/article/details/115499827
"""
import numpy as np
import matplotlib.pyplot as plt
import cv2

import hough_functions

img_path = 'imgs/test_img-1.jpg' #*注:Spyder里记得在Files窗口打开目录文件夹啊!
img_rgb=np.array(plt.imread(img_path)) 
#plt.imshow(img_rgb)
img_gray=hough_functions.rgb2gray(img_rgb)
img_gray = hough_functions.blurImage(img_gray) 
edged = cv2.Canny(img_gray, 30, 130)#cv2.Canny():边缘检测

#开始检测直线
#有时图片会自带边框, 为忽略掉它们这里把边沿5px都设为0
borderLen = 5 
lenx, leny = edged.shape
edged[0:borderLen,0:leny] = 0
edged[lenx-borderLen:lenx,0:leny] = 0
edged[0:lenx,0:borderLen] = 0
edged[0:lenx,leny-borderLen:leny] = 0
plt.imshow(edged) 
#np.set_printoptions(threshold=np.inf) #解决print()数组显示不全的问题
np.set_printoptions(threshold=1000) #恢复缩略显示
#print(edged[2000]) 

#plt.subplots():一纸绘多图。nrows:横轴分成的区域,ncols:纵轴分成的区域,plot_number:当前的绘图区,figsize:绘图区大小
fig, ax1 = plt.subplots(ncols=1, nrows=1, figsize=(8, 4))
ax1.set_axis_off()  #set_axis_off():不显示X轴和Y轴
ax1.imshow(edged, cmap="bone") #这里"bone"是一种颜色
fig.savefig("Rectangles_edged.jpg") #savefig():保存图片


rho,theta = hough_functions.hough_transform(edged,rho_res=1,theta_res=1,
                            thresholdVotes=30,filterMultiple=5,thresholdPixels=0)

print('rho:\n',rho)
print('theta:\n',theta)

hough_functions.plotHoughLines(rho,theta,img_rgb)


#开始检测矩形
theta2=theta+np.pi/2 #theta2=θ+90°
theta3=theta-np.pi/2 #theta3=θ-90°
difference=np.pi/90  #θ差异的阈值
differenceRho=2  #ρ差异的阈值
#找两两相互平行的角度
accumParallel=[] #accumulated:累积的,parallel:平行的
for i in range (0, len(theta)):#遍历θ
  #拿下一个值和它对比,如果θ两头都没超过θ阈值,且ρ超过ρ阈值,则放进去
  for j in range (i+1, len(theta)):
      if theta[j]>(theta[i]-difference) and theta[j]<(theta[i]+difference):
           if rho[j]<(rho[i]-differenceRho) or rho[j]>(rho[i]+differenceRho):
             accumParallel.append([i,j])
print('accumParallel:\n',accumParallel)

accumParallel=np.array(accumParallel)
print('accumParallel:\n',accumParallel)
print('accumParallel:\n',accumParallel.shape)
#找矩形的四条边
fourLines=[]
#accumParallel中的平行角度对进行两两对比,如果能形成直角(即其中有一个在theta2、theta3里的角度
#　分别和另一组平行角度对里其中一个的theta角度对比时两头都没超过阈值),则这两组平行角度对能组成矩形
for i in range (0, len(accumParallel)):
  for j in range (1, len(accumParallel)):
      if     (theta2[accumParallel[j][0]]>(theta[accumParallel[i][0]]-difference) and theta2[accumParallel[j][0]]<(theta[accumParallel[i][0]]+difference)) \
          or (theta2[accumParallel[j][1]]>(theta[accumParallel[i][0]]-difference) and theta2[accumParallel[j][1]]<(theta[accumParallel[i][0]]+difference)) \
          or (theta2[accumParallel[j][0]]>(theta[accumParallel[i][1]]-difference) and theta2[accumParallel[j][0]]<(theta[accumParallel[i][1]]+difference)) \
          or (theta2[accumParallel[j][1]]>(theta[accumParallel[i][1]]-difference) and theta2[accumParallel[j][1]]<(theta[accumParallel[i][1]]+difference)) \
          or (theta3[accumParallel[j][0]]>(theta[accumParallel[i][0]]-difference) and theta3[accumParallel[j][0]]<(theta[accumParallel[i][0]]+difference)) \
          or (theta3[accumParallel[j][1]]>(theta[accumParallel[i][0]]-difference) and theta3[accumParallel[j][1]]<(theta[accumParallel[i][0]]+difference)) \
          or (theta3[accumParallel[j][0]]>(theta[accumParallel[i][1]]-difference) and theta3[accumParallel[j][0]]<(theta[accumParallel[i][1]]+difference)) \
          or (theta3[accumParallel[j][1]]>(theta[accumParallel[i][1]]-difference) and theta3[accumParallel[j][1]]<(theta[accumParallel[i][1]]+difference)):
            print('accumParallel[i]:\n',accumParallel[i],'\n',accumParallel[i].shape)
            print('accumParallel[j]:\n',accumParallel[j],'\n',accumParallel[j].shape)
            accumParallel_ij=[accumParallel[i],accumParallel[j]]
            print('accumParallel_ij-1\n',accumParallel_ij)
            accumParallel_ij=np.array([accumParallel[i],accumParallel[j]])
            print('accumParallel_ij-2\n',accumParallel_ij,'\n',accumParallel_ij.shape)
            v=np.vstack((accumParallel[i],accumParallel[j]))
            print('v\n',v,'\n',v.shape)
            #*原文章这样写np.concatenate()会报错,而且后面自定义函数unique()中也是用的一维,不知道是不是原文错了???
            #fourLines.append(np.concatenate([accumParallel[i],accumParallel[j]],1))             
            fourLines.append(np.concatenate([accumParallel[i],accumParallel[j]],0))             
            #如果按原文的方式拼接,可以用np.vstack()代替np.concatenate(,axis=1)
            #fourLines.append(np.vstack((accumParallel[i],accumParallel[j])))             
            #print('fourLines\n',fourLines,'\n',fourLines.shape)
            print('fourLines\n',fourLines)
      '''break #*for test
  if len(fourLines)>0:
    break'''
  
fourLines=hough_functions.unique(fourLines) #去重
print('fourLines:\n',fourLines)


#找四个角
corners=[]
for quads in range (0, len(fourLines)): #遍历每对四角度的组合 #quads:四倍;四方院;四胞胎之一
  cornersTemp=[]
  for lines in range (0,4):
    if lines in [0,1]:#第0、2线的lines_i为0, 而1、3的为1
        lines_i=lines#第0、1线的next_i为2, 2的为3,3的为1
        next_i=2
    if lines == 2:
        lines_i=0
        next_i=3
    if lines == 3:
        lines_i=1
        next_i=1
    #a为:(j、k代表当前线和next线)
    #rho_j = x cos(theta_j) + y sin(theta_j)
    #rho_k = x cos(theta_k) + y sin(theta_k)
    a=np.array([[np.cos(theta[fourLines[quads][lines_i]]),
                 np.sin(theta[fourLines[quads][lines_i]])],
                [np.cos(theta[fourLines[quads][lines_i+next_i]]),
                 np.sin(theta[fourLines[quads][lines_i+next_i]])]])
    #b为j、k的角度θ对应在rho里的ρ
    b=np.array([rho[fourLines[quads][lines_i]],\
                rho[fourLines[quads][lines_i+next_i]]])
    #np.linalg.solve(a,b)以矩阵形式给出线性方程组的解。a为系数矩阵,b为线性方程组的等号右边的值。官方文档https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html
    #解出的x、y值即为交点坐标
    ans = np.linalg.solve(a, b)
    cornersTemp.append([int(ans[0]),int(ans[1])])
  corners.append(cornersTemp)

#print('corners\n',corners)
#四角重新排序
corners=hough_functions.reorderPoints(corners)

#过滤掉没用的矩形
print('len-1',len(corners)-1)
for i in range (len(corners)-1,-1,-1):#*?为什么要从后往前遍历
  print('len-2',len(corners)-1)
  if len(corners)<1:
    break
  minx=np.min(np.array(corners[i])[:,0])
  maxx=np.max(np.array(corners[i])[:,0])
  miny=np.min(np.array(corners[i])[:,1])
  maxy=np.max(np.array(corners[i])[:,1]) 
  #print('orners[i]:',corners[i])

  #去除太小的矩形
  height=hough_functions.getLength(corners[i][0],corners[i][1])
  width=hough_functions.getLength(corners[i][2],corners[i][1])
  if height<20 or width<20 or maxy-miny<10 or maxx-minx<10:
      del corners[i]
      continue
    
  #去除标准差过高的矩形  #*?这里没太懂为什么标准差高就更可能超出图片范围外?
  #If standard deviation is high, that may mean that rectangles has ended 
  #somewhere inside area of our corners. But this check is the one which 
  #restricts the code work only with solid rectangles. 
  xlin=np.array(np.linspace(corners[i][0][0],corners[i][2][0],20)).astype(int)
  ylin=np.array(np.linspace(corners[i][0][1],corners[i][2][1],20)).astype(int)
  xlin2=np.array(np.linspace(corners[i][1][0],corners[i][3][0],20)).astype(int)
  ylin2=np.array(np.linspace(corners[i][1][1],corners[i][3][1],20)).astype(int)
  #np.std()计算标准差。默认axis=None,求全局标准差。axis=0求每一列标准差,axis=1求每一行标准差。
  std=np.std(np.concatenate([img_gray[(ylin[2:-2]),(xlin[2:-2])],\
                             img_gray[(ylin2[2:-2]),(xlin2[2:-2])]]))
  print('std:',std)
  #*?原文里是7,这个数字该怎么选?
  #if std>7:
  if std>20:
      del corners[i]
      continue

  #*?这里也没太看懂
  #Remove if brighter: The requirement by task is fulfilled by checking the 
  #outer color of the rectangle. It is completed by selecting four points 
  #outside rectangle in the line from the midpoint to all for middles of sides.
  #np.average()计算平均值
  averageInside=np.average(np.concatenate([img_gray[(ylin[2:-2]),(xlin[2:-2])],\
                                           img_gray[(ylin2[2:-2]),(xlin2[2:-2])]]))
  print('corners[i]',corners[i])
  corners[i].append(corners[i][0])#第四角后连上第一角
  delete=0
  pixelsFromBorder=5
  #middlePoint是该矩形中心的坐标。平行四边形的中心是对角线的交点
  middlePoint=np.array([(corners[i][0][0]+corners[i][2][0])/2,\
                        (corners[i][0][1]+corners[i][2][1])/2])
  for j in range (0,4):        
      y=pixelsFromBorder*np.sin(hough_functions.getAngle([0,0],[1,0],\
          (np.array(corners[i][j+1])+np.array(corners[i][j]))/2-middlePoint,False))
      x=pixelsFromBorder*np.cos(hough_functions.getAngle([0,0],[1,0.01],\
          (np.array(corners[i][j+1])+np.array(corners[i][j]))/2-middlePoint,False))
      a=(np.array(corners[i][j+1])+np.array(corners[i][j]))/2+[int(x),int(y)]
      if img_gray[int(a[1]),int(a[0])]-averageInside<5:
          delete=1
  if delete==1:
      del corners[i]
      continue

#去除部分重叠的矩形(同片区域只保留最好的一个)
sumi=np.zeros(len(corners))
middlePoint=np.zeros((len(corners),2))
for i in range (len(corners)-1,-1,-1):
  middlePoint[i]=np.array([(corners[i][0][0]+corners[i][2][0])/2,\
                           (corners[i][0][1]+corners[i][2][1])/2])
  #check for edges
  for j in range (0,4):
    x1=corners[i][j][0]
    x2=corners[i][j+1][0]
    y1=corners[i][j][1]
    y2=corners[i][j+1][1]
    if x1!=x2:
        m = (y2-y1)/(1.0*(x2-x1))
        q = y2-m*x2
        x = np.linspace(np.min([x1,x2]),np.min([np.max([x1,x2]),\
                        edged.shape[1]-5]),np.absolute(x2-x1)+1)
        y = m*x+q
    else:
        y = np.linspace(np.min([y1,y2]),np.min([np.max([y1,y2]),\
                        edged.shape[1]-5]),np.max([y1,y2])-np.min([y1,y2])+1)
        x = x1*np.ones(len(y))
    sumi[i] += np.sum(edged[np.round(y).astype(int),\
                            np.round(x).astype(int)])/255.0
if len(corners)>0:
  maxDistance=10
  corners2=[]
  corners2.append(len(corners)-1)
  for i in range (len(corners)-2,-1,-1):
      found=0
      for j in range (len(corners2)-1,-1,-1):
          if hough_functions.getLength(
              middlePoint[corners2[j]],middlePoint[i])<=maxDistance:
              found=1
              if sumi[i]>sumi[corners2[j]]:
                  corners2[j]=i
      if found==0:
          corners2.append(i)
  
  fig2, ax1 = plt.subplots(ncols=1, nrows=1, figsize=(8, 4))
  ax1.imshow(img_rgb)
  ax1.set_axis_off()
  for i in corners2:   
      corners[i].append(corners[i][0])
      for j in range (0,4):
          ax1.plot( [corners[i][j][0],corners[i][j+1][0]],[corners[i][j][1],corners[i][j+1][1]], 'xb-',linewidth=3)
  
ax1.set_ylim([img_gray.shape[0],0])
ax1.set_xlim([0,img_gray.shape[1]])
fig2.savefig("Example4.jpg")
if len(corners)>0:
    plt.show()
else:
    print ('No rectangles were found')
