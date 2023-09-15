import os
import shutil


def make_small_dataset(dataset_path, output_dataset_path, n):
    dataset_small_path = os.path.join(
        os.path.dirname(dataset_path), output_dataset_path
    )
    os.makedirs(dataset_small_path, exist_ok=True)

    for subdir in os.listdir(dataset_path):
        subdir_path = os.path.join(dataset_path, subdir)
        new_subdir_path = os.path.join(dataset_small_path, subdir)

        if os.path.isdir(subdir_path):
            os.makedirs(new_subdir_path, exist_ok=True)

            for subsubdir in os.listdir(subdir_path):
                subsubdir_path = os.path.join(subdir_path, subsubdir)
                new_subsubdir_path = os.path.join(new_subdir_path, subsubdir)

                if os.path.isdir(subsubdir_path):
                    os.makedirs(new_subsubdir_path, exist_ok=True)

                    all_files = sorted(os.listdir(subsubdir_path))

                    for file in all_files[:n]:
                        src_path = os.path.join(subsubdir_path, file)
                        dest_path = os.path.join(new_subsubdir_path, file)
                        shutil.copy2(src_path, dest_path)
                        print(f"Copied {src_path} to {dest_path}")


base_path = "/Users/a/code/Wire_Note_Project/ttpla_dataset/data_original_size_v1/"
dataset_path = os.path.join(base_path, "dataset")
output_dataset_path = os.path.join(base_path, "dataset_small")
n = 100
make_small_dataset(dataset_path, output_dataset_path, n)
