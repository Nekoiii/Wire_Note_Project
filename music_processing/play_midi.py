#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
播放midi
"""

import pygame

# 初始化 Pygame
pygame.init()

# 设置音频设备
pygame.mixer.init()

# 加载 MIDI 文件
pygame.mixer.music.load('your_file.mid')

# 播放 MIDI 文件
pygame.mixer.music.play()

# 等待音乐播放完毕
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

# 关闭 Pygame
pygame.quit()