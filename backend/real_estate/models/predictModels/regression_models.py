#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
回归模型 regression_models

"""
import sys
sys.path.append('/Users/nekosa/code/maocaoStalls/backend/real_estate/models')
import data_preprocessing
from sklearn.metrics import r2_score
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dataset_csv='houses_data_1.csv'

#数据预处理
def do_data_preprocessing():
    X,y=data_preprocessing.import_dataset(dataset_csv)
    print(X,y)
    y = y.reshape(len(y),1)
    X[:, 1:-1]=data_preprocessing.process_missing_data(X[:, 1:-1])
    print(X[0])
    X=data_preprocessing.do_OneHotEncoder(X,0)
    X=data_preprocessing.do_OneHotEncoder(X,-1)
    X_train,X_test,y_train,y_test=data_preprocessing.split_training_and_test(X,y)
    print(X_train[0],X_test[0],y_train[0],y_test[0])
    sc_X, X_train[:, 5:] = data_preprocessing.do_standrad_scaler(X_train[:, 5:])
    sc_y, y_train = data_preprocessing.do_standrad_scaler(y_train)
    return(X, y, sc_X, sc_y, X_train, X_test, y_train, y_test)

# 简单线性回归(Simple Linear Regression)
# X:土地面积
def do_simple_linear_regression():
    dataset = pd.read_csv(dataset_csv)
    X = dataset.iloc[:, 5:6].values
    y = dataset.iloc[:, 4].values

    X_train, X_test, y_train, y_test = data_preprocessing.split_training_and_test(
        X, y)
    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    print(np.concatenate((y_pred.reshape(len(y_pred), 1),
          y_test.reshape(len(y_test), 1)), 1))

    score = r2_score(y_test, y_pred)
    print('score',score)

    return( score)


#多元线性回归（Multiple Linear Regression）
#problem: y_pred出现了负数，不知是哪出了问题？？？
def do_multiple_linear_regression():
    X, y, sc_X, sc_y, X_train, X_test, y_train, y_test = do_data_preprocessing()

    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    #X_test[:, 5:] = sc_X.transform(X_test[:, 5:])
    #y_pred = sc_y.inverse_transform(regressor.predict(X_test))
    np.set_printoptions(precision=2)
    print(np.concatenate((y_pred.reshape(len(y_pred), 1),
          y_test.reshape(len(y_test), 1)), 1))

    score = r2_score(y_test, y_pred)
    print('score',score)
    
    return(score)


#多项式回归（Polynomial Regression） 
#problem: y_pred出现了负数，不知是哪出了问题？？？
def do_polynomial_regression():
    X, y, sc_X, sc_y, X_train, X_test, y_train, y_test = do_data_preprocessing()

    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures
    # degree太高了会死机,千万别试!!!!
    poly_reg = PolynomialFeatures(degree=1)
    X_poly = poly_reg.fit_transform(X_train)
    regressor = LinearRegression()
    regressor.fit(X_poly, y_train)

    X_test[:, 5:] = sc_X.transform(X_test[:, 5:])
    print(X_test[0])
    y_pred = sc_y.inverse_transform(
        regressor.predict(poly_reg.transform(X_test)))
    np.set_printoptions(precision=2)
    print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

    score = r2_score(y_test, y_pred)
    print(score)

    return(score)


#支持向量回归 (SVR) (Support Vector Regression)'''
def do_support_vector_regression():
    X, y, sc_X, sc_y, X_train, X_test, y_train, y_test = do_data_preprocessing()

    from sklearn.svm import SVR
    regressor = SVR(kernel='rbf')
    regressor.fit(X_train, y_train.ravel())#*记得加.ravel()

    X_test[:, 5:] = sc_X.transform(X_test[:, 5:])
    y_pred = sc_y.inverse_transform(regressor.predict(X_test))
    np.set_printoptions(precision=2)
    print(np.concatenate((y_pred.reshape(len(y_pred), 1),
          y_test.reshape(len(y_test), 1)), 1))

    score = r2_score(y_test, y_pred)
    print(score)

    return(score)


#决策树回归( Decision Tree Regression）'''
# X:土地面积
def do_decision_tree_regression():
    dataset = pd.read_csv(dataset_csv)
    X = dataset.iloc[:, 5:6].values
    y = dataset.iloc[:, 4].values


    from sklearn.tree import DecisionTreeRegressor
    regressor = DecisionTreeRegressor(random_state=0)
    regressor.fit(X, y)

    X_train, X_test, y_train, y_test = data_preprocessing.split_training_and_test(
        X, y)
    y_pred = regressor.predict(X_test)
    print(np.concatenate((y_pred.reshape(len(y_pred), 1),
          y_test.reshape(len(y_test), 1)), 1))
    '''X_grid = np.arange(min(X), max(X), 0.01)
    X_grid = X_grid.reshape((len(X_grid), 1))
    plt.scatter(X, y, color = 'red')
    plt.plot(X_grid, regressor.predict(X_grid), color = 'blue')
    plt.title('Truth or Bluff (Decision Tree Regression)')
    plt.xlabel('Date')
    plt.ylabel('Newly Confirmed')
    plt.show()'''
    score=r2_score(y_test, y_pred)
    print(score)

    return(score)


#随机森林回归（Random Forest Regression）'''
def do_random_forest_regression():
    X, y, sc_X, sc_y, X_train, X_test, y_train, y_test = do_data_preprocessing()

    from sklearn.ensemble import RandomForestRegressor
    regressor = RandomForestRegressor(
        n_estimators=5, random_state=0)  # n_estimators是森林里树的棵数
    regressor.fit(X, y.ravel())

    y_pred = regressor.predict(X_test)
    print(np.concatenate((y_pred.reshape(len(y_pred), 1),
          y_test.reshape(len(y_test), 1)), 1))

    score = r2_score(y_test, y_pred)
    print(score)

    return(score)
