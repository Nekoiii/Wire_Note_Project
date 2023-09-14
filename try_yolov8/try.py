# https://watlab-blog.com/2023/08/20/ultralytics-yolov8/
# https://chem-fac.com/yolov8/

import cv2
from ultralytics import YOLO
import numpy as np
import os

print("file exists?", os.path.exists("sky-1.MOV"))
print(os.getcwd())

# def yolov8_object_detection():
#     return


# The performance of the model increases with
# yolov8n < yolov8s < yolov8m < yolov8l < yolov8x, but on the
# other hand it takes time for learning and inference.
model = YOLO("yolov8m.pt")
cap = cv2.VideoCapture("sky-1.MOV")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error reading the video.")
        break

    results = model(frame)
    # print("results---", results)
    result = results[0]

    # boxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
    # classes = np.array(result.boxes.cls.cpu(), dtype="int")
    # for cls, box in zip(classes, boxes):
    #     (x1, y1, x2, y2) = box
    #     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    #     cv2.putText(
    #         frame, str(cls), (x1, y1 - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2
    #     )

    # cv2.imshow("Img", frame)

    img_annotated = results[0].plot()

    cv2.imshow("Movie", img_annotated)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
