#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
利用 lipypond 画音符

#lilypond参考文档:https://lilypond.org/doc/v2.21/Documentation/learning/absolute-note-names.ja.html
一张谱的例子: https://lilypond.org/doc/v2.25/Documentation/snippets/editorial-annotations_003a-_30b0_30ea_30c3_30c9_7dda_003a-_30ea_30ba_30e0_306e_5f37_8abf_3068_97f3_7b26_306e_540c_671f
https://lilypond.org/doc/v2.21/Documentation/notation/visibility-of-objects.ja.html
#站内搜索:https://www.google.com/search?q=site%3Alilypond.org+%5Crelative&sxsrf=APwXEdcdQE7HPa2MyEzZy_3G9waN-y3hEw%3A1681026704587&ei=kG4yZJ6vI8ulhwPcoobwCw&ved=0ahUKEwiet9a8qJz-AhXL0mEKHVyRAb4Q4dUDCA8&uact=5&oq=site%3Alilypond.org+%5Crelative&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQA0oECEEYAVDxAViWGWD4G2gCcAB4AIABZYgBuwGSAQMxLjGYAQCgAQKgAQHAAQE&sclient=gws-wiz-serp

参考表:https://lilypond.org/doc/v2.24/Documentation/notation/cheat-sheet.ja.html
颜色表:
部件名字:https://lilypond.org/doc/v2.22/Documentation/learning/objects-and-interfaces.ja.html

ly中注释:%

"""
'''
lilypond要放进环境变量，或者在代码中指定
os.environ["PATH"] += os.pathsep + '/usr/local/opt/lilypond/bin'
os.environ["PATH"] += os.pathsep + '/usr/local/opt/gs/bin'
如要用lilypond转换文件的功能,要把export PATH="/usr/local/opt/gs/bin:$PATH"也加进环境变量
'''

import cv2
import asyncio
import subprocess
import constants.lily_partials as lily_partials
import process_note_img


ly_path='output_sheets/lily_output.ly'
origin_png_path='output_sheets/origin.png'  #转换成白色前的原曲谱
origin_png_name=origin_png_path.split('.')[0]

    
async def run_cmd(loop,cmd):  #执行命令栏命令
  try:
    subprocess.run(cmd, check=True)
  except subprocess.CalledProcessError as e:
    print("Failed to run command:", e)

    
async def create_lily(loop,note_list,png_path):
  note_string = ' '.join(note_list)
  file_content=(
                lily_partials.version
                +lily_partials.beginning
                +lily_partials.notes_prefix
                +note_string
                +lily_partials.notes_suffix
                +lily_partials.closing_brace
                +lily_partials.settings
                +lily_partials.closing_brace
                )
  with open('output_sheets/lily_output.ly', 'w') as f: #创建ly文件
      f.write(file_content)
      
  cmd=['lilypond', '--png', f'--output={origin_png_name}','output_sheets/lily_output.ly']
  await run_cmd(loop,cmd)

  png=process_note_img.turn_white_to_transparent(origin_png_path)
  if png is not None:
    cv2.imwrite(png_path, png)







