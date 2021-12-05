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
import numpy as np

url = 'https://www.homes.co.jp/kodate/chuko/list/'
# url = 'https://www.homes.co.jp/_ajax/list/'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)'
header = {'User-Agent': user_agent,
          'origin': 'https://www.homes.co.jp',
          'referer': 'https://www.homes.co.jp/kodate/chuko/list/',
          }

# 中古一戶建，池袋40min以内，车站15min以内，土地所有权，价格低到高
#注:encodeData字符串不能换行不然会失效!!!!
encodeData = 'cond%5Bsortby%5D=fee&cond%5Bprecond%5D=1004&referer=list&landingRouteAttr=a%3A3%3A%7Bs%3A8%3A%22category%22%3Bs%3A6%3A%22kodate%22%3Bs%3A5%3A%22btype%22%3Bs%3A5%3A%22chuko%22%3Bs%3A6%3A%22_route%22%3Bs%3A26%3A%22bukken_list_category_btype%22%3B%7D&totalhits=288&cond%5Bmbg%5D%5B1004%5D=1004&cond%5Bmoneyroom%5D=0&cond%5Bmoneyroomh%5D=0&cond%5Bhousearea%5D=0&cond%5Bhouseareah%5D=0&cond%5Blandarea%5D=0&cond%5Blandareah%5D=0&cond%5Bwalkminutesh%5D=15&cond%5Bcommute_eki%5D%5B0%5D=%E6%B1%A0%E8%A2%8B&cond%5Bcommute_time%5D%5B0%5D=40&cond%5Bcommute_transfer_count%5D%5B0%5D=0&cond%5Bhouseageh%5D=0&cond%5Bmcf%5D%5B120301%5D=120301&cond%5Bnewdate%5D=0&cond%5Bfreeword%5D=&cond%5Bfwtype%5D=1'
res = requests.post(url + '?' + encodeData, headers=header)
# res=requests.post(url, headers=header,res.request.headers)

#获取总页数
soup = BeautifulSoup(res.text, 'lxml')
last_page_li = soup.find('li', {'class': 'lastPage'})#总页数
if last_page_li:
    last_page_a = last_page_li.find('a')
    last_page_num = int(last_page_a.attrs['data-page'])
    print(last_page_num)

#获取所有物件的链接
href_list=[]
for i in range(last_page_num-1):
    res=requests.post(url + '?page='+str(i)+'?' + encodeData, headers=header)
    bukkenNameAnchor_list = soup.find_all(class_='prg-bukkenNameAnchor')
    href_list .extend([x.attrs['href'] for x in bukkenNameAnchor_list])
print(href_list)

#总物件数
'''totalhits_input = soup.find('input', id='totalhits')
if totalhits_input:
    totalhits_value = totalhits_input.attrs['value']
    print( totalhits_value)'''


