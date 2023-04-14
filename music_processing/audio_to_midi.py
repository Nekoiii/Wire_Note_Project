#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频转midi  *problem：失败了！music21的库不支持直接识别wav、mp3转midi！
                    只有网页上才能识别-转换
"""

import os
from music21 import *

from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import which
import subprocess

file_name = 'audios/zhenbiantonghua-short'
mp3_file= file_name + '.mp3'
wav_file = file_name + '.wav'
midi_file = file_name + '.mid'
xml_file = file_name + '.musicxml'

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../midi', 'output_1')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output_midi_file_path = os.path.join(output_dir, file_name+'_output_1'+'.mid')

# 转换音频文件为MIDI文件
converter.parse(wav_file).write('midi', fp=midi_file)

# 打印转换后MIDI文件的音符和音高信息
midi_stream = converter.parse(midi_file)
for note in midi_stream.flat.notes:
    print(note.nameWithOctave, note.offset)


def mp3_to_wav():
  '''# 运行which命令查找ffprobe程序位置
  process = subprocess.Popen(['which', 'ffprobe'], stdout=subprocess.PIPE)
  stdout, _ = process.communicate()
  ffprobe_path = stdout.decode().strip()
  # 输出ffprobe程序位置
  print('xxx',ffprobe_path,'yyy')'''
  #audio_file = AudioSegment.from_file(mp3_file, format="mp3",ffmpeg=ffmpeg_path, ffprobe=ffprobe_path)

  audio_file = AudioSegment.from_file('zhenbiantonghua-short.mp3', format="mp3")
  audio_file.export('zhenbiantonghua-short.wav', format='wav')
  play(AudioSegment.from_file("zhenbiantonghua-short.wav", format="wav"))


mp3_to_wav()






