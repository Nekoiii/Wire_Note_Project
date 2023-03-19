#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
参考文章：https://zhuanlan.zhihu.com/p/367325899
"""
import requests
import os
import re
from bs4 import BeautifulSoup
import time
import random

keyword='电线杆'

def get_images_from_baidu(keyword, page_num, save_dir):
  header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
  #请求的url
  url = 'https://image.baidu.com/search/acjson?'
  n = 0
  for pn in range(0, 30 * page_num, 30):
    # 请求参数  
    param ={'tn': 'resultjson_com',
       # 'logid': '7603311155072595725',
       'ipn': 'rj',
       'ct': 201326592,
       'is': '',
       'fp': 'result',
       'queryWord': keyword,
       'cl': 2,
       'lm': -1,
       'ie': 'utf-8',
       'oe': 'utf-8',
       'adpicid': '',
       'st': -1,
       'z': '',
       'ic': '',
       'hd': '',
       'latest': '',
       'copyright': '',
       'word': keyword,
       's': '',
       'se': '',
       'tab': '',
       'width': '',
       'height': '',
       'face': 0,
       'istype': 2,
       'qc': '',
       'nc': '1',
       'fr': '',
       'expermode': '',
       'force': '',
       'cg': '',    # 这个参数没公开，但是不可少
       'pn': pn,    # 显示：30-60-90
       'rn': '30',  # 每页显示 30 条
       'gsm': '1e',
           # 'logid': '7603311155072595725',
            'ipn': 'rj',
            'ct': 201326592,
            'is': '',
            'fp': 'result',
            'queryWord': keyword,
            'cl': 2,
            'lm': -1,
            'ie': 'utf-8',
            'oe': 'utf-8',
            'adpicid': '',
            'st': -1,
            'z': '',
            'ic': '',
            'hd': '',
            'latest': '',
            'copyright': '',
            'word': keyword,
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': 0,
            'istype': 2,
            'qc': '',
            'nc': '1',
            'fr': '',
            'expermode': '',
            'force': '',
            'cg': '',    # 这个参数没公开，但是不可少
            'pn': pn,    # 显示：30-60-90
            'rn': '30',  # 每页显示 30 条
            'gsm': '1e',
            '1618827096642': ''
            }
    request = requests.get(url=url, headers=header, params=param)
    if request.status_code == 200:
        print('Request success.')
    request.encoding = 'utf-8'
    # 正则方式提取图片链接
    html = request.text
    image_url_list = re.findall('"thumbURL":"(.*?)",', html, re.S)
    print(image_url_list)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for image_url in image_url_list:
      try:
        image_data = requests.get(url=image_url, headers=header).content
        with open(os.path.join(save_dir, f'{n:06d}.jpg'), 'wb') as fp:
            fp.write(image_data)
        n = n + 1
        # 设置每爬取一张图片就随机等待一段时间，避免被反爬虫检测
        time.sleep(random.uniform(0.5, 1.5))
      except:
        print('下载图片出错')


if __name__ == '__main__':
    keyword = '电线杆'
    save_dir = './imgs/powerLines'
    page_num = 30
    get_images_from_baidu(keyword, page_num, save_dir)
    print('Got images successfully.')



