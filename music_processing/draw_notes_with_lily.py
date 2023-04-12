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

r'''
'''
"""
import os
import cv2
import asyncio
import subprocess
import constants.lily_partials as lily_partials
import process_note_img


current_directory = os.getcwd()
print(current_directory)

os.environ["PATH"] += os.pathsep + '/usr/local/opt/lilypond/bin'
os.environ["PATH"] += os.pathsep + '/usr/local/opt/gs/bin'


ly_path='output_sheets/lily_output.ly'

    
async def create_lily(note_list,png_path):
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
  #print('file_content',file_content)
  with open('output_sheets/lily_output.ly', 'w') as f:
      f.write(file_content)
  #subprocess.run(['lilypond', '-fpdf', 'lily_output.ly'], cwd='output_sheets')
  png_name=png_path.split('.')[0]
  print('asssss-0')
  try:
    subprocess.run(['lilypond', '--png', f'--output={png_name}','output_sheets/lily_output.ly'])
  except subprocess.CalledProcessError as e:
    print("Failed to run lilypond command:", e)
  
  print('asssss-1')
  png=process_note_img.turn_white_to_transparent(png_path)
  print('asssss-2')
  if png is not None:
    cv2.imwrite(png_path, png)







