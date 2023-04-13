#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
键盘弹琴入口文件
"""
import os
import sys
import wave
import pygame
import asyncio
import pyaudio
import threading
from constants.keys_map import keys_map
import draw_notes_with_music21
import draw_notes_with_lily

import nest_asyncio
nest_asyncio.apply()
'''***注: 
Sypder中用python异步要先pip install nest_asyncio，然后
import nest_asyncio
nest_asyncio.apply()
才能用, 不然会报错RuntimeError: This event loop is already running！！！！
'''

png_path="output_sheets/output-1.png"  #最终显示的png


lily_notes=[] #写入ly文件的音符们
background_color=(50, 0, 0)


# 初始化Pygame和PyAudio
pygame.init()
p = pyaudio.PyAudio()

#设置窗口
pygame.display.set_caption("Piano")
font = pygame.font.Font(None, 36)
screen_w=800;
screen_h=600;
screen = pygame.display.set_mode((screen_w,screen_h))
pygame.display.update() 
x0,y0=50,50; #绘制时的初始坐标
scroll_position = 0  # 当前窗口应该显示图片的位置
max_y=screen_h   # 完整画面的高度
scroll_surface = pygame.Surface((screen_w, max_y))# 在另一个更大的 Surface 上绘制, 以实现滚动效果

#播放音频
def play_audio(path,key):
    CHUNK = 1024    #CHUNK指定每次从音频流中读取和处理的音频样本数。它是一个缓冲区的大小，用于控制每次处理的数据量。一般可用 1024 或 2048 。值太小，播放音频将会更加实时，但可能会导致音频出现卡顿或者声音质量差的问题。值太大，音频播放将更加平滑，但会增加延迟，可能会导致应用程序的响应性下降。
    wf = wave.open(path, 'rb')
    data = wf.readframes(CHUNK)
    p = pyaudio.PyAudio()
    
    FORMAT = p.get_format_from_width(wf.getsampwidth())# 获得语音文件的各个参数
    CHANNELS = wf.getnchannels()
    RATE = wf.getframerate()
    
    sys.stdout.flush() #强制刷新标准输出流。没有这句的话可能会导致这些输出被延迟到之后再输出，或者干脆不输出
    
    stream = p.open(format=FORMAT,  #音频样本的格式, 如8位整数、16位整数或32位浮点数等
                    channels=CHANNELS,  #音频流的通道数,如单声道或立体声
                    rate=RATE,  #音频流的采样率, 即每秒采集的样本数
                    frames_per_buffer=CHUNK, #音频流的缓冲区大小, 指定每次读取和处理的音频样本数
                    output=True)    #True输出, False输入
    while data:
      stream.write(data)  
      data = wf.readframes(CHUNK)  #从音频流中读取下一块数据
    
    
    
#用 music21 生成五线谱
def add_note_music21_and_reload(note_name):
    draw_notes_with_music21.add_note(note_name)
    reload_img()
    redraw_surface(lily_notes)

#用 lilypond 生成五线谱
def add_note_lily_and_reload(lily_notes):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(draw_notes_with_lily.create_lily(loop,lily_notes,png_path)))
    reload_img()
    redraw_surface(lily_notes)
    loop.close()
 
    
    
def reload_img():  #重新读取图片
  try:
    image = pygame.image.load(png_path)
  except pygame.error as e:
    print(f"Unable to load image: {png_path}. Error: {e}")
    return None, None, None

  scaled_w = 0.9 * screen_w   #缩放图片
  scaled_h = image.get_height() * scaled_w / image.get_width()  
  return(image,scaled_w,scaled_h)


def redraw_scroll():  #上下滚动后的重新绘制
  screen.fill(background_color)

  scroll_rect = pygame.Rect(0, scroll_position, screen_w, screen_h)
  screen.blit(scroll_surface.subsurface(scroll_rect), (0, 0))
  pygame.display.update()


def redraw_surface(lily_notes):  #改变了音符后的重新绘制
  global scroll_surface,screen,max_y
  
  screen.fill(background_color)    #清空窗口并绘制背景色(不然图片移动时不会恢复底色)
  scroll_surface.fill(background_color)

  image,scaled_w,scaled_h= reload_img()  #重新读取图片
  if image is None:
    return

  #在屏幕上显示字符
  items_per_line = 10   # 设置每行显示的元素个数
  y=y0
  # 将列表分成每10个元素一组, 再把组内每项用' - '分隔
  #*注: pygame默认字体无法识别换行符\n,所以只能一行行计算坐标显示！
  grouped_items = [lily_notes[i:i+items_per_line] for i in range(0, len(lily_notes), items_per_line)]
  grouped_items = ['  -  '.join(group) for group in grouped_items]
  text_surfaces = []  #字符的显示surface
  for item in grouped_items:
    text_surface=font.render(item, True, (255, 255, 255))
    text_surfaces.append(text_surface)
  for text_surface in text_surfaces:
    scroll_surface.blit(text_surface, (x0, y))
    screen.blit(scroll_surface, (0,0)) #*注: 这里一定要先画一次到screen上！！！！不然后面画图片时再次scroll_surface.blit会覆盖掉前面的！！！！
    y+=30
  
  if y+scaled_h>screen_h:
    max_y=y+scaled_h  #如果超出屏幕了,更新最大高度。否则设为屏幕高度
  else:
    max_y=screen_h
  
  new_scroll_surface=pygame.Surface((screen_w, max_y)) #scroll_surface改大小
  new_scroll_surface.blit(scroll_surface, (0, 0))
  scroll_surface = new_scroll_surface
  

  #在屏幕上绘制图片
  if len(lily_notes)>0:
    scroll_surface.blit(pygame.transform.scale
                (image, (scaled_w, scaled_h)), 
                (0.5*(screen_w-scaled_w), y))
  # 根据 scroll_position 将 scroll_surface 上的一部分绘制到屏幕上
  scroll_rect = pygame.Rect(0, scroll_position, screen_w, screen_h)
  screen.blit(scroll_surface.subsurface(scroll_rect), (0, 0))
  
  pygame.display.update()


#监听键盘事件
def keyboard_event():
  global scroll_position,lily_notes
  
  scroll_step=100  #上下滚动窗口时每次滚多少 
  
  if_quited=False  #判断是否退出。不然pygame.quit()后再执行pygame.event.get()会报错error: video system not initialized
  while not if_quited:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:  #关闭窗口
        if_quited=True
        pygame.quit()
        
      if event.type == pygame.KEYDOWN: #按下键盘
        #print('KEYDOWN--',event.key)
        key = event.key
        
        if(key == pygame.K_ESCAPE):    #esc键退出
          if_quited=True
          pygame.quit()
        #*problem: 下滚窗口时文字显示会不全,不知道哪里出问题了
        elif key ==pygame.K_UP:    #上下滚动窗口
            reload_img()
            scroll_position -= scroll_step
            if scroll_position < 0:
                scroll_position = 0
            redraw_scroll()
        elif event.key ==pygame.K_DOWN:
            image,scaled_w,scaled_h=reload_img()
            scroll_position += scroll_step
            if scroll_position > (max_y - screen_h):
                scroll_position = max_y - screen_h
            redraw_scroll()
        elif event.key ==pygame.K_LEFT:  #←键删除一个音
          if lily_notes:   #可以直接用if来判断列表是否为空,不用加len()
            lily_notes.pop()
            threading.Thread(target=add_note_lily_and_reload, args=(lily_notes,)).start()
            redraw_surface(lily_notes)
          
        elif key in keys_map.keys():       #按下琴键 
          note_name=keys_map[key]['note_name']
          lily_notes.append(keys_map[key]['lily_note'])
          
          #添加音符,并重新生成png图片
          #*注: threading.Thread只传一个参数时, args=(note_name,)中要加逗号把它变成一个元组,不然就会报错 xxx() takes 1 positional argument but 2 were given
          #【用music21生成曲谱】
          #threading.Thread(target=add_note_music21_and_reload, args=(note_name,)).start()
          #【用lilypond生成曲谱】
          threading.Thread(target=add_note_lily_and_reload, args=(lily_notes,)).start()
          
          
          #播放音频
          basic_path = 'audios/piano_keys/'
          wav_path = basic_path+str(note_name)+".wav"
          if os.path.exists(wav_path):            
            threading.Thread(target=play_audio, args=(wav_path, key)).start()
            
          #绘制
          redraw_surface(lily_notes)
  
        
          
      elif event.type == pygame.KEYUP: #放开键盘
        break
        #print('KEYUP--')


if __name__ == "__main__":
    keyboard_event()











