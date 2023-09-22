

import cv2
from ultralytics import YOLO
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
import seaborn as sns


import sys
sys.path.append('/Users/a/code/Wire_Note_Project')

from config import CLASSES

def draw_box_and_label(draw, class_name, colors, x1, y1, x2, y2):
  color_index = CLASSES.index(class_name)
  color = colors[color_index]
  draw.rectangle([(x1, y1), (x2, y2)], outline=color, width=2)
  font = ImageFont.load_default()
  draw.text((x1, y1 - 5), class_name, font=font, fill=color)




