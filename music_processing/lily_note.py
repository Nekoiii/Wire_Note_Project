#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建lipypond文件
#lilypond参考文档:https://lilypond.org/doc/v2.21/Documentation/learning/absolute-note-names.ja.html
一张谱的例子: https://lilypond.org/doc/v2.25/Documentation/snippets/editorial-annotations_003a-_30b0_30ea_30c3_30c9_7dda_003a-_30ea_30ba_30e0_306e_5f37_8abf_3068_97f3_7b26_306e_540c_671f
https://lilypond.org/doc/v2.21/Documentation/notation/visibility-of-objects.ja.html
#站内搜索:https://www.google.com/search?q=site%3Alilypond.org+%5Crelative&sxsrf=APwXEdcdQE7HPa2MyEzZy_3G9waN-y3hEw%3A1681026704587&ei=kG4yZJ6vI8ulhwPcoobwCw&ved=0ahUKEwiet9a8qJz-AhXL0mEKHVyRAb4Q4dUDCA8&uact=5&oq=site%3Alilypond.org+%5Crelative&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQA0oECEEYAVDxAViWGWD4G2gCcAB4AIABZYgBuwGSAQMxLjGYAQCgAQKgAQHAAQE&sclient=gws-wiz-serp

参考表:https://lilypond.org/doc/v2.24/Documentation/notation/cheat-sheet.ja.html
部件名字:https://lilypond.org/doc/v2.22/Documentation/learning/objects-and-interfaces.ja.html


ly中注释:%

r'''
'''
"""
import os
import subprocess

current_directory = os.getcwd()
print(current_directory)

os.environ["PATH"] += os.pathsep + '/usr/local/opt/lilypond/bin'
os.environ["PATH"] += os.pathsep + '/usr/local/opt/gs/bin'

#r''（Raw String）表示原始字符串，即字符串中的所有特殊字符，如\n、\t等等，都会被原封不动地输出，而不会被解析为其特殊含义

version=r'''
\version "2.24.1"
'''

#*problem背景颜色设置失败了
paper_setting=r'''
\paper {
  % 设置底色为grey
  bgcolor = #grey
}
'''
beginning=r'''
\score {
  \new Staff {
'''



notes=r'''
\fixed c'{
c d e f
c' d e f
cis dis eis fis
}
'''

# *lily居然可以直接变颜色！！！！
settings = r'''
\layout {
\hide Staff.StaffSymbol 
%\override NoteHead.color = #white
%\override Staff.Clef.color = #white
%Staff.BarLine=#white
}
'''



closing_brace=r'''
}
'''



def creat_lily(notes,file_name):
  file_content=version+paper_setting+beginning+notes+closing_brace+settings+closing_brace
  #print('file_content',file_content)
  with open('output_sheets/lily_output.ly', 'w') as f:
      f.write(file_content)
  subprocess.run(['lilypond', '-fpdf', 'lily_output.ly'], cwd='output_sheets')
  subprocess.run(['lilypond', '--png', 'lily_output.ly'], cwd='output_sheets')









