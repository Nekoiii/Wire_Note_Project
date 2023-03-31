#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频转midi
"""



'''
n = note.Note("D#3")
n.duration.type = 'half'
n.show()
'''
import os
from music21 import *
from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import which

import subprocess

# 运行which命令查找ffprobe程序位置
process = subprocess.Popen(['which', 'ffprobe'], stdout=subprocess.PIPE)
stdout, _ = process.communicate()
ffprobe_path = stdout.decode().strip()

# 输出ffprobe程序位置
print('xxx',ffprobe_path,'yyy')

ffprobe_path = which('ffprobe')
print('ffprobe_path',ffprobe_path)


file_name = 'audios/zhenbiantonghua-short'
mp3_file= file_name + '.mp3'
wav_file = file_name + '.wav'
midi_file = file_name + '.mid'
xml_file = file_name + '.musicxml'


ffmpeg_path = '/usr/local/bin/ffmpeg'
ffprobe_path = '/usr/local/bin/ffprobe'
audio_file = AudioSegment.from_file(mp3_file, format="mp3",ffmpeg=ffmpeg_path, ffprobe=ffprobe_path)
audio.export(wav_file, format='wav')




output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../midi', 'output_1')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output_midi_file_path = os.path.join(output_dir, file_name+'_output_1'+'.mid')



# 读取wav文件并播放
mf = music21.midi.MidiFile()
mf.open(wav_file+'.mid')
mf.read()
mf.close()

sp = music21.midi.realtime.StreamPlayer(mf.play())
sp.play()





