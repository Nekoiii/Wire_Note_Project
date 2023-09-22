import os
import mido
from mido import MidiFile
import pygame
import time

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import seaborn as sns

import sys
sys.path.append('/Users/a/code/Wire_Note_Project')

from config import BASE_PATH,MIDI_PATH,BG_PATH,BGM_PATH,MODELS_PATH


WIRES_DETECT_MODEL_PATH=os.path.join(MODELS_PATH,'yolov8_wires_dect_best.pt')

mid = MidiFile(MIDI_PATH)
print({MIDI_PATH})





def main():
  bg = Image.open(BG_PATH)
  bg_width, bg_height = bg.size
  screen = pygame.display.set_mode((bg_width, bg_height))


  return


if __name__ == "__main__":
  main()