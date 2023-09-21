import os
import sys
import subprocess
import re
import cv2


current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
parent_dir = os.path.dirname(current_dir)
print(parent_dir)
sys.path.append(os.path.join(parent_dir, 'music_processing'))
print('sys.path--  ',sys.path)

import constants.lily_partials as lily_partials
from process_note_img import turn_white_to_transparent

base_path = '/Users/a/code/Wire_Note_Project/try_audio_to_sheet'
midi_file_path = os.path.join(base_path, 'test_audio-1_basic_pitch.mid')
music_path = os.path.join(base_path, 'test_audio-2.mp3')
bg_path = os.path.join(base_path, 'bg.jpg')
output_folder = os.path.join(base_path, 'output')
output_xml = os.path.join(output_folder, 'output_xml.xml')
output_ly = os.path.join(output_folder, 'output_ly.ly')
output_png_folder = os.path.join(output_folder, 'output_png_folder')
os.makedirs(output_folder, exist_ok=True)
os.makedirs(output_png_folder, exist_ok=True)

LILYPOND_PATH = '/opt/homebrew/bin/lilypond'
MUSESCORE_PATH = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'


def midi_to_musicxml(input_file, output_file):

  command = [MUSESCORE_PATH, input_file, "-o", output_file]
  subprocess.run(command)


def musicxml_to_ly(input_file, output_file):
  command = ["musicxml2ly", input_file, "-o", output_file]
  subprocess.run(command)


def ly_to_png(ly_file, png_output):
  command = [LILYPOND_PATH, "--png", "-o", png_output, ly_file]
  subprocess.run(command)


def add_settings_to_ly_file(ly_file_path, settings):
  with open(ly_file_path, 'r') as file:
    content = file.read()

  layout_pattern = re.compile(r'\\layout\s*{[^}]*}', re.DOTALL)
  settings_content = re.search(r'\\layout\s*{([^}]*)}', settings, re.DOTALL).group(1).strip()
  layout_content = layout_pattern.search(content)

  # If there's only one \layout { ... } section, this code will replace just the first one if there are multiple.
  # If the original content does not have a \layout { ... } section, it directly appends settings to the end.
  if layout_content:
      new_content = content.replace(layout_content.group(), r'\layout {' + settings_content + '}')
  else:
      new_content = content + "\n" + r'\layout {' + settings_content + '}'
      
  with open(ly_file_path, 'w') as file:
    file.write(new_content)


def main():
  midi_to_musicxml(midi_file_path, output_xml)
  musicxml_to_ly(output_xml, output_ly)
  add_settings_to_ly_file(output_ly,lily_partials.settings)
  ly_to_png(output_ly, output_png_folder)
  
  for _dirpath, _dirnames, filenames in os.walk(output_png_folder):
    # print('dddd----',dirpath,'----', dirnames,'----', filenames)
    for filename in filenames:
      full_path = os.path.join(output_png_folder, filename)
      # print('full_path---',full_path)
      transparent_png = turn_white_to_transparent(full_path)
      if transparent_png is not None:
        
        cv2.imwrite(full_path, transparent_png)

  return


if __name__ == '__main__':
  main()
