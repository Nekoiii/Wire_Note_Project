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

houses_data_1_csv='houses_data_1.csv'

#去除空格或换行符\n
def remove_space(dataset=houses_data_1_csv):
    dataset=pd.read_csv(dataset)
    #*注: 一定要加.str才能用啊啊啊啊
    dataset['type']=dataset['type'].str.replace(' ','').str.replace('\n', '').str.replace('\r', '')
    dataset.to_csv('remove_space.csv', index=False)
    return
remove_space()

#导入dataset,返回x,y
def import_dataset(dataset=houses_data_1_csv):
    dataset=pd.read_csv(dataset)
    X=np.hstack((dataset.iloc[:, 1:4].values,dataset.iloc[:, 4:].values))
    y=dataset.iloc[:, 4].values
    print(X)
    print(y)
    return(X,y)
import_dataset()

#分类型数据用OneHotEncoder进行标准化
def do_OneHotEncoder(data,col_i):
    ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [col_i])], remainder='passthrough')
    data=np.array(ct.fit_transform(data))
    #data=ct.fit_transform(data).toarray()#problem:不知为何有时上面那条不能用要用这个,有时候下面这个用不了只能用上面的
    return(data)

do_OneHotEncoder(X,0)

#处理缺失数据,返回补全的数据
def process_missing_data(data):
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputer.fit(data)
    data=imputer.transform(data)
    return(data)













