#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬取数据
网址:'https://www.homes.co.jp/kodate/chuko/list/'
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import asyncio
import re

url = 'https://www.homes.co.jp/kodate/chuko/list/'
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)',
          # *注: 不设置这个会被拒绝访问
          'origin': 'https://www.homes.co.jp',
          'referer': 'https://www.homes.co.jp/kodate/chuko/list/',
          }

# 新筑/中古一戶建/土地，池袋40min以内，车站15min以内，土地所有权，除去价格未定，价格低到高
# *注:encodeData字符串不能换行不然会失效!!!!
encodeData = 'cond%5Bsortby%5D=fee&cond%5Bprecond%5D=1004&referer=list&landingRouteAttr=a%3A3%3A%7Bs%3A8%3A%22category%22%3Bs%3A6%3A%22kodate%22%3Bs%3A5%3A%22btype%22%3Bs%3A5%3A%22chuko%22%3Bs%3A6%3A%22_route%22%3Bs%3A26%3A%22bukken_list_category_btype%22%3B%7D&totalhits=1%2C036&cond%5Bmbg%5D%5B1003%5D=1003&cond%5Bmbg%5D%5B1004%5D=1004&cond%5Bmbg%5D%5B1005%5D=1005&cond%5Bmoneyroom%5D=0&cond%5Bmoneyroomh%5D=0&cond%5Bfee_option_mitei%5D=1&cond%5Bhousearea%5D=0&cond%5Bhouseareah%5D=0&cond%5Blandarea%5D=0&cond%5Blandareah%5D=0&cond%5Bwalkminutesh%5D=15&cond%5Bcommute_eki%5D%5B0%5D=%E6%B1%A0%E8%A2%8B&cond%5Bcommute_time%5D%5B0%5D=40&cond%5Bcommute_transfer_count%5D%5B0%5D=0&cond%5Bhouseageh%5D=0&cond%5Bmcf%5D%5B120301%5D=120301&cond%5Bnewdate%5D=0&cond%5Bfreeword%5D=&cond%5Bfwtype%5D=1'
res = requests.post(url + '?' + encodeData, headers=header)
# res=requests.post(url, headers=header,res.request.headers)

# 获取总页数
soup = BeautifulSoup(res.text, 'lxml')
last_page_li = soup.find('li', {'class': 'lastPage'})  # 总页数
if last_page_li:
    last_page_a = last_page_li.find('a')
    last_page_num = int(last_page_a.attrs['data-page'])
    # print(last_page_num)


# 总物件数 #*problem:不知为何会比网页里的少
# totalhits_input = soup.find('input', id='totalhits')
# if totalhits_input:
#     totalhits_value = totalhits_input.attrs['value']
#     print( totalhits_value)

# 检查是否为数字or小数点
def check_num(string):
    return (string.isdigit() or string == '.')


