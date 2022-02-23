#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
回归模型 regression_models

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

dataset_csv = 'houses_data_1.csv'

# 数据预处理
def do_data_preprocessing(X,y):
    y = y.reshape(len(y), 1)
    X[:, 1:-1] = data_preprocessing.process_missing_data(X[:, 1:-1])
    # print(X[0])
    #*注：标签化后的x的列的结构发生了变化，之后下标别写错了！！！！
    X = data_preprocessing.do_OneHotEncoder(X, 0)
    X = data_preprocessing.do_OneHotEncoder(X, -1)
    X_train, X_test, y_train, y_test = \
        data_preprocessing.split_training_and_test(X, y)
    # print(X_train[0],X_test[0],y_train[0],y_test[0])
    # *注:这里其实概率模型（树形模型）不需要归一化，只是为了方便一起用了
    print('X_train[0]',X_train[0])
    sc_X, X_train[:, 5:] = data_preprocessing.do_standrad_scaler(
        X_train[:, 5:])
    sc_y, y_train = data_preprocessing.do_standrad_scaler(y_train)
    return( sc_X, sc_y, X_train, X_test, y_train, y_test)

def do_regression_predict(model):
    df=pd.read_csv(dataset_csv)
    #*注:X中就算只取单列也不能不能[:, 1],一定要[:, 1:2]!!!!
    X=np.hstack((df.iloc[:, 1:2].values,
                 df.iloc[:, 3:4].values,
                 df.iloc[:, 5:9].values,
                 df.iloc[:, 10:].values))
    y=df.iloc[:, 4].values
    #type(X)

    sc_X, sc_y, X_train, X_test, y_train, y_test = \
            do_data_preprocessing(X,y)
    # 简单线性回归(Simple Linear Regression)
    # X:土地面积
    if model=='SimpleLinearRegression':
        X = df.iloc[:, 5:6].values
        y = df.iloc[:, 4].values
        X_train, X_test, y_train, y_test = \
            data_preprocessing.split_training_and_test(X, y)
        from sklearn.linear_model import LinearRegression
        regressor = LinearRegression()
        regressor.fit(X_train, y_train)
        y_pred = regressor.predict(X_test)
        print(np.concatenate((y_pred.reshape(len(y_pred), 1),
              y_test.reshape(len(y_test), 1)), 1))
        score = r2_score(y_test, y_pred)
        print('score', score)
        plot_charts.plot_predict_result(y_test, y_pred, score)
        return(y_test, y_pred, score)
    # 多元线性回归（Multiple Linear Regression）
    if model=='MultipleLinearRegression':
        from sklearn.linear_model import LinearRegression
        regressor = LinearRegression()
    # 多项式回归（Polynomial Regression）
    # problem: y_pred出现了负数，不知是哪出了问题？？？
    if model=='PolynomialRegression':
        from sklearn.linear_model import LinearRegression
        from sklearn.preprocessing import PolynomialFeatures
        # degree太高了会死机,千万别试!!!!
        poly_reg = PolynomialFeatures(degree=2)
        X_poly = poly_reg.fit_transform(X_train)
        regressor = LinearRegression()
        regressor.fit(X_poly, y_train)
        X_test[:, 5:] = sc_X.transform(X_test[:, 5:])
        y_pred = sc_y.inverse_transform(
            regressor.predict(poly_reg.transform(X_test)))
        np.set_printoptions(precision=2)
        print(np.concatenate((y_pred.reshape(len(y_pred), 1),
              y_test.reshape(len(y_test), 1)), 1))
        score = r2_score(y_test, y_pred)
        print(score)
        plot_charts.plot_predict_result(y_test, y_pred, score)
        return(y_test, y_pred, score)
    
    # 支持向量回归 (SVR) (Support Vector Regression)
    if model=='SupportVectorRegression':
        from sklearn.svm import SVR
        regressor = SVR(kernel='rbf')
        #regressor.fit(X_train, y_train.ravel())  # *记得加.ravel()
    # 决策树回归(Decision Tree Regression）'''
    # X:土地面积
    if model=='DecisionTreeRegression':
        from sklearn.tree import DecisionTreeRegressor
        regressor = DecisionTreeRegressor(random_state=0)
    # 随机森林回归（Random Forest Regression）
    if model=='RandomForestRegression':
        from sklearn.ensemble import RandomForestRegressor
        regressor = RandomForestRegressor(
            n_estimators=5, random_state=0)  # n_estimators是森林里树的棵数
        #regressor.fit(X, y.ravel())
        
    regressor.fit(X_train, y_train)
    #y_pred = regressor.predict(X_test)
    X_test[:, 5:] = sc_X.transform(X_test[:, 5:])
    y_pred = sc_y.inverse_transform(regressor.predict(X_test))
    np.set_printoptions(precision=2)
    #print(np.concatenate((y_pred.reshape(len(y_pred), 1),
    #      y_test.reshape(len(y_test), 1)), 1))

    score = r2_score(y_test, y_pred)
    #print('score', score)
    plot_charts.plot_predict_result(y_test, y_pred, score)

    return(y_test, y_pred, score)
do_regression_predict('SimpleLinearRegression')
do_regression_predict('MultipleLinearRegression')
do_regression_predict('PolynomialRegression')
do_regression_predict('SupportVectorRegression')
do_regression_predict('DecisionTreeRegression')
do_regression_predict('RandomForestRegression')


    
