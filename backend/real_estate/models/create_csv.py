#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制作csv文件
"""
import os
import csv
import datetime
import pandas as pd
import sys
import asyncio
from crawl_data import *


# 新建csv
def create_new_csv(file_name, header):
    with open(file_name , 'w') as f:  # 'w': 覆盖原文件重写
        f_writer = csv.writer(f)
        f_writer.writerow(header)
    return

house_list = asyncio.run(get_house_list())
print('house_list: ', house_list)
if len(house_list) > 0:
    keys_list = list(house_list[0].keys())
    print(keys_list)
    file_name='houses_data_2.csv'
    create_new_csv(file_name, keys_list)
    value_list=[]
    for it in house_list:
        value_list.append(list(it.values()))
    print(value_list)
    with open(file_name, 'a') as f:  # 'a': 从尾部添加
        f_writer = csv.writer(f)
        f_writer.writerows(value_list)