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

# 初始化Pygame和PyAudio
pygame.init()
p = pyaudio.PyAudio()


#按键映射表
keys_map = {
    pygame.K_t: 'C4',
    pygame.K_y: 'D4',
    pygame.K_u: 'E4',
    pygame.K_i: 'F4',
    pygame.K_o: 'G4',
    pygame.K_p: 'A4',
    pygame.K_LEFTBRACKET: 'B4',
    pygame.K_RIGHTBRACKET: 'C5',
    pygame.K_6: 'C4#',
    pygame.K_7: 'D4#',
    pygame.K_9: 'F4#',
    pygame.K_0: 'G4#',
    pygame.K_MINUS: 'A4#'
}
'''
#按键映射表
keys_map = {
    't': 'C4',
    'y': 'D4',
    'u': 'E4',
    'i': 'F4',
    'o': 'G4',
    'p': 'A4',
    '[': 'B4',
    ']': 'C5',
    '6': 'C4#',
    '7': 'D4#',
    '9': 'F4#',
    '0': 'G4#',
    '-': 'A4#'
}
# 加载钢琴按键音频
basic_path = 'audios/piano_keys/'
key_sounds = {}
for key, note in keys_map.items():
    key_sound = wave.open(basic_path + note + '.wav', 'rb')
    key_sounds[key] = {
        'sound': key_sound,
        'stream': p.open(format=p.get_format_from_width(key_sound.getsampwidth()),
                         channels=key_sound.getnchannels(),
                         rate=key_sound.getframerate(),
                         output=True)
    }
'''

#设置窗口
pygame.display.set_caption("Piano")
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((800,600))
pygame.display.update() 


def play(path,key):
    CHUNK = 1024    #CHUNK指定每次从音频流中读取和处理的音频样本数。它是一个缓冲区的大小，用于控制每次处理的数据量。一般可用 1024 或 2048 。值太小，播放音频将会更加实时，但可能会导致音频出现卡顿或者声音质量差的问题。值太大，音频播放将更加平滑，但会增加延迟，可能会导致应用程序的响应性下降。
    wf = wave.open(path, 'rb')
    data = wf.readframes(CHUNK)
    global p # 创建播放器
    # 获得语音文件的各个参数
    FORMAT = p.get_format_from_width(wf.getsampwidth())
    CHANNELS = wf.getnchannels()
    RATE = wf.getframerate()
    
    #print(keyDict[key],end=' ')
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
  
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
    if event.type == pygame.KEYDOWN:
      key = event.key
      print('KEYDOWN--')
      if(key == pygame.K_ESCAPE):    #esc键退出
        pygame.quit()
      elif key in keys_map.keys():
        basic_path = 'audios/piano_keys/'
        fileName = basic_path+str(keys_map[key])+".wav"
        if os.path.exists(fileName):
          print('play---',fileName)
          threading.Thread(target=play, args=(fileName,key)).start()
    elif event.type == pygame.KEYUP:
      print('KEYUP--')
  
'''
playing_keys = []
# 循环读取事件
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:# 退出程序
            for key_sound in key_sounds.values():
                key_sound['stream'].stop_stream()
                key_sound['stream'].close()
                key_sound['sound'].close()
            p.terminate()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:# 按下键盘
            key = pygame.key.name(event.key)
            if(key == pygame.K_ESCAPE):#esc键退出
                pygame.quit()
            if key in keys_map and key not in playing_keys:
                # 播放音频
                key_sound = key_sounds[key]
                key_sound['sound'].rewind()
                key_sound['stream'].write(key_sound['sound'].readframes(44100))
                playing_keys.append(key)
        elif event.type == pygame.KEYUP:# 松开键盘
            key = pygame.key.name(event.key)
            if key in playing_keys:
                # 停止音频
                key_sound = key_sounds[key]
                key_sound['stream'].stop_stream()
                playing_keys.remove(key)

    # 绘制文本
    text = ' '.join([keys_map[key] for key in playing_keys])
    text_surface = font.render(text, True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(text_surface, (50, 50))
    pygame.display.flip()

    # 控制帧率
    clock = pygame.time.Clock()
    clock.tick(30)
'''

