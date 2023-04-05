#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画曲谱
"""
import os
from music21 import *
import matplotlib.pyplot as plt
import fitz

s = stream.Score()

'''
# 添加音符
n1 = note.Note("C4")
n2 = note.Note("E4")
s.append([n1, n2])
'''
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
    '''
    # 读取PDF文件
    pdf = plt.imread(pdf_path)
    # 显示PDF文件
    plt.imshow(pdf)
    plt.axis('off')
    plt.show()
    '''
    
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







