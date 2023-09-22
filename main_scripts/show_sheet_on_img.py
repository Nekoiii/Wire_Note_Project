import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import seaborn as sns

from ultralytics import YOLO

from draw_somethings.draw_box_and_label import draw_box_and_label

import sys
# print('xxxx-1',sys.path)
# sys.path.append('/Users/a/code/Wire_Note_Project')
sys.path.append(sys.path[0]+"/../")
sys.path.append(sys.path[0]+"/./draw_somethings")
# print('xxxx-2',sys.path)
from config import BASE_PATH,OUTPUTS_PATH,MIDI_PATH,BG_PATH,BGM_PATH,MODELS_PATH,CLASSES_COLORS
from main_scripts.draw_somethings.draw_something import draw_sheet

IF_SHOW_BOXES = True

WIRES_DETECT_MODEL_PATH=os.path.join(MODELS_PATH,'my_models/yolov8_wires_dect_best.pt')
SHEET_PATH=os.path.join(OUTPUTS_PATH,'output/output_png_folder/output_ly-page3.png')
OUTPUT_PATH=os.path.join(OUTPUTS_PATH,'show_sheet_on_img_output.jpg')


def draw_png_on_img(bg_img,png_img, x1, y1, x2, y2):
  for c in range(0, 3):
    bg_img[int(y1):int(y2), int(x1):int(x2), c] = bg_img[int(y1):int(y2), int(x1):int(x2), c] * (1 - png_img[:, :, 3] / 255.0) + \
    png_img[:, :, c] * (png_img[:, :, 3] / 255.0)
  return bg_img



def main():
  model = YOLO(WIRES_DETECT_MODEL_PATH)

  bg_img=cv2.imread(BG_PATH)
  sheet_img=Image.open(SHEET_PATH)
  sheet_img = np.array(sheet_img)


  results = model(bg_img)
  print('results--', results)
  result = results[0]
  boxes = np.array(result.boxes.xyxy.cpu(), dtype='int')
  classes = np.array(result.boxes.cls.cpu(), dtype='int')

  for cls, box in zip(classes, boxes):
    (x1, y1, x2, y2) = box
    class_name = result.names[cls]

    # if IF_SHOW_BOXES:
    #   draw_box_and_label(draw, class_name, CLASSES_COLORS, x1, y1, x2, y2)

    # Draw symbols for class 'cable'
    if class_name == 'cable':
      draw_sheet(bg_img,sheet_img,  x1, y1)

  cv2.imwrite('OUTPUT_PATH', bg_img)
  cv2.imshow('Output', bg_img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  
  return


if __name__ == "__main__":
  main()
