#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Play midi file
"""
import sys
sys.path.append('/Users/a/code/Wire_Note_Project')

from config import MIDI_PATH
import pygame


def play_midi(midi_path):
  pygame.init()
  pygame.mixer.init()
  pygame.mixer.music.load(midi_path)
  pygame.mixer.music.play()

  while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(10)

  pygame.quit()


if __name__ == "__main__":
  play_midi(MIDI_PATH)
