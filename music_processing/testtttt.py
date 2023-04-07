#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 22:27:54 2023

@author: nekosa
"""

import asyncio
import nest_asyncio
nest_asyncio.apply()

async def async_func():
    # 异步函数代码
    print('This is an async function')

async def keyboard_event():
    while True:
        key = input()
        if key == 'a':
            await async_func()

async def main():
    # 启动键盘事件处理协程
    asyncio.create_task(keyboard_event())

    # 程序其他逻辑代码
    print('Program started')

if __name__ == "__main__":
    asyncio.run(main())