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
https://www.homeworkhelponline.net/blog/programming/find-rectangles，github: https://github.com/HomeworkHelpOnline/Python-Find_Rectangles
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
img_gray = hough_functions.blur_image(img_gray) 
edged = cv2.Canny(img_gray, 30, 130)#cv2.Canny():边缘检测

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




#找平行线
theta2=theta+np.pi/2
theta3=theta-np.pi/2
difference=np.pi/90
differenceRho=2
accumParallel=[]#parallel平行的
for i in range (0, len(theta)):
    for j in range (i+1, len(theta)):
        if theta[j]>(theta[i]-difference) and theta[j]<(theta[i]+difference):
             if rho[j]<(rho[i]-differenceRho) or rho[j]>(rho[i]+differenceRho):
                accumParallel.append([i,j])

fourLines=[]
#找直角
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
                fourLines.append(np.concatenate([accumParallel[i],accumParallel[j]],1))
    
fourLines=hough_functions.unique(fourLines)

#solve 4 of equations for 4 corners
#rho_j = x cos(theta_j) + y sin(theta_j)
#rho_k = x cos(theta_k) + y sin(theta_k)
corners=[]
for quads in range (0, len(fourLines)):
    cornersTemp=[]
    for lines in range (0,4):
        if lines in [0,1]:
            linesi=lines
            nexti=2
        if lines == 2:
            linesi=0
            nexti=3
        if lines == 3:
            linesi=1
            nexti=1
        b=np.array([rho[fourLines[quads][linesi]],rho[fourLines[quads][linesi+nexti]]])
        a=np.array([[np.cos(theta[fourLines[quads][linesi]]),
                     np.sin(theta[fourLines[quads][linesi]])],
                    [np.cos(theta[fourLines[quads][linesi+nexti]]),
                     np.sin(theta[fourLines[quads][linesi+nexti]])]])
        ans = np.linalg.solve(a, b)
        cornersTemp.append([int(ans[0]),int(ans[1])])
    corners.append(cornersTemp)

#reorder corners
corners=hough_functions.reorderPoints(corners)

#check if valid rectangles
for i in range (len(corners)-1,-1,-1):

    minx=np.min(np.array(corners[i])[:,0])
    maxx=np.max(np.array(corners[i])[:,0])
    miny=np.min(np.array(corners[i])[:,1])
    maxy=np.max(np.array(corners[i])[:,1]) 
    
    height=hough_functions.getLength(corners[i][0],corners[i][1])
    width=hough_functions.getLength(corners[i][2],corners[i][1])
    
    #remove wrongs if small
    if height<20 or width<20 or maxy-miny<10 or maxx-minx<10:
        del corners[i]
        continue
    
    
    xlin=np.array(np.linspace(corners[i][0][0],corners[i][2][0],20)).astype(int)
    ylin=np.array(np.linspace(corners[i][0][1],corners[i][2][1],20)).astype(int)
    xlin2=np.array(np.linspace(corners[i][1][0],corners[i][3][0],20)).astype(int)
    ylin2=np.array(np.linspace(corners[i][1][1],corners[i][3][1],20)).astype(int)
    
    #remove wrong rectangle if std
    std=np.std(np.concatenate([img_gray[(ylin[2:-2]),(xlin[2:-2])],img_gray[(ylin2[2:-2]),(xlin2[2:-2])]]))
    if std>7:
        del corners[i]
        continue
    
    #remove wrongs if brighter
    averageInside=np.average(np.concatenate([img_gray[(ylin[2:-2]),(xlin[2:-2])],img_gray[(ylin2[2:-2]),(xlin2[2:-2])]]))
    corners[i].append(corners[i][0])
    delete=0
    pixelsFromBorder=5
    middlePoint=np.array([(corners[i][0][0]+corners[i][2][0])/2,(corners[i][0][1]+corners[i][2][1])/2])
    for j in range (0,4):        
        y=pixelsFromBorder*np.sin(hough_functions.getAngle([0,0],[1,0],(np.array(corners[i][j+1])+np.array(corners[i][j]))/2-middlePoint,False))
        x=pixelsFromBorder*np.cos(hough_functions.getAngle([0,0],[1,0.01],(np.array(corners[i][j+1])+np.array(corners[i][j]))/2-middlePoint,False))
        a=(np.array(corners[i][j+1])+np.array(corners[i][j]))/2+[int(x),int(y)]
        if img_gray[a[1],a[0]]-averageInside<5:
            delete=1
    if delete==1:
        del corners[i]
        continue
#        
#Removing duplicates
#Here we remove duplicate rectangles by finding the overlapping ones
sumi=np.zeros(len(corners))
middlePoint=np.zeros((len(corners),2))
for i in range (len(corners)-1,-1,-1):
    middlePoint[i]=np.array([(corners[i][0][0]+corners[i][2][0])/2,(corners[i][0][1]+corners[i][2][1])/2])
    #check for edges
    for j in range (0,4):
        x1=corners[i][j][0]
        x2=corners[i][j+1][0]
        y1=corners[i][j][1]
        y2=corners[i][j+1][1]
        if x1!=x2:
            m = (y2-y1)/(1.0*(x2-x1))
            q = y2-m*x2
            x = np.linspace(np.min([x1,x2]),np.min([np.max([x1,x2]),edged.shape[1]-5]),np.absolute(x2-x1)+1)
            y = m*x+q
        else:
            y = np.linspace(np.min([y1,y2]),np.min([np.max([y1,y2]),edged.shape[1]-5]),np.max([y1,y2])-np.min([y1,y2])+1)
            x = x1*np.ones(len(y))
        sumi[i] += np.sum(edged[np.round(y).astype(int),np.round(x).astype(int)])/255.0

maxDistance=10
corners2=[]
corners2.append(len(corners)-1)
for i in range (len(corners)-2,-1,-1):
    found=0
    for j in range (len(corners2)-1,-1,-1):
        if hough_functions.getLength(middlePoint[corners2[j]],middlePoint[i])<=maxDistance:
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




