# 用来创建虚拟数据
import csv
import random

# 创建家具厂,记录1000条购买记录
furniture_list=[]
def create_furniture_list():
    for i in range(65,91):#创建26个以大写字母为名的家具
        furniture_list.append(chr(i))
    print(furniture_list)
    return furniture_list
#创建1000条记录, 把家具随机分配给每条记录
def distribute_funrniture(user_num,furniture_list):
    with open('furniture_factory.csv' , 'w') as f:
        f_writer = csv.writer(f)
        funi_thro_list=[]#给每个家具随机生成一个阈值
        for i in furniture_list:
            threshold=random.randint(0,10)#随机生成阈值
            funi_thro_list.append(threshold)
                        
        for i in range(0,user_num+1):#把家具随机分配给每条记录
            a_list=[]
            for i_2,val_2 in  enumerate(furniture_list):
                random_num=random.randint(0,10)#再随机生成一个数
                if random_num>funi_thro_list[i_2]:#如果随机数>家具阈值,则放进去
                    a_list.append(furniture_list[i_2])
            print('a_list',a_list)
            f_writer.writerow(a_list)
    return
                

def create_furniture_factory():
    furniture_list=create_furniture_list()
    distribute_funrniture(1000,furniture_list)
    
    return     
    
create_furniture_factory()








