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

dataset_csv='houses_data_affordable_2.csv'

# 数据预处理
def do_data_preprocessing(X,y):
    #y = y.reshape(len(y), 1)
    X[:, :] = data_preprocessing.process_missing_data(X[:, :])
    # print(X[0])
    #*注：标签化后的x的列的结构发生了变化，之后下标别写错了！！！！
    '''X = data_preprocessing.do_OneHotEncoder(X, 0)
    X = data_preprocessing.do_OneHotEncoder(X, -1)'''
    X_train, X_test, y_train, y_test = \
        data_preprocessing.split_training_and_test(X, y)
    print(X_train[0],X_test[0],y_train[0],y_test[0])
    #print('X_train[0]',X_train[0])
    '''sc_X, X_train[:, 5:] = data_preprocessing.do_standrad_scaler(
        X_train[:, 5:])'''
    sc_X, X_train=data_preprocessing.do_standrad_scaler(X_train)
    return( sc_X,  X_train, X_test, y_train, y_test)


def do_classification_predict(model):
    df=pd.read_csv(dataset_csv)
    '''X=np.hstack((df.iloc[:, 1:2].values,
                 df.iloc[:, 3:4].values,
                 df.iloc[:, 5:9].values,
                 df.iloc[:, 10:-1].values))'''
    X=np.hstack((df.iloc[:, 3:4].values,
                 df.iloc[:, 5:6].values))
    y=df.iloc[:, -1].values
    #do_data_preprocessing(X,y)
    sc_X, X_train, X_test, y_train, y_test = \
            do_data_preprocessing(X,y)

    #Logistic Regression
    if model=='Logistic_Regression':
        from sklearn.linear_model import LogisticRegression
        classifier = LogisticRegression(random_state = 0)
    classifier.fit(X_train, y_train)
    #classifier.fit(X_train, y_train.ravel())
    '''X_test[:, 5:] = sc_X.transform(X_test[:, 5:])'''
    X_test = sc_X.transform(X_test)
    y_pred = classifier.predict(X_test)
    #print(np.concatenate((y_pred.reshape(len(y_pred), 1),
    #      y_test.reshape(len(y_test), 1)), 1))
    from sklearn.metrics import confusion_matrix, accuracy_score
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    accuracy_score(y_test, y_pred)
    
    from matplotlib.colors import ListedColormap
    X_set, y_set = sc_X.inverse_transform(X_train), y_train
    print('y_set',y_set[0])
    #return
    X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 10, stop = X_set[:, 0].max() + 10, step = 0.25),
                         np.arange(start = X_set[:, 1].min() - 10, stop = X_set[:, 1].max() + 10, step = 0.25))
    plt.contourf(X1, X2, classifier.predict(sc_X.transform(np.array([X1.ravel(), X2.ravel()]).T)).reshape(X1.shape),
                 alpha = 0.75, cmap = ListedColormap(('red', 'green')))
    plt.xlim(X1.min(), X1.max())
    plt.ylim(X2.min(), X2.max())
    for i, j in enumerate(np.unique(y_set)):
        plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1], color = ListedColormap(('red', 'green'))(i), label = j)
    plt.title('Logistic Regression (Training set)')
    plt.xlabel('Age')
    plt.ylabel('Estimated Salary')
    plt.legend()
    plt.show()
    
    '''from matplotlib.colors import ListedColormap
    X_set, y_set = sc_X.inverse_transform(X_test), y_test
    X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 10, stop = X_set[:, 0].max() + 10, step = 0.25),
                         np.arange(start = X_set[:, 1].min() - 1000, stop = X_set[:, 1].max() + 1000, step = 0.25))
    plt.contourf(X1, X2, classifier.predict(sc_X.transform(np.array([X1.ravel(), X2.ravel()]).T)).reshape(X1.shape),
                 alpha = 0.75, cmap = ListedColormap(('red', 'green')))
    plt.xlim(X1.min(), X1.max())
    plt.ylim(X2.min(), X2.max())
    print('X_set',X_set[0])
    print('y_set',y_set[0])
    for i, j in enumerate(np.unique(y_set)):
        print('X_set[y_set == j, 0]',X_set[y_set == j, 0])
        plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1], 
                    color = ListedColormap(('red', 'green'))(i), label = j)
    plt.title('Logistic Regression (Test set)')
    plt.xlabel('Age')
    plt.ylabel('Estimated Salary')
    plt.legend()
    plt.show()'''

do_classification_predict('Logistic_Regression')       
        
        
        
        
        