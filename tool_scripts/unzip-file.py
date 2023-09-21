import zipfile

path_to_zip_file = (
    "/Users/a/Desktop/datasets/powerLines-ttpla/data_original_size_v1.zip"
)
directory_to_extract_to = "./ttpla_dataset"
with zipfile.ZipFile(path_to_zip_file, "r") as zip_ref:
    zip_ref.extractall(directory_to_extract_to)
