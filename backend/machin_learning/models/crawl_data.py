#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬取数据
网址:'https://www.homes.co.jp/list/'
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import asyncio
import re

url = 'https://www.homes.co.jp/list/'
# *注: 不设置User-Agent会被拒绝访问
# *problem:header里有些东西去掉后拿回来的数据会不一样,不知道哪些要哪些不要
header = {
    'accept': 'application/json, text/javascript',
    'content-type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'origin': 'https://www.homes.co.jp',
    'sec-ch-ua-platform': "macOS",
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'x-requested-with': 'XMLHttpRequest',
}

# 新筑/中古一戶建/土地，池袋40min以内，车站15min以内，土地所有权，除去价格未定，价格低到高
# *注:encodeData字符串不能换行不然会失效!!!!
encodeData = 'cond%5Bsortby%5D=fee&cond%5Bprecond%5D=1003&referer=list&landingRouteAttr=a%3A2%3A%7Bs%3A8%3A%22category%22%3Bs%3A6%3A%22kodate%22%3Bs%3A6%3A%22_route%22%3Bs%3A20%3A%22bukken_list_category%22%3B%7D&totalhits=1%2C038&cond%5Bmbg%5D%5B1003%5D=1003&cond%5Bmbg%5D%5B1004%5D=1004&cond%5Bmbg%5D%5B1005%5D=1005&cond%5Bmoneyroom%5D=0&cond%5Bmoneyroomh%5D=0&cond%5Bfee_option_mitei%5D=1&cond%5Bhousearea%5D=0&cond%5Bhouseareah%5D=0&cond%5Blandarea%5D=0&cond%5Blandareah%5D=0&cond%5Bwalkminutesh%5D=15&cond%5Bcommute_eki%5D%5B0%5D=%E6%B1%A0%E8%A2%8B&cond%5Bcommute_time%5D%5B0%5D=40&cond%5Bcommute_transfer_count%5D%5B0%5D=0&cond%5Bhouseageh%5D=0&cond%5Bmcf%5D%5B120301%5D=120301&cond%5Bnewdate%5D=0&cond%5Bfreeword%5D=&cond%5Bfwtype%5D=1'
# *注:encodeData不能直接加在url后不然后面翻页会失效啊啊啊啊!!!!
res = requests.post(url, headers=header, data=encodeData)

# 获取总页数
soup = BeautifulSoup(res.text, 'lxml')
last_page_li = soup.find('li', {'class': 'lastPage'})
if last_page_li:
    last_page_a = last_page_li.find('a')
    last_page_num = int(last_page_a.attrs['data-page'])
    print('last_page_num--', last_page_num)

