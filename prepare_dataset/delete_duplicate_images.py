#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
delete duplicate images
通过计算图片的哈希值来判断图片是否相同。如果哈希值相同，则可以认为图片是重复的
"""

from PIL import Image
import os
 
# 定义计算图片哈希值的函数
def get_image_hash(image):
    image = image.resize((8, 8), resample=Image.BILINEAR).convert("L")
    pixels = list(image.getdata())
    avg = sum(pixels) // len(pixels)
    hash_value = 0
    for pixel in pixels:
        if pixel > avg:
            hash_value = (hash_value << 1) + 1
        else:
            hash_value = hash_value << 1
    return hash_value

# 指定图片所在的目录
folder = "./imgs/powerLines"

#被删除的图片转移到单独的目录
deleted_folder = "./deleted"  
if not os.path.exists(deleted_folder):
    os.makedirs(deleted_folder)

# 定义空字典
hash_dict = {}
# 获取目录下所有文件名
files = os.listdir(folder)
for filename in files:
    print('filename',filename)
    # 过滤掉隐藏文件和非图片文件
    if not filename.startswith(".") and (filename.endswith(".png") or filename.endswith(".jpg")):
        filepath = os.path.join(folder, filename)
        try:
            # 使用PIL库打开图片文件
            with Image.open(filepath) as img:
                # 计算图片哈希值
                img_hash = get_image_hash(img)
                # 判断哈希值是否已经存在
                if img_hash in hash_dict:
                    print(f"Found duplicate image: {filename}")
                    os.rename(filepath, os.path.join(deleted_folder, filename))
                else:
                    hash_dict[img_hash] = filepath
        except Exception as e:
            print(f"Error processing image {filename}: {str(e)}")


