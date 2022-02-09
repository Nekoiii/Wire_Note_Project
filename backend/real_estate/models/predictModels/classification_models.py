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
    X[:, :] = data_preprocessing.process_missing_data(X[:, :])
    X_train, X_test, y_train, y_test = \
        data_preprocessing.split_training_and_test(X, y)
    print(X_train[0],X_test[0],y_train[0],y_test[0])
    sc_X, X_train=data_preprocessing.do_standrad_scaler(X_train)
    return( sc_X,  X_train, X_test, y_train, y_test)


def do_classification_predict(model):
    df=pd.read_csv(dataset_csv)
    #X:土地面积,车站距离。y:是否超预算
    X=np.hstack((df.iloc[:, 5:6].values,
                 df.iloc[:, 10:11].values))
    y=df.iloc[:, -1].values
    sc_X, X_train, X_test, y_train, y_test = \
            do_data_preprocessing(X,y)

    #Logistic Regression
    if model=='Logistic_Regression':
        from sklearn.linear_model import LogisticRegression
        classifier = LogisticRegression(random_state = 0)
    classifier.fit(X_train, y_train)
    X_test = sc_X.transform(X_test)
    y_pred = classifier.predict(X_test)
    #print(np.concatenate((y_pred.reshape(len(y_pred), 1),
    #      y_test.reshape(len(y_test), 1)), 1))
    from sklearn.metrics import confusion_matrix, accuracy_score
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    accuracy_score(y_test, y_pred)
    
    from matplotlib.colors import ListedColormap
    #X_set, y_set = sc_X.inverse_transform(X_train), y_train
    X_set, y_set = sc_X.inverse_transform(X_test), y_test
    X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 10, stop = X_set[:, 0].max() + 10, step = 0.25),
                         np.arange(start = X_set[:, 1].min() - 10, stop = X_set[:, 1].max() + 10, step = 0.25))
    plt.contourf(X1, X2, classifier.predict(sc_X.transform(np.array([X1.ravel(), X2.ravel()]).T)).reshape(X1.shape),
                 alpha = 0.75, cmap = ListedColormap(('red', 'green')))
    plt.xlim(X1.min(), X1.max())
    plt.ylim(X2.min(), X2.max())
    for i, j in enumerate(np.unique(y_set)):
        plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1], color = ListedColormap(('red', 'green'))(i), label = j)
    #plt.title('Logistic Regression (Training set)')
    plt.title('Logistic Regression (Test set)')
    plt.xlabel('Land Area')
    plt.ylabel('Station Dist')
    plt.legend()
    plt.show()
    

do_classification_predict('Logistic_Regression')       
        
        
        
        
        