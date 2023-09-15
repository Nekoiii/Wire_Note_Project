# ultralytics - yolov8 github: https://github.com/ultralytics/ultralytics
# yolov8 docs: https://docs.ultralytics.com/modes/train/#introduction
# https://watlab-blog.com/2023/08/20/ultralytics-yolov8/
# https://chem-fac.com/yolov8/

import cv2
from ultralytics import YOLO
import numpy as np
import os

base_path = "/Users/a/code/Wire_Note_Project/try_yolov8/"
video_path = os.path.join(base_path, "sky-2.MOV")
print("file exists?", os.path.exists(video_path))
print(os.getcwd())

# def yolov8_object_detection():
#     return


# The performance of the model increases with
# yolov8n < yolov8s < yolov8m < yolov8l < yolov8x, but on the
# other hand it takes time for learning and inference.
# model = YOLO("yolov8m.pt")
model = YOLO(os.path.join(base_path, "best.pt"))
# model.train(
#     data="/Users/a/code/Wire_Note_Project/try_yolov8/try_yolov8.yaml",
#     epochs=300,
#     imgsz=640,
# )
# metrics = model.val()
# print("metrics--", metrics)

cap = cv2.VideoCapture(video_path)
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
