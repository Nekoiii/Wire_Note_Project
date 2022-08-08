# 用来创建虚拟数据
import numpy as np
import csv
import random

# 创建家具厂,记录100条购买记录
furniture_list = []


def create_furniture_list():
    for i in range(65, 91):  # 创建26个以大写字母为名的家具
        furniture_list.append(chr(i))
    print(furniture_list)
    return furniture_list


# 创建100条记录, 把家具随机分配给每条记录
def distribute_funrniture(user_num, furniture_list):
    with open('furniture_factory.csv', 'w') as f:
        f_writer = csv.writer(f)
        funi_thro_list = []  # 给每个家具随机生成一个阈值
        for i in furniture_list:
            threshold = random.randint(0, 10)  # 随机生成阈值
            funi_thro_list.append(threshold)
        max_cols = 0
        the_list = []
        for i in range(0, user_num):  # 把家具随机分配给每条记录
            a_list = []
            for i_2, val_2 in enumerate(furniture_list):
                random_num = random.randint(0, 10)  # 再随机生成一个数
                if random_num > funi_thro_list[i_2]:  # 如果随机数>家具阈值,则放进去
                    a_list.append(furniture_list[i_2])
            if len(a_list) > max_cols:
                max_cols = len(a_list)
            # print('a_list',a_list)
            the_list.append(a_list)

        for a_list in the_list:  # 统一每行的列数,不然读取时会报错
            if len(a_list) < max_cols:
                a_list.extend((max_cols - len(a_list)) * [None])
            f_writer.writerow(a_list)
    return


def create_furniture_factory():
    furniture_list = create_furniture_list()
    distribute_funrniture(100, furniture_list)
    return


create_furniture_factory()


# 创建10个房子,10000条记录,1/0表示是否收藏了此物件
def create_houses_marks_record():
    houses = []
    csv_header=[]
    for i in range(0, 10):  # 生成10个房子
        houses.append({'name': 'House_' + str(i + 1)})
        csv_header.append('House_' + str(i + 1))
    with open('houses_marks_record.csv', 'w') as f:  # 'w':  覆盖原文件重写
        f_writer = csv.writer(f)
        f_writer.writerow(csv_header)
    for i, j in enumerate(houses):  # 给每个房子随机生成一个阈值
        threshold = random.randint(1, 800)  # 随机生成[1,800]间的阈值
        j['thre'] = threshold
    #print(houses)
    for i in houses:
        print(i['thre'])
    for i in range(0, 10000):  # 创建10000条记录
        a_row=[]
        for x, y in enumerate(houses):
            mark = 0
            threshold = random.randint(0, 2000)  # 随机生成阈值
            if threshold < y['thre']:
                mark = 1
            a_row.append(mark)
        with open('houses_marks_record.csv', 'a') as f:  # 'a': 从尾部添加
            f_writer = csv.writer(f)
            f_writer.writerow(a_row)# *注:这里别写成writerows了啊啊啊啊
create_houses_marks_record()