# 总物件数   #*problem:不知为何和网页里的数不一样
totalhits_input = soup.find('input', id='totalhits')
if totalhits_input:
    totalhits_value = totalhits_input.attrs['value']
    print('totalhits_value-- ', totalhits_value)


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
    house_obj['price'] = ''.join(
        filter(check_num, price_ele.text.split('～')[0].split('(')[0].split('（')[0].split('・')[0].split('、')[0] \
               .replace(',', '').replace('，', '').replace('万円', ''))) if price_ele else np.NaN
    land_area_ele = soup.find(id='chk-bkc-landarea')  # 土地面积
    house_obj['land_area'] = ''.join(filter(check_num, re.split('[mｍ]', land_area_ele.text.split('～')[0])[0])) \
        if (land_area_ele and len(re.split('[mｍ]', land_area_ele.text.split('～')[0])) > 1) else np.NaN
    house_area_ele = soup.find(id='chk-bkc-housearea')  # 建物面积
    house_obj['house_area'] = ''.join(filter(check_num, re.split('[mｍ]', house_area_ele.text.split('～')[0])[0])) \
        if (house_area_ele and len(re.split('[mｍ]', house_area_ele.text.split('～')[0])) > 1) else np.NaN
    BCR_FAR_ele = soup.find(id='chk-bkd-landkenpeiyoseki')  # 建蔽率/容積率
    if BCR_FAR_ele:
        BCR_FAR_text_list = re.split('[%％/]', BCR_FAR_ele.text)
        house_obj['BCR'] = ''.join(filter(check_num, BCR_FAR_text_list[0]))
        house_obj['FAR'] = ''.join(filter(check_num, BCR_FAR_text_list[1])) \
            if len(BCR_FAR_text_list) > 1 else np.NaN
    else:
        BCR_ele = soup.find(id='chk-bkc-landkenpei')  # 建蔽率(有些页面要用这个才能找到)
        house_obj['BCR'] = ''.join(filter(check_num, BCR_ele.text.replace('%', ''))) \
            if BCR_ele else np.NaN
        FAR_ele = soup.find(id='chk-bkc-landyouseki')  # 容積率(有些页面要用这个才能找到)
        house_obj['FAR'] = ''.join(filter(check_num, FAR_ele.text.replace('%', ''))) \
            if FAR_ele else np.NaN
    station_ele = soup.find(id='chk-bkc-fulltraffic') if soup.find(id='chk-bkc-fulltraffic') \
        else soup.find(id='chk-bkd-fulltraffic')  # 最近车站/徒步距离
    if station_ele:
        if station_ele.text.find('」') > 0:
            house_obj['nearest_station'] = station_ele.text.split('」')[0].split('「')[1]
        elif len(re.compile('[駅.+線]').findall(station_ele.text)) > 0:
            house_obj['nearest_station'] = station_ele.text.split('駅')[0].split('線')[-1].replace(' ', '').replace('\n',
                                                                                                                  '').replace(
                '\r', '')
        house_obj['station_dist'] = ''.join(filter(str.isdigit, station_ele.text.split('徒歩')[1].split('分')[0])) \
            if len(station_ele.text.split('徒歩')) > 1 else np.NaN
        # print('station_ele.text--',house_obj['id'] ,station_ele.text,'---',house_obj['nearest_station'])

    age_ele = soup.find(id='chk-bkc-kenchikudate')  # 建筑年数
    house_obj['age'] = ''.join(filter(check_num, age_ele.text.split('築')[1])) \
        if (age_ele and len(age_ele.text.split('築')) > 1) else np.NaN
    can_not_be_rebuilt_ele = soup.body.findAll(text=re.compile('.*再建築不可.*'))  # 是否再建筑不可
    house_obj['can_not_be_rebuilt'] = True if len(can_not_be_rebuilt_ele) > 0 else False
    # print('house_obj---', house_obj)
    return house_obj
    # _ele = soup.find(class_='')  #*模板
    # house_obj[''] = _ele.text if _ele else np.NaN


# 遍历全部页面，获取所有物件
async def get_house_list():
    house_list = []
    # last_page_num = 3  # *for test
    for i in range(last_page_num - 1):
        # *注:encodeData不能直接加在这里啊啊啊啊
        # complete_url = url + '?page=' + str(int(i + 1)) + '&' + encodeData
        complete_url = url + '?page=' + str(int(i + 1))
        header['referer'] = complete_url
        res = requests.post(complete_url, headers=header, data=encodeData)
        print('x_url  --', complete_url)
        soup = BeautifulSoup(res.text, 'lxml')
        house_ele = soup.find_all(class_='moduleInner')  # 一个物件的整大块元素
        next_page = soup.find(class_='nextPage')
        print('next_page', next_page)
        print('res', res)
        for j in house_ele:
            # 种类,链接,池袋时间,价格,土地面积,建物面积,建蔽率,容積率,最近车站,最近车站徒步距离,建筑年数,是否再建筑不可
            house_obj = {'id': np.NaN, 'type': np.NaN, 'href': np.NaN, 'ike_dist': np.NaN, 'price': np.NaN,
                         'land_area': np.NaN, 'house_area': np.NaN, 'BCR': np.NaN, 'FAR': np.NaN,
                         'nearest_station': np.NaN, 'station_dist': np.NaN,
                         'age': np.NaN, 'can_not_be_rebuilt': False}
            type_ele = j.find(class_='bType')  # 种类(土地/新筑一户建/中古一户建)
            house_obj['type'] = type_ele.text.replace(' ', '').replace('\n', '').replace('\r',
                                                                                         '') if type_ele else np.NaN
            if house_obj['type'] == '一戸建て':
                house_obj['type'] = '中古一戸建て'
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

# house_list = asyncio.run(get_house_list())
# print('house_list: ', house_list)
