#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制作、处理csv文件
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

#爬取房产网站信息,建立csv
def create_house_list():
    return  #*爬取有风险,先封住,防止误操作
    house_list = asyncio.run(get_house_list())
    print('house_list: ', house_list)
    if len(house_list) > 0:
        keys_list = list(house_list[0].keys())
        print(keys_list)
        file_name='houses_data_1.csv'
        create_new_csv(file_name, keys_list)
        value_list=[]
        for it in house_list:
            value_list.append(list(it.values()))
        print(value_list)
        with open(file_name, 'a') as f:  # 'a': 从尾部添加
            f_writer = csv.writer(f)
            f_writer.writerows(value_list)
        
        
#全角转半角
def convert_to_helf_width(string):
    new_string_list=[]
    for char in string:
                num=ord(char)
                if num==0x3000:
                    num=32
                elif 0xFF01 <= num <= 0xFF5E:
                    num -= 0xfee0
                num = chr(num)
                new_string_list.append(num)
    new_string=''.join(new_string_list)
    return new_string
#执行全角转半角
def do_convert_to_helf_width():
    dataset_csv='houses_data_1.csv'           
    df=pd.read_csv(dataset_csv)
    df['price']=df['price'].apply(convert_to_helf_width)
    print(df['price'])            
    df.to_csv('convert_to_helf_width.csv', index=False)
    return


#去除空格或换行符\n
def remove_space(dataset_csv):
    df=pd.read_csv(dataset_csv)
    #*注: pandas中操作字符串一定要加.str啊啊啊啊
    #df['type']=df['type'].str.replace(' ','').str.replace('\n', '').str.replace('\r', '')
    df['nearest_station']=df['nearest_station'].str.replace(' ','').str.replace('\n', '').str.replace('\r', '')
    df.to_csv('remove_space.csv', index=False)
    return
#remove_space()

#添加'affordable'列
def add_affordable_col():
    dataset_csv='houses_data_1.csv'           
    df=pd.read_csv(dataset_csv)
    print(df.columns)
    affordable_list=[]
    thr=5000#价钱阈值
    for i,row in df.iterrows():
        #print(i,row['price'])
        affordable=0
        if not(row['price']>thr):
            affordable=1
        print(affordable)
        affordable_list.append(affordable)
    df['affordable']=affordable_list
    print(df['affordable'])
    df.to_csv('add_affordable.csv', index=False)
add_affordable_col()

#添加label列
def add_classification_label_col():
    dataset_csv='Absenteeism_at_work.csv'
    df=pd.read_csv(dataset_csv)
    label_col=[]
    #print(df.columns)
    #分为5档,0、1~5、6~10、11~30、>30
    #thr_list=[0,5,10,30]
    #分为3档,0、1~10、>10
    thr_list=[0,10]
    for i,row in df.iterrows():
        label=1#label设为从1开始
        for j in range(0,len(thr_list)):
            if(row['Absenteeism_time_in_hours']>thr_list[j]):
                label=j+2
        print(label)
        label_col.append(label)
    df['label']=label_col
    print(df['label'])
    df.to_csv('Absenteeism_at_work_new.csv', index=False)
add_classification_label_col()


