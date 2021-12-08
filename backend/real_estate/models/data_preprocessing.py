#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
数据预处理
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import csv

#dataset_csv='houses_data_1.csv'

'''df=pd.read_csv('XXX.csv')
df['type']=df['type'].str.replace('xxx','中古一戸建て')
df.to_csv('XXX.csv', index=False) '''   

#去空格和换行符

#去除空格或换行符\n
def remove_space(dataset_csv):
    df=pd.read_csv(dataset_csv)
    #*注: pandas中操作字符串一定要加.str啊啊啊啊
    #df['type']=df['type'].str.replace(' ','').str.replace('\n', '').str.replace('\r', '')
    df['nearest_station']=df['nearest_station'].str.replace(' ','').str.replace('\n', '').str.replace('\r', '')
    df.to_csv('remove_space.csv', index=False)
    return
#remove_space()

#数据去重
def data_deduplication():
    dataset_csv='houses_data_1.csv'
    df=pd.read_csv(dataset_csv)
    usecols=['type','ike_dist','price','land_area','house_area', 'BCR', 'FAR','nearest_station', 'station_dist','age', 'can_not_be_rebuilt']
    df_deduplication=df.drop_duplicates(usecols) 
    print (df.size,df_deduplication.size)
    df_deduplication.to_csv('data_deduplication.csv', index=False)


#导入df,返回x,y
def import_dataset(dataset_csv):
    df=pd.read_csv(dataset_csv)
    #*注:X中就算只取单列也不能不能[:, 1],一定要[:, 1:2]!!!!
    X=np.hstack((df.iloc[:, 1:2].values,df.iloc[:, 3:4].values,df.iloc[:, 5:9].values,df.iloc[:, 10:].values))
    y=df.iloc[:, 4].values
    print(X[1])
    print(y)
    return(X,y)
#X,y=import_dataset()


#处理缺失数据,返回补全的数据
def process_missing_data(data):
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputer.fit(data)
    data=imputer.transform(data)
    return(data)
#X[:, 1:-1]=process_missing_data(X[:, 1:-1])

#分类型数据用OneHotEncoder进行标准化
def do_OneHotEncoder(data,col_i):
    ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [col_i])], remainder='passthrough')
    data=np.array(ct.fit_transform(data))
    #data=ct.fit_transform(data).toarray()#problem:不知为何有时上面那条不能用要用这个,有时候下面这个用不了只能用上面的
    #防止虚拟变量陷阱,去掉第一列
    data=data[:,1:]
    return(data)
#print(X[0])
#X=do_OneHotEncoder(X,0)
#X=do_OneHotEncoder(X,-1)

#分为训练集、测试集
def split_training_and_test(X,y,test_size=0.2,random_state=0):
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=random_state)
    return(X_train,X_test,y_train,y_test)

#X_train,X_test,y_train,y_test=split_training_and_test(X,y)
#print(X_train[0],X_test[0],y_train[0],y_test[0])

#归一化
def do_standrad_scaler(data):
    sc=StandardScaler()
    data=sc.fit_transform(data)
    return(sc,data)

#画图
def draw_plot(x_train,y_train):
    plt.scatter(x_train,y_train,color='red')



