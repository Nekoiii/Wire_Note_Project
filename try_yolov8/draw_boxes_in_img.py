import os
import cv2

base_path = "/Users/a/code/Wire_Note_Project/ttpla_dataset/data_original_size_v1"

dataset_path = os.path.join(base_path, "dataset_small")
images_path = os.path.join(dataset_path, "images")
labels_path = os.path.join(dataset_path, "labels")
output_path = os.path.join(base_path, "img_with_boxes")
os.makedirs(output_path, exist_ok=True)

# *unfinished: need to be refined
classes = ["cable", "tower_wooden"]
colors = [(0, 0, 255), (0, 255, 0)]
class_colors = dict(zip(classes, colors))

for subset in ["train", "test", "val"]:
    subset_images_path = os.path.join(images_path, subset)
    subset_labels_path = os.path.join(labels_path, subset)
    subset_output_path = os.path.join(output_path, subset)
    os.makedirs(subset_output_path, exist_ok=True)

    for image_name in os.listdir(subset_images_path):
        image_path = os.path.join(subset_images_path, image_name)
        label_path = os.path.join(
            subset_labels_path, image_name.replace(".jpg", ".txt")
        )

        image = cv2.imread(image_path)
        with open(label_path, "r") as f:
            labels = f.readlines()

        for label in labels:
            class_id, x_center, y_center, width, height = map(
                float, label.strip().split()
            )
            class_id = int(class_id)
            class_name = classes[class_id]

            x_center, y_center, width, height = (
                x_center * image.shape[1],
                y_center * image.shape[0],
                width * image.shape[1],
                height * image.shape[0],
            )
            x1, y1, x2, y2 = (
                int(x_center - width / 2),
                int(y_center - height / 2),
                int(x_center + width / 2),
                int(y_center + height / 2),
            )

            cv2.rectangle(image, (x1, y1), (x2, y2), class_colors[class_name], 2)
            cv2.putText(
                image,
                class_name,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2,
            )

        cv2.imwrite(os.path.join(subset_output_path, image_name), image)
