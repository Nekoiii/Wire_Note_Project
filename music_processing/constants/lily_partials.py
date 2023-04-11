#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lilypond文件常用的部分
"""

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

notes_prefix=r'''
\fixed c'{
'''

notes=r'''
c d e f
c' d e f
cis dis eis fis
'''

notes_suffix=r'''
}
'''

# *lily居然可以直接变颜色！！！！
# 但找了半天发现变不了background的color,只能额外画个有颜色的盒子叠在底下。所以没办法直接生成透明背景曲谱了qvq
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





















