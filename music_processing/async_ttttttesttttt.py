#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 22:27:54 2023

@author: nekosa
"""

import pygame
import asyncio
import nest_asyncio
nest_asyncio.apply()

pygame.init()
pygame.display.set_caption("Piano")
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((800,600))
pygame.display.update() 

async def async_func():
    await asyncio.sleep(1)
    print('sleep---')
    # 异步函数代码
    print('This is an async function')

async def keyboard_event():
    if_quited=False
    while not if_quited:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:  #关闭窗口
          if_quited=True
          pygame.quit()
        if event.type == pygame.KEYDOWN:
          key = event.key
          if(key == pygame.K_ESCAPE):    #esc键退出
            if_quited=True
            pygame.quit()

          await async_func()
          print('KEYDOWN--',event.key)
          

  
async def main():
    # 启动键盘事件处理协程
    asyncio.create_task(keyboard_event())


if __name__ == "__main__":
    asyncio.run(main())
    
    
    
    
    
    
    
    
    
    