# 获取单个物件的详细信息
# 返回price,space,BCR,FAR
async def get_house_details(house_obj):
    if (pd.isna(house_obj['href'])): return house_obj
    res = requests.post(house_obj['href'], headers=header)
    soup = BeautifulSoup(res.text, 'lxml')

    price_ele = soup.find(id='chk-bkc-moneyroom')  # 价格
    house_obj['price'] = price_ele.text.split('～')[0].split('(')[0].split('（')[0].replace(',', '').replace('万円','') if price_ele else np.NaN
    land_area_ele = soup.find(id='chk-bkc-landarea')  # 土地面积
    house_obj['land_area'] = ''.join(filter(check_num, re.split('[mｍ]', land_area_ele.text.split('～')[0])[0])) \
        if (land_area_ele and len(re.split('[mｍ]', land_area_ele.text.split('～')[0])) > 1) else np.NaN
    house_area_ele = soup.find(id='chk-bkc-housearea')  # 建物面积
    house_obj['house_area'] = ''.join(filter(check_num, re.split('[mｍ]', house_area_ele.text.split('～')[0])[0])) \
        if (house_area_ele and len(re.split('[mｍ]', house_area_ele.text.split('～')[0])) > 1) else np.NaN
    BCR_FAR_ele = soup.find(id='chk-bkd-landkenpeiyoseki')  # 建蔽率/容積率
    if BCR_FAR_ele:
        BCR_FAR_text_list = re.split('[／/・\u3000\s{1}]', BCR_FAR_ele.text.replace('建ぺい率・容積率', ''))
        print('ele', BCR_FAR_ele.text, BCR_FAR_text_list)
        house_obj['BCR'] = ''.join(filter(check_num, BCR_FAR_text_list[0].replace('%', '')))
        house_obj['FAR'] = ''.join(filter(check_num, BCR_FAR_text_list[1].replace('%', ''))) if len(
            BCR_FAR_text_list) > 1 else np.NaN
    station_ele = soup.find(class_='trafficText')  # 最近车站/徒步距离
    if station_ele:
        house_obj['nearest_station'] = station_ele.text.split('」')[0].split('「')[1]
        house_obj['station_dist'] = ''.join(filter(str.isdigit, station_ele.text.split('徒歩')[1])) \
            if len(station_ele.text.split('徒歩')) > 1 else np.NaN
    age_ele = soup.find(id='chk-bkc-kenchikudate')  # 建筑年数
    house_obj['age'] = filter(check_num, age_ele.text.split('築')[1]) \
        if (age_ele and len(age_ele.text.split('築')) > 1) else np.NaN
    can_not_be_rebuilt_ele = soup.body.findAll(text='再建築不可')  # 是否再建筑不可
    house_obj['can_not_be_rebuilt'] = True if len(can_not_be_rebuilt_ele) > 0 else False
    # _ele = soup.find(class_='')  #*模板
    # house_obj[''] = _ele.text if _ele else np.NaN
    print('house_obj-1 --', house_obj)
    return house_obj


# 遍历全部页面，获取所有物件
async def get_house_list():
    house_list = []
    last_page_num = 2  # *for test
    for i in range(last_page_num - 1):
        res = requests.post(url + '?page=' + str(int(i + 1)) + '?' + encodeData, headers=header)
        soup = BeautifulSoup(res.text, 'lxml')
        house_ele = soup.find_all(class_='moduleInner')  # 一个物件的整大块元素
        print(res)
        for j in house_ele:
            # 种类,链接,池袋时间,价格,土地面积,建物面积,建蔽率,容積率,最近车站,最近车站徒步距离,建筑年数,是否再建筑不可
            house_obj = {'id': np.NaN, 'type': np.NaN, 'href': np.NaN, 'ike_dist': np.NaN, 'price': np.NaN,
                         'land_area': np.NaN, 'house_area': np.NaN, 'BCR': np.NaN, 'FAR': np.NaN,
                         'nearest_station': np.NaN, 'station_dist': np.NaN,
                         'age': np.NaN, 'price': np.NaN, 'can_not_be_rebuilt': False}
            type_ele = j.find(class_='bType')  # 种类(土地/新筑一户建/中古一户建)
            house_obj['type'] = type_ele.text if type_ele else np.NaN
            ike_dist_ele = j.find(class_='time')  # 去池袋所需时间
            house_obj['ike_dist'] = ike_dist_ele.text.replace('分', '') if ike_dist_ele else np.NaN
            if pd.isna(house_obj['ike_dist']):  # Homes会显示pr物件,这里把它们筛选掉
                continue
            href_ele = j.find(class_='prg-bukkenNameAnchor')  # 物件链接
            if href_ele:
                house_obj['href'] = href_ele.attrs['href']
                house_obj['id'] = 'b-' + href_ele.attrs['href'].split('b-')[-1].replace('/', '')
                house_obj = await get_house_details(house_obj)
                house_list.append(house_obj)
    return house_list


house_list = asyncio.run(get_house_list())
print('house_list: ', house_list)
