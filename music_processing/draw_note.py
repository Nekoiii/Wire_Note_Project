#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画曲谱
"""
import os
from music21 import *
import matplotlib.pyplot as plt
import fitz
import cv2
from pdf2image import convert_from_path
import numpy as np

s = stream.Score()
path = os.path.abspath(os.path.join(os.getcwd(), "output_sheets", "test.xml"))
pdf_path=os.path.abspath(os.path.join(os.getcwd(), "output_sheets", "test.pdf"))
png_path="output_sheets/output.png"

def add_note(note_name): #添加音符
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
      
    turn_white_to_transparent(img,150)

  
#把图片中像素>threshold的变为透明
def turn_white_to_transparent(img,threshold=250):
    #转换为NumPy数组格式的图像数据
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    thresh_rgba = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGBA)
    
    mask = thresh_rgba[:, :, 0] > threshold
    img[mask] = [0, 0, 0, 0]
    cv2.imwrite(png_path, img)
    
  
def save_note():
    # 保存为MusicXML文件
    s.write("musicxml.pdf", path)
    
    pix=pdf_to_png()
    #pix.save(png_path)
    
    s.show('text')


'''
while True:
    key = input("Press 'c' to add a C4 note, 'e' to add an E4 note, or 'q' to quit: ")
    if key == 'q':
        break
    elif key == 'c':
        s.append(note.Note("C4"))
    elif key == 'e':
        s.append(note.Note("E4"))
        
    # 保存为MusicXML文件
    path = os.path.abspath(os.path.join(os.getcwd(), "output_sheets", "test.xml"))
    s.write("musicxml.pdf", path)
    pdf_path=os.path.abspath(os.path.join(os.getcwd(), "output_sheets", "test.pdf"))
    # 打开PDF文件
    #subprocess.call(('open', pdf_path))

    #pdf转png
    pdf = fitz.open(pdf_path)
    page = pdf.load_page(0)
    png_path="output_sheets/output.png"
    #pix = page.get_pixmap()
    dpi = 350  # 设置输出的分辨率(不设置的话会超级模糊!)
    scale = dpi / 72  # 计算缩放比例
    mat = fitz.Matrix(scale, scale)  # 创建矩阵对象
    pix = page.get_pixmap(matrix=mat)  # 使用矩阵对象进行缩放
    pix.save(png_path)
    
    
    png = plt.imread(png_path)
    plt.imshow(png)
    plt.axis('off')
    plt.show()
    
    s.show('text')
'''






