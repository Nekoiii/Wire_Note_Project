#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import os
import sys
import wave
import pygame
import pyaudio
import threading
from keys_map import keys_map

png_path="output_sheets/output.png"

# 初始化Pygame和PyAudio
pygame.init()
p = pyaudio.PyAudio()


#设置窗口
pygame.display.set_caption("Piano")
font = pygame.font.Font(None, 36)
screen_w=800;
screen_h=600;
screen = pygame.display.set_mode((800,600))
pygame.display.update() 
scroll_position = 0  # 当前窗口应该显示图片的位置
max_y=screen_h
x,y=50,50; #绘制时的初始坐标


def play_audio(path,key):
    CHUNK = 1024    #CHUNK指定每次从音频流中读取和处理的音频样本数。它是一个缓冲区的大小，用于控制每次处理的数据量。一般可用 1024 或 2048 。值太小，播放音频将会更加实时，但可能会导致音频出现卡顿或者声音质量差的问题。值太大，音频播放将更加平滑，但会增加延迟，可能会导致应用程序的响应性下降。
    wf = wave.open(path, 'rb')
    data = wf.readframes(CHUNK)
    global p # 创建播放器
    # 获得语音文件的各个参数
    FORMAT = p.get_format_from_width(wf.getsampwidth())
    CHANNELS = wf.getnchannels()
    RATE = wf.getframerate()
    
    print(keys_map[key],end=' ')
    sys.stdout.flush() 
    # 打开音频流。output=True表示音频输出
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    frames_per_buffer=CHUNK,
                    output=True)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
  
  
def reload_img():
  global max_y
  image = pygame.image.load(png_path)
  scaled_w=0.9*screen_w;
  img_w=image.get_width();
  img_h=image.get_height()
  scale_factor=scaled_w/img_w #缩放图片
  scaled_h=img_h * scale_factor
  max_y=y+scaled_h  
  return(image,scaled_w,scaled_h)
  
def re_draw():
  global x,y
  # 清空窗口并绘制背景色(不然图片移动时不会恢复底色)
  screen.fill((0, 0, 0))

  image,scaled_w,scaled_h=reload_img()
  # 在另一个更大的 Surface 上绘制, 以实现滚动效果
  scroll_surface = pygame.Surface((screen_w, max_y))

  #输出字
  items_per_line = 10   # 设置每行显示的元素个数
  # 将列表分成每10个元素一组，组内用逗号分隔pygame
  #*注: pygame默认字体无法识别换行符\n,所以只能一行行计算坐标显示！
  grouped_items = [text_list[i:i+items_per_line] for i in range(0, len(text_list), items_per_line)]
  grouped_items = [', '.join(group) for group in grouped_items]
  text_surfaces = []
  for item in grouped_items:
    text_surface=font.render(item, True, (255, 255, 255))
    text_surfaces.append(text_surface)
  for text_surface in text_surfaces:
    scroll_surface.blit(text_surface, (x, y))
    screen.blit(scroll_surface, (0,0))
    y+=30
  
  #绘制图片
  if len(text_list)>0:
    scroll_surface.blit(pygame.transform.scale
                (image, (scaled_w, scaled_h)), 
                (0.5*(screen_w-scaled_w), y))
    
  # 根据 scroll_position 将 Surface 上的一部分绘制到屏幕上
  scroll_rect = pygame.Rect(0, scroll_position, screen_w, screen_h)
  screen.blit(scroll_surface.subsurface(scroll_rect), (0, 0))
  
  pygame.display.update()


text_list=[] #显示的文字
if_quited=False  #判断是否退出。不然pygame.quit()后再执行pygame.event.get()会报错error: video system not initialized
while not if_quited:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:  #关闭窗口
      if_quited=True
      pygame.quit()
    if event.type == pygame.KEYDOWN: #按下键盘
      key = event.key
      print('KEYDOWN--')
      
      if key ==pygame.K_UP:    #上下滚动窗口
          reload_img()
          scroll_position -= 100
          if scroll_position < 0:
              scroll_position = 0
          #print('---K_UP--scroll_position',scroll_position)
          re_draw()
      elif event.key ==pygame.K_DOWN:
          image,scaled_w,scaled_h=reload_img()
          scroll_position += 100
          print('---K_DOWN--scroll_position111',scroll_position,max_y - screen_h)
          if scroll_position > (max_y - screen_h):
              scroll_position = max_y - screen_h
          print('---K_DOWN--scroll_position222',scroll_position,max_y - screen_h)
          re_draw()
      elif(key == pygame.K_ESCAPE):    #esc键退出
        if_quited=True
        pygame.quit()
        
        
      elif key in keys_map.keys():       #按下琴键 
        #播放音频
        basic_path = 'audios/piano_keys/'
        fileName = basic_path+str(keys_map[key])+".wav"
        if os.path.exists(fileName):
          threading.Thread(target=play_audio, args=(fileName,key)).start()
          
        #绘制
        text_list.append(keys_map[key])
        re_draw()

      
        
    elif event.type == pygame.KEYUP:
      print('KEYUP--')











