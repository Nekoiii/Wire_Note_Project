import os
import mido
from mido import MidiFile
import pygame
import time

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import seaborn as sns

base_path = '/Users/a/code/Wire_Note_Project/try_audio_to_sheet'
midi_file_path = os.path.join(base_path, 'test_audio-1_basic_pitch.mid')
music_path = os.path.join(base_path, 'test_audio-2.mp3')
bg_path = os.path.join(base_path, 'bg.jpg')

note_to_char = {
    21: 'A0', 22: 'Bb0', 23: 'B0',
    24: 'C1', 25: 'Db1', 26: 'D1', 27: 'Eb1', 28: 'E1', 29: 'F1', 30: 'Gb1', 31: 'G1', 32: 'Ab1', 33: 'A1', 34: 'Bb1', 35: 'B1',
    36: 'C2', 37: 'Db2', 38: 'D2', 39: 'Eb2', 40: 'E2', 41: 'F2', 42: 'Gb2', 43: 'G2', 44: 'Ab2', 45: 'A2', 46: 'Bb2', 47: 'B2',
    48: 'C3', 49: 'Db3', 50: 'D3', 51: 'Eb3', 52: 'E3', 53: 'F3', 54: 'Gb3', 55: 'G3', 56: 'Ab3', 57: 'A3', 58: 'Bb3', 59: 'B3',
    60: 'C4', 61: 'Db4', 62: 'D4', 63: 'Eb4', 64: 'E4', 65: 'F4', 66: 'Gb4', 67: 'G4', 68: 'Ab4', 69: 'A4', 70: 'Bb4', 71: 'B4',
    72: 'C5', 73: 'Db5', 74: 'D5', 75: 'Eb5', 76: 'E5', 77: 'F5', 78: 'Gb5', 79: 'G5', 80: 'Ab5', 81: 'A5', 82: 'Bb5', 83: 'B5',
    84: 'C6', 85: 'Db6', 86: 'D6', 87: 'Eb6', 88: 'E6', 89: 'F6', 90: 'Gb6', 91: 'G6', 92: 'Ab6', 93: 'A6', 94: 'Bb6', 95: 'B6',
    96: 'C7', 97: 'Db7', 98: 'D7', 99: 'Eb7', 100: 'E7', 101: 'F7', 102: 'Gb7', 103: 'G7', 104: 'Ab7', 105: 'A7', 106: 'Bb7', 107: 'B7',
    108: 'C8'
}


mid = MidiFile(midi_file_path)


def midi_to_chars(mid):
  chars = []
  notes = []

  for track in mid.tracks:
    for msg in track:
      if msg.type == 'note_on':
        char = note_to_char.get(msg.note, '?')
        chars.append(char)
        notes.append((msg.note, msg.time))

  result = '-'.join(chars)
  print(result)
  print(notes)
  return notes


notes = midi_to_chars(mid)


def play_midi(midi_file_path):
  pygame.mixer.init()

  pygame.mixer.music.load(midi_file_path)
  pygame.mixer.music.play()

  # 由于播放是异步的，我们要等待音乐播放完毕
  while pygame.mixer.music.get_busy():
    time.sleep(1)  # 等待1秒钟

  pygame.mixer.quit()


play_midi(midi_file_path)


def show():

  # Show img and notes
  bg = Image.open(bg_path)
  bg_width, bg_height = bg.size
  screen = pygame.display.set_mode((bg_width, bg_height))
  pygame.display.set_caption('Music Visualization')
  font = ImageFont.load_default()
  font_size = 100
  font = ImageFont.truetype("Arial.ttf", font_size)

  def draw_notes_on_image(bg_path, notes, note_to_char):
    bg = Image.open(bg_path)
    draw = ImageDraw.Draw(bg)

    x_offset = 10  # start drawing 10 pixels from the left
    y_position = bg.height // 2  # middle of the image

    for note, _ in notes:
      char = note_to_char.get(note, '?')
      draw.text((x_offset, y_position - font_size // 2), char, font=font, fill=(255, 255, 255))
      x_offset += font_size + 5  # 5 pixels space between each character

    return bg

  bg_with_notes = draw_notes_on_image(bg_path, notes, note_to_char)
  # Convert PIL Image to Pygame Surface
  bg_pygame = pygame.image.fromstring(bg_with_notes.tobytes(), bg_with_notes.size, bg_with_notes.mode)

  # Play music
  pygame.mixer.init()
  pygame.mixer.music.load(music_path)
  pygame.mixer.music.play()

  # Show img with notes
  screen = pygame.display.set_mode((bg_width, bg_height))
  pygame.display.set_caption('Music Visualization')

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    screen.blit(bg_pygame, (0, 0))
    pygame.display.flip()

  pygame.quit()
