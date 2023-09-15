# ultralytics - yolov8 github: https://github.com/ultralytics/ultralytics
# yolov8 docs: https://docs.ultralytics.com/modes/train/#introduction
# https://watlab-blog.com/2023/08/20/ultralytics-yolov8/
# https://chem-fac.com/yolov8/

import cv2
from ultralytics import YOLO
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont

base_path = '/Users/a/code/Wire_Note_Project/try_yolov8/'
video_path = os.path.join(base_path, 'sky-3.MOV')
print('file exists?', os.path.exists(video_path))
print(os.getcwd())

IF_SHOW_BOXES = False

# '♪', '♩', '♫', '♬', '♭', '♮', '♯', '𝄪', '𝄫''''𝄞', ',', '🎶, ', '🎶🎶, '🎶'
symbols_weights = [
    {'symbol': '♪', 'weight': 40},
    {'symbol': '♩', 'weight': 20},
    {'symbol': '♫', 'weight': 30},
    {'symbol': '♬', 'weight': 20},
    {'symbol': '♭', 'weight': 5},
    {'symbol': '♮', 'weight': 5},
    {'symbol': '♯', 'weight': 5},
    {'symbol': '𝄪', 'weight': 1},
    {'symbol': '𝄫', 'weight': 2},
    {'symbol': '𝄞', 'weight': 1},
    {'symbol': '𝄢', 'weight': 1},
]

symbols = [item['symbol'] for item in symbols_weights]
weights_int = [item['weight'] for item in symbols_weights]
total_weight = sum(weights_int)
weights = [w/total_weight for w in weights_int]


# The performance of the model increases with
# yolov8n < yolov8s < yolov8m < yolov8l < yolov8x, but on the
# other hand it takes time for learning and inference.
# model = YOLO('yolov8m.pt')
model = YOLO(os.path.join(base_path, 'best.pt'))

cap = cv2.VideoCapture(video_path)
while cap.isOpened():
  ret, frame = cap.read()
  if not ret:
    print('Error reading the video.')
    break

  results = model(frame)
  result = results[0]
  # print('result--', result)

  boxes = np.array(result.boxes.xyxy.cpu(), dtype='int')
  classes = np.array(result.boxes.cls.cpu(), dtype='int')

  # Define different colors for each class
  colors = {
      'cable': (0, 0, 255),
      'tower_wooden': (0, 255, 0)
  }

  pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
  draw = ImageDraw.Draw(pil_img)

  for cls, box in zip(classes, boxes):
    (x1, y1, x2, y2) = box
    class_name = result.names[cls]

    if IF_SHOW_BOXES:
      draw.rectangle([(x1, y1), (x2, y2)], outline=colors[class_name], width=2)

    # Draw symbols for class 'cable'
    if class_name == 'cable':
      center_x = (x1 + x2) // 2
      center_y = (y1 + y2) // 2
      font_size = 100
      font_path = os.path.join(base_path, 'NotoMusic-Regular.ttf')
      font = ImageFont.truetype(font_path, font_size)
      symbol = np.random.choice(symbols, p=weights)
      symbol_color = (0, 0, 0)

      draw.text((center_x, center_y), symbol, font=font, fill=symbol_color)
    else:
      if IF_SHOW_BOXES:
        font = ImageFont.load_default()
        draw.text((x1, y1 - 5), class_name, font=font, fill=colors[class_name])

  frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
  cv2.imshow('Movie', frame)

  if cv2.waitKey(1) == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
