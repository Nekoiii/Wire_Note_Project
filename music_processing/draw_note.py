#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画曲谱
"""
import os
import asyncio
import subprocess
from music21 import *
import matplotlib.pyplot as plt
import cv2
from pdf2image import convert_from_path
import numpy as np
import nest_asyncio
nest_asyncio.apply()
os.environ["PATH"] += os.pathsep + '/usr/local/opt/lilypond/bin'
os.environ["lilypondPath"] = "/usr/local/opt/lilypond/bin"
os.environ['LILYPOND'] = '/usr/local/opt/lilypond/bin'
mscore_path = "/Applications/MuseScore 4.app/Contents/MacOS/mscore"

s = stream.Score()
#s.append(note.Note("C"))
xml_path = os.path.abspath(os.path.join(os.getcwd(), "output_sheets", "output.xml"))
pdf_path=os.path.abspath(os.path.join(os.getcwd(), "output_sheets", "output.pdf"))
#musicxml_path="output_sheets/test.musicxml"
musicxml_path=os.path.abspath(os.path.join(os.getcwd(), "output_sheets", "output.musicxml"))
#png_path_0="output_sheets/test-1.png"
png_path_0="output_sheets/output.png"
#png_path="output_sheets/output.png"
png_path="output_sheets/output-1.png"
#png_path = os.path.abspath(os.path.join(os.getcwd(), "output_sheets", "output.png"))

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
  
    #【】直接用music生成png的方法：（这样生成的png宽度不定，会导致随着音符增加而变长）
    png=s.write("musicxml.png", xml_path)
    png=cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
    
    png=make_opaque_to_white(png)
    cv2.imwrite(png_path, png)

  
    #【】
    '''
    png=s.write("musicxml", musicxml_path)
    cmd = [
        mscore_path,
        musicxml_path,
        '-o', png_path_0,
        '-T', '0',
        '-r', '300',
    ]    
    subprocess.run(cmd, check=True)
    try:
      output = subprocess.check_output(["ls", "-l"])
      print(output)
    except subprocess.CalledProcessError as e:
        print("Command '{}' returned non-zero exit status {}".format(e.cmd, e.returncode))

    png=cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
    
    png=turn_white_to_transparent(png)
    cv2.imwrite(png_path, png)
    '''
  
    #【】先存为pdf，再转为png的方法：
    '''
    s.write("musicxml.pdf", xml_path)
    png=pdf_to_png()
    png=turn_white_to_transparent(png)
    cv2.imwrite(png_path, png)
    '''
    '''报错 music21.base.Music21ObjectException: cannot support showing in this format yet: ttt.png
    并不是因为不能转png,而是"musicxml.png"这个不是文件名,而是表示将score对象s写入到
    MusicXML格式的文件中,并生成一个同名的png格式的图像文件啊啊啊啊！！！！！！！
    是可以直接生成png的啊啊啊啊啊！！！！！！！
    而且一定要"musicxml.png"而不能单独生成"png"！！！
    '''
    '''
    但！是！我怀疑music21生成的png有问题！！！！其他png都能正常深色转白色、保留原本透明度，
    就只有music21生成的png会连背景透明部分也变白啊啊啊啊！！！！
    用cv2.imread(png_path)不带cv2.IMREAD_UNCHANGED参数读取，再cv2.imshow()时
    其他图透明处都显示为白色，就它是黑的！但透明通道print出来看上去和其他图又是一样的不知道
    到底怎么回事！！！！
    '''


    
    #【】用lilypond隐藏谱线
    #*problem:也没能成功
    '''
    png=s.write("musicxml", musicxml_path)
    
    # 从 MusicXML 文件中读取乐谱
    score = converter.parse(musicxml_path)
    
    # 循环遍历所有小节并隐藏谱线
    for part in score.parts:
        for measure in part.getElementsByClass('Measure'):
            for staff in measure.getElementsByClass('Staff'):
                staff.showLines = False
                staff.systemStaffLines = False
    
    # musicxml转ly
    lilypond_path = 'output_sheets/output.ly'  
    subprocess.run(['musicxml2ly', musicxml_path, '-o', lilypond_path])
    # ly转pdf *problem报错
    subprocess.run(['lilypond', '-fpdf', '-o', 'output_sheets/output.ly', lilypond_path])
    '''
    
    
    #【】用mscore生成png的方法：（这样能设置MuseScore中的参数。https://musescore.org/en/handbook/3/command-line-options）
    #*注意参数里大小写！！！！
    #*problem:但没有用，并没能隐藏谱线    
    '''
    # 使用 musescore 命令将 MusicXML 转换为 PNG 图片，并设置参数隐藏线条
    cmd = [
        mscore_path,
        musicxml_path,
        '-o', png_path,
        '-T', '0',
        '-r', '300',
        '-S','staff-lines'
    ]
    subprocess.run(cmd, check=True)
    try:
      output = subprocess.check_output(["ls", "-l"])
      print(output)
    except subprocess.CalledProcessError as e:
        print("Command '{}' returned non-zero exit status {}".format(e.cmd, e.returncode))
    
    # 删除 MusicXML 文件
    #os.remove(musicxml_path)
    '''
    
   
    
    






