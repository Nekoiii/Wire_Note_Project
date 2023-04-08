#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画曲谱
"""
import os
import asyncio
from music21 import *
import matplotlib.pyplot as plt
import cv2
from pdf2image import convert_from_path
import numpy as np
import nest_asyncio
nest_asyncio.apply()



s = stream.Score()
path = os.path.abspath(os.path.join(os.getcwd(), "output_sheets", "test.xml"))
pdf_path=os.path.abspath(os.path.join(os.getcwd(), "output_sheets", "test.pdf"))
png_path_0="output_sheets/test-1.png"
png_path="output_sheets/output.png"

def add_note(note_name): #添加音符
  print('add_note--',note_name)
  global s
  s.append(note.Note(note_name))
  save_note()
  
  
#pdf转png
def pdf_to_png():
    pages = convert_from_path(pdf_path)
    img = np.array(pages[0])
    
    if len(img.shape) == 2:
      img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
    elif img.shape[2] == 3:
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    #img=turn_white_to_transparent(img)
    return img

  
#把图片中像素>threshold的变为透明,深色的地方都转为白色
def turn_white_to_transparent(img,threshold=250):
    #print('turn_white_to_transparent----')
    if len(img.shape) == 2:
      img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
    elif img.shape[2] == 3:
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

      
    #转换为NumPy数组格式的图像数据
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    thresh_rgba = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGBA)
    
    mask = thresh_rgba[:, :, 0] > threshold
    img[np.where(mask)] = [0, 0, 0, 0]  #白色的地方转为透明
    img[np.where(~mask)] = [255, 255, 255, 255]  #其余都设为白色

    return img
    
  
def make_opaque_to_white(png):
  alpha = png[:, :, 3]
  alpha[alpha != 0] = 255
  png[png[:, :, 3] != 0] = [255, 255, 255, 255] 
  return png  
  
  
 
def save_note():
    '''
    # 先存为pdf，再转为png的情况：
    s.write("musicxml.pdf", path)
    png=pdf_to_png()
    png=turn_white_to_transparent(png)
    cv2.imwrite(png_path, png)
    '''
    '''报错 music21.base.Music21ObjectException: cannot support showing in this format yet: ttt.png
    并不是因为不能转png,而是"musicxml.png"这个不是文件名,而是表示将score对象s写入到
    MusicXML格式的文件中,并生成一个同名的png格式的图像文件啊啊啊啊！！！！！！！
    是可以直接生成png的啊啊啊啊啊！！！！！！！
    '''
    '''
    但！是！我怀疑music21生成的png有问题！！！！其他png都能正常深色转白色、保留原本透明度，
    就只有music21生成的png会连背景透明部分也变白啊啊啊啊！！！！
    用cv2.imread(png_path)不带cv2.IMREAD_UNCHANGED参数读取，再cv2.imshow()时
    其他图透明处都显示为白色，就它是黑的！但透明通道print出来看上去和其他图又是一样的不知道
    到底怎么回事！！！！
    '''
    png=s.write("musicxml.png", path)
    png=cv2.imread(png_path_0, cv2.IMREAD_UNCHANGED)
    
    png=make_opaque_to_white(png)
    cv2.imwrite(png_path, png)
    






