# ultralytics - yolov8 github: https://github.com/ultralytics/ultralytics
# yolov8 docs: https://docs.ultralytics.com/modes/train/#introduction
# https://watlab-blog.com/2023/08/20/ultralytics-yolov8/
# https://chem-fac.com/yolov8/

import cv2
from ultralytics import YOLO
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
import seaborn as sns

from symbols_data import symbols_weights
from config import CLASSES

base_path = '/Users/a/code/Wire_Note_Project/try_yolov8/'
video_path = os.path.join(base_path, '../assets/videos/sky-3.MOV')
print('file exists?', os.path.exists(video_path))
# print(os.getcwd())

IF_SHOW_BOXES = True
IF_SAVE_OUTPUT_VIDEO = False

"""
# The performance of the model increases with
# yolov8n < yolov8s < yolov8m < yolov8l < yolov8x, but on the
# other hand it takes time for learning and inference.
# model = YOLO('yolov8m.pt')
"""
model = YOLO(os.path.join(base_path, 'best.pt'))


cap = cv2.VideoCapture(video_path)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter(os.path.join(base_path, 'output_video.mp4'), fourcc, fps, frame_size)


def draw_notes(draw, x1, y1, x2, y2):
  symbols = [item['symbol'] for item in symbols_weights]
  weights_int = [item['weight'] for item in symbols_weights]
  total_weight = sum(weights_int)
  weights = [w/total_weight for w in weights_int]

  center_x = (x1 + x2) // 2
  center_y = (y1 + y2) // 2
  font_size = 100
  font_path = os.path.join(base_path, 'NotoMusic-Regular.ttf')
  font = ImageFont.truetype(font_path, font_size)
  symbol = np.random.choice(symbols, p=weights)
  symbol_color = (0, 0, 0)

  draw.text((center_x, center_y), symbol, font=font, fill=symbol_color)


def draw_box_and_label(draw, class_name, colors, x1, y1, x2, y2):
  color_index = CLASSES.index(class_name)
  color = colors[color_index]
  draw.rectangle([(x1, y1), (x2, y2)], outline=color, width=2)
  font = ImageFont.load_default()
  draw.text((x1, y1 - 5), class_name, font=font, fill=color)


def main():
  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      print(f'Failed to read video {video_path}')
      break

    results = model(frame)
    result = results[0]
    # print('result--', result)

    boxes = np.array(result.boxes.xyxy.cpu(), dtype='int')
    classes = np.array(result.boxes.cls.cpu(), dtype='int')

    # Define different colors for each class
    colors = [(int(r*255), int(g*255), int(b*255)) for r, g, b in
              sns.color_palette('pastel', len(CLASSES))]

    pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)

    for cls, box in zip(classes, boxes):
      (x1, y1, x2, y2) = box
      class_name = result.names[cls]

      if IF_SHOW_BOXES:
        draw_box_and_label(draw, class_name, colors, x1, y1, x2, y2)

      # Draw symbols for class 'cable'
      if class_name == 'cable':
        draw_notes(draw, x1, y1, x2, y2)

    frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    if IF_SAVE_OUTPUT_VIDEO:
      out.write(frame)

    cv2.imshow('Movie', frame)

    if cv2.waitKey(1) == ord('q'):
      break

  cap.release()
  out.release()
  cv2.destroyAllWindows()


if __name__ == '__main__':
  main()
