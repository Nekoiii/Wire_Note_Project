#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classification models 分类模型
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
    #K-Nearest Neighbors (K-NN)
    if model=='K-NN':
        from sklearn.neighbors import KNeighborsClassifier
        classifier = KNeighborsClassifier(n_neighbors = 5, 
                                          metric = 'minkowski', 
                                          p = 2)
    #Support Vector Machine (SVM)
    if model=='SVM':
        from sklearn.svm import SVC
        classifier = SVC(kernel = 'linear', random_state = 0)
    #SVM (RBF Kernel)
    if model=='SVM_RBF':
        from sklearn.svm import SVC
        classifier = SVC(kernel = 'rbf', random_state = 0)
    #Naive Bayes 朴素贝叶斯
    if model=='Naive_Bayes':
        from sklearn.naive_bayes import GaussianNB
        classifier = GaussianNB()
    #Decision Tree Classification
    if model=='Decision_Tree':
        from sklearn.tree import DecisionTreeClassifier
        classifier = DecisionTreeClassifier(criterion = 'entropy',
                                            random_state = 0)
    #Random Forest Classification
    if model=='Random_Forest':
        from sklearn.ensemble import RandomForestClassifier
        classifier = RandomForestClassifier(n_estimators = 10,
                                            criterion = 'entropy',
                                            random_state = 0)

    classifier.fit(X_train, y_train)
    X_test = sc_X.transform(X_test)
    y_pred = classifier.predict(X_test)
    #print(np.concatenate((y_pred.reshape(len(y_pred), 1),
    #      y_test.reshape(len(y_test), 1)), 1))
        
    #混淆矩阵、评分
    from sklearn.metrics import confusion_matrix, accuracy_score
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    score=accuracy_score(y_test, y_pred)
    print(score)
    
    #画图
    from matplotlib.colors import ListedColormap
    X_set_1, y_set_1 = sc_X.inverse_transform(X_train), y_train
    X_set_2, y_set_2 = sc_X.inverse_transform(X_test), y_test
    x_start=(X_set_1[:, 0].min() \
        if X_set_1[:, 0].min()<X_set_2[:, 0].min() \
            else X_set_2[:, 0].min())-10
    x_stop=(X_set_1[:, 0].max() \
        if X_set_1[:, 0].max()>X_set_2[:, 0].max() \
            else X_set_2[:, 0].max())+10
    x_step = 0.25
    y_start=(X_set_1[:, 1].min() \
        if X_set_1[:, 1].min()<X_set_2[:, 1].min() \
            else X_set_2[:, 1].min())-10
    y_stop=(X_set_1[:, 1].max() \
        if X_set_1[:, 1].max()>X_set_2[:, 1].max() \
            else X_set_2[:, 1].max())+10
    y_step = 0.25
        
    X1, X2 = np.meshgrid(np.arange(x_start, x_stop, x_step),
                         np.arange(y_start, y_stop, y_step))
    #print('X_set_1',X_set_1[0])
    #print('y_set_1',y_set_1)
    #画训练集
    plt.figure()
    plt.subplot(1,2,1)#把两个图画在一个窗口
    plt.contourf(X1, X2, classifier.predict(sc_X.transform(
        np.array([X1.ravel(), X2.ravel()]).T)).reshape(X1.shape),
                 alpha = 0.75, cmap = ListedColormap(('red', 'green')))
    plt.xlim(X1.min(), X1.max())
    plt.ylim(X2.min(), X2.max())
    #y_set_1经过np.unique()去重后就只剩跟种类数一样长度的数据
    for i, j in enumerate(np.unique(y_set_1)):
        #print('y_set_1---2',y_set_1)
        #print('i:',i,'j:',j)
        plt.scatter(X_set_1[y_set_1 == j, 0], X_set_1[y_set_1 == j, 1],
                    color = ListedColormap(('red', 'green'))(i),
                    label = j)
    plt.title('Classification (Training set)')
    plt.xlabel('Land Area')
    plt.ylabel('Station Dist')
    plt.legend()
    plt.show()
    
    #画测试集
    #plt.figure() #把两个图画在不同窗口
    plt.subplot(1,2,2)
    plt.contourf(X1, X2, classifier.predict(sc_X.transform(np.array(
        [X1.ravel(), X2.ravel()]).T)).reshape(X1.shape),
                 alpha = 0.75, cmap = ListedColormap(('red', 'green')))
    plt.xlim(X1.min(), X1.max())
    plt.ylim(X2.min(), X2.max())
    for i, j in enumerate(np.unique(y_set_2)):
        plt.scatter(X_set_2[y_set_2 == j, 0], X_set_2[y_set_2 == j, 1],
                    color = ListedColormap(('red', 'green'))(i),
                    label = j)
    plt.title('Classification (Test set)')
    plt.xlabel('Land Area')
    plt.ylabel('Station Dist')
    plt.legend()
    plt.show()
    

do_classification_predict('Logistic_Regression')       
#do_classification_predict('K-NN')       
#do_classification_predict('SVM')       
#do_classification_predict('SVM_RBF')       
#do_classification_predict('Naive_Bayes')       
#do_classification_predict('Decision_Tree')       
#do_classification_predict('Random_Forest')       
           
        
        
        
        