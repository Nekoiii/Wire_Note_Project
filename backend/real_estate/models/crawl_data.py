#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬取数据
网址:'https://www.homes.co.jp/kodate/chuko/list/'
"""

from bs4 import BeautifulSoup
import requests
import json
import urllib

url = 'https://www.homes.co.jp/kodate/chuko/list/'
# url = 'https://www.homes.co.jp/_ajax/list/'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)'
header = {'User-Agent': user_agent,
          # 'origin': 'https://www.homes.co.jp',
          # 'referer': 'https://www.homes.co.jp/kodate/chuko/list/',

          }
ss=urllib.parse.unquote('a%3A3%3A%7Bs%3A8%3A%22category%22%3Bs%3A6%3A%22kodate%22%/3Bs%3A5%3A%22btype%22%3Bs%3A5%3A%22chuko%22%3Bs%3A6%3A%22_route%22%3Bs%3A26%3A%22bukken_list_category_btype%22%3B%7D')
# print('ssss',ss)
data = {'cond[sortby]': 'fee',
        'cond[mbg][1004]': 1004,
        'landingRouteAttr': ss,
        'cond[commute_eki][0]': '池袋',
        'cond[commute_time][0]': '40',
        'cond[commute_transfer_count][0]': 0
        }

# res = requests.post(url, headers=header, json=data)
res=requests.post(url, headers=header)
# print(res.text)
# print(res.request.body)
# print(res.request.headers)

soup = BeautifulSoup(res.text, 'lxml')
# print(context)
bukkenList=soup.find_all('div',{'class':'mod-bukkenList'})
print(bukkenList)