import json
import os
import shutil

from config import CLASSES, DATASET_BASE_PATH


# Transform COCO json to YOLO txt
# The format of the txt file is:
#   [class_id x_center y_center width height]
def json_to_yolo_txt(json_data, output_txt_file, classes):
  with open(output_txt_file, "w") as f:
    for shape in json_data["shapes"]:
      label = shape["label"]
      if label not in classes:
        continue

      points = shape["points"]
      x_min, y_min = map(min, zip(*points))
      x_max, y_max = map(max, zip(*points))

      x_center = (x_min + x_max) / 2
      y_center = (y_min + y_max) / 2
      width = x_max - x_min
      height = y_max - y_min

      # Normalize by image dimensions
      x_center /= json_data["imageWidth"]
      y_center /= json_data["imageHeight"]
      width /= json_data["imageWidth"]
      height /= json_data["imageHeight"]

      class_id = classes.index(label)
      f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")


def make_yolo_dataset(
    json_file, output_labels_folder, base_imgs_folder, output_images_folder, classes
):
  with open(json_file, "r") as f:
    json_data = json.load(f)

  # Make 'images' folder
  json_image_path = json_data["imagePath"]
  image_path = os.path.join(base_imgs_folder, json_image_path)
  output_image_path = os.path.join(output_images_folder, json_image_path)
  if not os.path.exists(image_path):
    print(f"Warning: {image_path} does not exist. Skipping...")
    return
  shutil.copy(image_path, output_image_path)

  # Make 'labels' folder
  image_name = json_image_path.split(".")[0]
  output_txt_file = os.path.join(output_labels_folder, image_name + ".txt")
  json_to_yolo_txt(json_data, output_txt_file, classes)


def main():
  base_path = DATASET_BASE_PATH
  output_folder = os.path.join(base_path, "dataset")
  input_base_path = os.path.join(base_path, "splitting_jsons")
  base_imgs_folder = os.path.join(base_path, "sized_data")
  subfolders = ["test_jsons", "val_jsons", "train_jsons"]

  for subfolder in subfolders:
    input_folder = os.path.join(input_base_path, subfolder)
    output_labels_folder = os.path.join(
        output_folder, "labels", subfolder.replace("_jsons", "")
    )
    output_images_folder = os.path.join(
        output_folder, "images", subfolder.replace("_jsons", "")
    )
    os.makedirs(output_labels_folder, exist_ok=True)
    os.makedirs(output_images_folder, exist_ok=True)

    for root, _dirs, files in os.walk(input_folder):
      for file in files:
        if file.endswith(".json"):
          json_file_path = os.path.join(root, file)
          make_yolo_dataset(
              json_file_path,
              output_labels_folder,
              base_imgs_folder,
              output_images_folder,
              CLASSES,
          )


if __name__ == "__main__":
  main()
