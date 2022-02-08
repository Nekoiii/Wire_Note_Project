#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classification models 回归模型
"""
import sys
sys.path.append('/Users/nekosa/code/maocaoStalls/backend/real_estate/models')
sys.path.append(
    '/Users/nekosa/code/maocaoStalls/backend/real_estate/models/plot')
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import r2_score
import plot_charts
import data_preprocessing

dataset_csv='houses_data_affordable.csv'

# 数据预处理
def do_data_preprocessing(X,y):
    y = y.reshape(len(y), 1)
    X[:, 1:-1] = data_preprocessing.process_missing_data(X[:, 1:-1])
    # print(X[0])
    #*注：标签化后的x的列的结构发生了变化，之后下标别写错了！！！！
    X = data_preprocessing.do_OneHotEncoder(X, 0)
    X = data_preprocessing.do_OneHotEncoder(X, -1)
    y = data_preprocessing.do_OneHotEncoder(y, 0)
    #print(y[0])
    X_train, X_test, y_train, y_test = \
        data_preprocessing.split_training_and_test(X, y)
    print(X_train[0],X_test[0],y_train[0],y_test[0])
    #print('X_train[0]',X_train[0])
    sc_X, X_train[:, 5:] = data_preprocessing.do_standrad_scaler(
        X_train[:, 5:])
    sc_y, y_train = data_preprocessing.do_standrad_scaler(y_train)
    return( sc_X, sc_y, X_train, X_test, y_train, y_test)


def do_classification_predict(model):
    df=pd.read_csv(dataset_csv)
    X=np.hstack((df.iloc[:, 1:2].values,
                 df.iloc[:, 3:4].values,
                 df.iloc[:, 5:9].values,
                 df.iloc[:, 10:-1].values))
    y=df.iloc[:, -1].values
    #do_data_preprocessing(X,y)
    sc_X, sc_y, X_train, X_test, y_train, y_test = \
            do_data_preprocessing(X,y)

    
    #Logistic Regression
    from sklearn.linear_model import LogisticRegression
    classifier = LogisticRegression(random_state = 0)
    classifier.fit(X_train, y_train)