#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
霍夫变换(hough transform)等函数
"""
import numpy as np
import scipy.signal as sp
import math
import matplotlib.pyplot as plt
import cv2

#进行霍夫变换
#edged输入图像
#rho_res距离精度(单位是像素),theta_res角度精度(单位是弧度)。这里的'精度'相当于步长,这俩一般用1就好了。
#thresholdVotes指定在累加平面中阈值,大于它的直线才会被返回。
#filterMultiple指定在相邻一定距离内,只留一条值最大的线。
#thresholdPixels指定边缘的阈值,大于它的像素点都会被认为是边缘。(深色背景,浅色边缘)
def hough_transform(edged,rho_res,theta_res,thresholdVotes,filterMultiple,thresholdPixels=0):
  #笛卡尔坐标系x-y,笛卡尔坐标转霍夫空间k-q,极坐标转霍夫空间θ-ρ(读作theta-rho)
  #极坐标霍夫空间中, 横轴θ, 竖轴 ρ=x*cosθ+y*sinθ
  #角度制转弧度制公式: 1度=π/180≈0.01745弧度, 1弧度=180/π≈57.3度
  
  rows, columns = edged.shape
  #print('rows:',rows,'columns:',columns)

  #创建霍夫空间横轴theta, 范围[-90,90], 取点数 2*(90/theta_res)+1 
  #np.linspace(起始值,终点值,取点数):创建等差数列。
  theta = np.linspace(-90.0, 0.0, int(np.ceil(90.0/theta_res) + 1.0))#*?为什么是-90°~90°?
  #数组中[start:end:step]。这里step=-1表示从右往左取值,len(theta)-2是为了去掉一个多余的0
  theta = np.concatenate((theta, -theta[len(theta)-2::-1]))
  
  #创建霍夫空间纵轴rho, 范围[-图片对角线长度,图片对角线长度],取点数: 2*(图片对角线长度/rho_res)+1
  diagonal = np.sqrt((rows - 1)**2 + (columns - 1)**2) #diagonal对角线
  q = np.ceil(diagonal/rho_res)
  nrho = 2*q + 1 #取点数
  rho = np.linspace(-q*rho_res, q*rho_res, int(nrho))
  
  #创建空的霍夫空间坐标系。大小为rho行theta列
  houghMatrix = np.zeros((len(rho), len(theta)))

  #把图片里属于边缘的像素一个个填入霍夫空间坐标系。
  for rowId in range(rows):                           
      for colId in range(columns):
        #如果是边缘像素,则循环遍历所有可能的θ值,计算对应的ρ,在累加器中找到θ和ρ索引并在该位置递加。                   
        if edged[rowId, colId]>thresholdPixels: 
          #print('rowId,colId:',rowId, colId,'\n edged[rowId, colId]:',edged[rowId, colId])
          #霍夫空间竖轴, 值=rhoVal。
          for thId in range(len(theta)):
            rhoVal = colId*np.cos(theta[thId]*np.pi/180.0) + \
                rowId*np.sin(theta[thId]*np.pi/180)
            #np.nonzero()得到数组array中非零元素的位置。np.abs()绝对值。
            #这里相当于用nonzero()找到令rho=rhoVal为True时ρ的索引
            #这里相当于用了np.argmin(np.abs(rho - rhoVal))。np.argmin():返回最小值在数组中的索引。
            rhoIdx = np.nonzero(np.abs(rho-rhoVal) == np.min(np.abs(rho-rhoVal)))[0] 
            houghMatrix[rhoIdx[0], thId] += 1   #*注:这里不要写反了,坐标系里x、y轴在数组里位置是[y,x](因为是先取行再取列)
  print('houghMatrix:\n',houghMatrix)

  #为了不让线粘太紧,靠得近的线里只留数值最高的一条,其他除掉
  #cluster and filter multiple dots in Houghs plane
  if filterMultiple>0:
      clusterDiameter=filterMultiple # diameter:直径
      #values存放houghMatrix中大于阈值的值。np.transpose():交换轴的位置,不加其他参数时相当于.T()转置。
      values=np.transpose(np.array(np.nonzero(houghMatrix>thresholdVotes)))
      print('values:\n',values)
      filterArray=[]#这几个Array放的都是在values里的索引
      filterArray.append(0)
      totalArray=[]
      for i in range (0, len(values)):
          if i in filterArray[1::]:
              continue #*注:continue，break都是对for起作用而不是if啊啊啊啊
          tempArray=[i]
          for j in range (i+1, len(values)):#遍历位置在i后面的值,如果
              if j in filterArray[1::]:
                  continue
              #遍历当前簇,如果此线和里面其他线有距离小于阈值的,则放进同一簇
              for k in range (0, len(tempArray)):
                  if getLength(values[tempArray[k]],values[j])<clusterDiameter:
                      filterArray.append(j)
                      tempArray.append(j)#放进当前的簇
                      break
          totalArray.append(tempArray)#tempArray存放一簇线,totalArray存放所有tempArray
          #print('totalArray-',i,':\n',totalArray)
      #print('totalArray-ending',totalArray)
      #每一簇都只留一条最大值,其他变成0
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
                       ii=i  #ii,jj保存上一轮的i,j
                       jj=j
                   else:
                       houghMatrix[values[totalArray[i][j]][0],values[totalArray[i][j]][1]]=0
               #print('highest:',highest)
  print('houghMatrix-2:\n',houghMatrix)     
  return (np.where(houghMatrix>thresholdVotes)[0]-q)*rho_res,\
            theta[np.where(houghMatrix>thresholdVotes)[1]]*np.pi/180.0


#画霍斯空间的线
def plotHoughLines(rho,theta,image):
  #极坐标与笛卡尔互相转换: https://blog.csdn.net/weixin_36815313/article/details/109485524
  #极坐标转笛卡尔坐标系公式: x=ρ*cosθ, y=ρ*sinθ
  a = np.cos(theta) # a=cosθ
  b = np.sin(theta) # b=sinθ
  x0 = a*rho
  y0 = b*rho

  #plt.subplots():一纸绘多图。nrows:横轴分成的区域,ncols:纵轴分成的区域
  fig2, ax1 = plt.subplots(ncols=1, nrows=1)
  ax1.imshow(image)
  
 
  #*注:[x1,x2],[y1,y2]的xy别写反了
  for i in range (0, len(rho)): 
    #这里的+1000*(-b[i])和+1000*(a[i])是为了画延长线,其他数值也可以
    ax1.plot( [x0[i] + 1000*(-b[i]), x0[i] - 1000*(-b[i])],
              [y0[i] + 1000*(a[i]), y0[i] - 1000*(a[i])], 
              'xb-',linewidth=3)# plot():参数[fmt] = '[color][marker][line]'。
  
  ax1.set_ylim([image.shape[0],0])
  ax1.set_xlim([0,image.shape[1]])
  
  plt.show()


#计算笛卡尔坐标系中两点的距离, startPoint、secondPoint格式: [x,y] 
def getLength(startPoint,secondPoint):
  v1x=secondPoint[0]-startPoint[0]
  v1y=secondPoint[1]-startPoint[1]
  lenv=np.sqrt(v1x*v1x+v1y*v1y)
  #print('startPoint',startPoint,'secondPoint:',secondPoint,'lenv:',lenv)     
  return lenv
  

#去除array中的重复项,a: list of 1xN arrays,返回值b: array (按行升序排序)
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
  
#重新排列四边形的四个角,使相邻的角跟在一起。reorder:重新排列
#corners:四角坐标,形如[[153, 104], [255, 98], [178, 144], [231, 58]]
#返回array:[[153, 104], [178, 144], [255, 98], [231, 58]]
def reorderPoints(corners):    
    array=[]
    #遍历每个角,分别算它和另外三点距离
    for i in range (0, len(corners)):
        tempArray=[]
        length1=getLength(corners[i][0],corners[i][1])
        length2=getLength(corners[i][0],corners[i][2])
        length3=getLength(corners[i][0],corners[i][3])
        lenArr=np.array([length1,length2,length3])
        tempArray.append(corners[i][0])
        #找到最短距离对应的角中的第一个,放进tempArray
        tempArray.append(corners[i][1+np.where(np.array(lenArr)==np.min(lenArr))[0][0]])
        #为避免有一样长的,把最短那条缩短
        lenArr[np.where(np.array(lenArr)==np.min(lenArr))[0][0]]+=-0.00001 
        #最长、中间边对应的角放进tempArray
        tempArray.append(corners[i][1+np.where(np.array(lenArr)==np.max(lenArr))[0][0]])
        tempArray.append(corners[i][1+np.where(np.array(lenArr)==np.median(lenArr))[0][0]])
        array.append(tempArray)
        print('tempArray:\n',tempArray)
    print('array:\n',array)
    return array

def getAngle(startPoint,secondPoint,thirdPoint, absol=True):
    #Gets angle between vectors (startPoint,secondPoint) and vector
    #(secondPoint,thirdPoint)

    ##Inputs:
    #startPoint - [x,y]
    #secondPoint - [x,y]
    #thirdPoint - [x,y]

    ##Outputs:
    #angle - angle between two vectors


    v1x=secondPoint[0]-startPoint[0]
    v1y=secondPoint[1]-startPoint[1]
    v2x=thirdPoint[0]-startPoint[0]
    v2y=thirdPoint[1]-startPoint[1]

    lenv1=np.sqrt(v1x*v1x+v1y*v1y)
    lenv2=np.sqrt(v2x*v2x+v2y*v2y)

    angle=np.arccos((v1x*v2x+v1y*v2y)/(lenv1*lenv2))

    a=1
    if absol==False:
        a = np.sign((v1x) * (v2y) - (v1y) * (v2x))

    if np.absolute(angle) < 0.02:
        angle=0
    return a*angle


def blurImage(image_gray):
    kernel = np.ones((2,2),np.float32)/4                     #Blurring kernel
    #We will skip first line and first column to keep it more simple, it's zeroed out anyway.
    #now for every pixel we change it with the average of 4 pixels(as the kernel): itself, pixel to left
    #pixel up, and pixel up-left. It drifts some edges one pixel to bottom-down, but it does not matter as
    #long as we use edged picture for the future work
    res=sp.convolve2d(image_gray,kernel,mode='same')

    return np.round(res).astype(np.uint8)
  
  
  
  
  
  