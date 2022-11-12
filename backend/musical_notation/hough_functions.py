#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
霍夫变换等函数
"""

import numpy as np
import scipy.signal as sp
import math
import matplotlib.pyplot as plt
import cv2







#进行霍夫变换
'''def hough_transform(img, angle_step=1,value_threshold=5):
  thetas = np.deg2rad(np.arange(-90.0, 90.0, angle_step))#np.deg2rad()角度制转弧度制 
  width, height = img.shape
  diag_len = int(round(math.sqrt(width * width + height * height)))
  rhos = np.linspace(-diag_len, diag_len, diag_len * 2)#np.linspace()创建等差数列
  
  #一些常用值
  cos_theta = np.cos(thetas)
  sin_theta = np.sin(thetas)
  num_thetas = len(thetas)

  # Hough accumulator array of theta vs rho
  accumulator = np.zeros((2 * diag_len, num_thetas))
  are_edges = cv2.Canny(img,50,150,apertureSize = 3)
  
  y_idxs, x_idxs = np.nonzero(are_edges)  # np.nonzero()返回array中非零元素索引
  
  # Vote in the hough accumulator
  xcosthetas = np.dot(x_idxs.reshape((-1,1)), cos_theta.reshape((1,-1)))
  ysinthetas = np.dot(y_idxs.reshape((-1,1)), sin_theta.reshape((1,-1)))
  rhosmat = np.round(xcosthetas + ysinthetas) + diag_len
  rhosmat = rhosmat.astype(np.int16)
  for i in range(num_thetas):
      rhos,counts = np.unique(rhosmat[:,i], return_counts=True)
      accumulator[rhos,i] = counts
  return accumulator, thetas, rhos

#绘制映射到霍夫空间的图像
def show_hough_line(img, accumulator, thetas, rhos, save_path=None):
  fig, ax = plt.subplots(1, 2, figsize=(10, 10))

  ax[0].imshow(img, cmap=plt.cm.gray)
  ax[0].set_title('Input img')
  ax[0].axis('img')

  ax[1].imshow(
      accumulator, cmap='jet',
      extent=[np.rad2deg(thetas[-1]), np.rad2deg(thetas[0]), rhos[-1], rhos[0]])
  ax[1].set_aspect('equal', adjustable='box')
  ax[1].set_title('Hough transform')
  ax[1].set_xlabel('Angles (degrees)')
  ax[1].set_ylabel('Distance (pixels)')
  ax[1].axis('img')

  # plt.axis('off')
  if save_path is not None:
      plt.savefig(save_path, bbox_inches='tight')
  plt.show()
  
def plotHoughLines(rho,theta,img):
  a = np.cos(theta)
  b = np.sin(theta)
  x0 = a*rho
  y0 = b*rho

  fig2, ax1 = plt.subplots(ncols=1, nrows=1)
  ax1.imshow(img)
  
  for i in range (0, len(rho)):   
      ax1.plot( [x0[i] + 1000*(-b[i]), x0[i] - 1000*(-b[i])],
                [y0[i] + 1000*(a[i]), y0[i] - 1000*(a[i])], 
                'xb-',linewidth=3)
  
  ax1.set_ylim([img.shape[0],0])
  ax1.set_xlim([0,img.shape[1]])
  
  plt.show()'''
#rho_res、theta_res一般用1
def hough_transform(edged,rho_res,theta_res,thresholdVotes,filterMultiple,thresholdPixels=0):
  rows, columns = edged.shape
  theta = np.linspace(-90.0, 0.0, np.ceil(90.0/theta_res) + 1.0)#np.linspace()创建等差数列
  theta = np.concatenate((theta, -theta[len(theta)-2::-1]))
  
  #霍夫空间中 x= theta, y= x*cos(theta)+y*sin(theta)
  #角度制转弧度制公式: 1度=π/180≈0.01745弧度，1弧度=180/π≈57.3度
  diagonal = np.sqrt((rows - 1)**2 + (columns - 1)**2)#原坐标系里图片对角线的长度作为新坐标系
  q = np.ceil(diagonal/rho_res)
  nrho = 2*q + 1
  rho = np.linspace(-q*rho_res, q*rho_res, nrho)
  houghMatrix = np.zeros((len(rho), len(theta)))
  
  for rowId in range(rows):                              
      for colId in range(columns):                        
        if edged[rowId, colId]>thresholdPixels:  #pixel一般为0 ~ 255 
          #计算rhoVal,然后映射到霍夫空间
          for thId in range(len(theta)):
            rhoVal = colId*np.cos(theta[thId]*np.pi/180.0) + \
                rowId*np.sin(theta[thId]*np.pi/180)
            #np.nonzero()得到数组array中非零元素的位置。np.abs()绝对值
            #**这里没懂为什么要
            rhoIdx = np.nonzero(np.abs(rho-rhoVal) == np.min(np.abs(rho-rhoVal)))[0] 
            houghMatrix[rhoIdx[0], thId] += 1  
          
 
 #cluster and filter multiple dots in Houghs plane
  if filterMultiple>0:
      clusterDiameter=filterMultiple
      values=np.transpose(np.array(np.nonzero(houghMatrix>thresholdVotes)))
      filterArray=[]
      filterArray.append(0)
      totalArray=[]
      for i in range (0, len(values)):
          if i in filterArray[1::]:
              continue
          tempArray=[i]
          for j in range (i+1, len(values)):
              if j in filterArray[1::]:
                  continue
              for k in range (0, len(tempArray)):
                  if getLength(values[tempArray[k]],values[j])<clusterDiameter:
                      filterArray.append(j)
                      tempArray.append(j)
                      break
          totalArray.append(tempArray)
      
      #leave the highest value in each cluster
      #*这里ii、jj/i、j为什么要设为0
      for i in range (0, len(totalArray)):
           for j in range (0, len(totalArray[i])):
               if j==0:
                   highest=houghMatrix[values[totalArray[i][j]][0],values[totalArray[i][j]][1]]
                   ii=i
                   jj=j
               else:
                   if houghMatrix[values[totalArray[i][j]][0],values[totalArray[i][j]][1]]>=highest:
                       highest=houghMatrix[values[totalArray[i][j]][0],values[totalArray[i][j]][1]]
                       houghMatrix[values[totalArray[ii][jj]][0],values[totalArray[ii][jj]][1]]=0
                       ii=i
                       jj=j
                   else:
                       houghMatrix[values[totalArray[i][j]][0],values[totalArray[i][j]][1]]=0
                  
  return (np.where(houghMatrix>thresholdVotes)[0]-q)*rho_res, theta[np.where(houghMatrix>thresholdVotes)[1]]*np.pi/180.0

#计算两点的距离, startPoint、secondPoint格式: [x,y] 
def getLength(startPoint,secondPoint):
    v1x=secondPoint[0]-startPoint[0]
    v1y=secondPoint[1]-startPoint[1]
    lenv=np.sqrt(v1x*v1x+v1y*v1y)
    return lenv
  

#去除array中的重复项,a: list of 1xN arrays,返回值b: array
def unique(a):
    #a=np.array([[ 1,  3, 12, 17],[ 1,  3, 17, 12],[ 1,  3, 18, 20]]) #Example
    #print('a: \n',a)
    b=np.array(a)
    a=np.sort(np.array(a)) #np.sort():数组排序。axis=0 按列排序, axis=1 按行排序。
    #print('np.sort(np.array(a)): \n',a)
    #print('a.T: \n',a.T)
    order = np.lexsort(a.T)  #np.lexsort():多级排序,优先按后面的列来从小到大排序
    #print('order: ',order)
    a = a[order]
    b = b[order]
    #print('a[order]: \n',a,'\n b[order]: \n',b)
    diff = np.diff(a, axis=0) #np.diff(): 计算沿给定轴的n阶离散差。out[i] = a[i+1] - a[i] 
    #print('diff: \n',diff)
    ui = np.ones(len(a), 'bool')  #np.ones()创建全1数组。dtype指定数组的所需数据类型(这里用了'bool')
    #print('ui-initial: \n',ui,'\n ui[1:]: \n',ui[1:])
    #这里ui[1:]去掉第一行是因为diff计算a等差时没有第一行
    ui[1:] = (diff != 0).any(axis=1) #numpy.array.any():判断array中是否至少有一个值为True。axis=1按列。https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.any.html
    #print('ui: \n',ui,'\n b[ui]: \n',b[ui])
    return b[ui] #b[ui]留下了a中diff不全为0的行
  
def rgb2gray(rbg_img):  #RGB彩图转灰度图(convert a color img to grayscale)  
  #np.dot(): 计算向量点积
  #RGB转灰度的常用参数[0.2989, 0.5870, 0.1140]     
  return np.dot(rbg_img[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)

def blur_image(img_gray): #滤波函数。类似于cv里的filter2d()
    #skipped first line and first column to keep it more simple (it's zeroed out anyway).
    #for every pixel we change it with the average of 4 pixels.
    kernel = np.ones((2,2),np.float32)/4  #Blurring kernel
    res=sp.convolve2d(img_gray,kernel,mode='same')#scipy.signal.convolve2d():进行卷积
    return np.round(res).astype(np.uint8)




