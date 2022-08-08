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
from sklearn.preprocessing import LabelEncoder
import csv

#dataset_csv='houses_data_1.csv'

'''df=pd.read_csv('XXX.csv')
df['type']=df['type'].str.replace('xxx','中古一戸建て')
df.to_csv('XXX.csv', index=False) '''   

#分析数据
def data_analysis():
    df=pd.read_csv('houses_data_1.csv')
    #观察数据集概况
    df.info()
    #列出表头
    df.columns
    #查看某一列数据的详细情况
    df['price'].describe()
    df['land_area'].describe()
    df['nearest_station'].describe()

#数据去重
def data_deduplication():
    dataset_csv='houses_data_1.csv'
    df=pd.read_csv(dataset_csv)
    usecols=['type','price','land_area','house_area', 'BCR', 'FAR','nearest_station', 'station_dist','age', 'can_not_be_rebuilt']
    df_deduplication=df.drop_duplicates(usecols) 
    print (df.size,df_deduplication.size)
    df_deduplication.to_csv('data_deduplication.csv', index=False)


#处理缺失数据,返回补全的数据
#data:numpy.ndarray
def process_missing_data(data):
    from sklearn.impute import SimpleImputer
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputer.fit(data)
    data=imputer.transform(data)
    return(data)
#X[:, 1:-1]=process_missing_data(X[:, 1:-1])

#分类型数据用OneHotEncoder进行标准化
def do_OneHotEncoder(data,col_i):
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder
    ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), 
                            [col_i])], remainder='passthrough')
    data=np.array(ct.fit_transform(data))
    #data=ct.fit_transform(data).toarray()#*problem:不知为何有时上面那条不能用要用这个,有时候下面这个用不了只能用上面的
    #防止虚拟变量陷阱,去掉第一列
    data=data[:,1:]
    return(data)
#print(X[0])
#X=do_OneHotEncoder(X,0)
#X=do_OneHotEncoder(X,-1)

#分为训练集、测试集
def split_training_and_test(X,y,test_size=0.2,random_state=0):
    from sklearn.model_selection import train_test_split
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,
                                        random_state=0)
    return(X_train,X_test,y_train,y_test)

#X_train,X_test,y_train,y_test=split_training_and_test(X,y)
#print(X_train[0],X_test[0],y_train[0],y_test[0])

#归一化
def do_standrad_scaler(data):
    from sklearn.preprocessing import StandardScaler
    sc=StandardScaler()
    data=sc.fit_transform(data)
    return(sc,data)

#画图
def draw_plot(x_train,y_train):
    plt.scatter(x_train,y_train,color='red')



