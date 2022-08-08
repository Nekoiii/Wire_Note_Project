#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自然语言处理 Natural Language Processing
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#delimiter = '\t'读取tsv文件,quoting = 3保留双引号
dataset = pd.read_csv('Restaurant_Reviews.tsv',
                      delimiter = '\t', quoting = 3)    
    
def do_natural_language_processing(model):
    #清理文字
    import re
    import nltk
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    corpus = []
    for i in range(0, 1000):
      review = re.sub('[^a-zA-Z]', ' ', #去除非字母的字符
                      dataset['Review'][i])
      review = review.lower()#转化为小写
      review = review.split()
      ps = PorterStemmer()
      all_stopwords = stopwords.words('english')
      #if ('aren\'t' in all_stopwords):
      #    print ("存在")
      all_stopwords = [e for e in all_stopwords #保留一些需要的词
                       if e not in ('not','isn\'t','aren\'t','weren\'t','won\'t','don\'t','doesn\'t','didn\'t')]
      #print(len(all_stopwords))
      review = [ps.stem(word) for word in review #转化为词干
                if not word in set(all_stopwords)]
      review = ' '.join(review)#重新用空格拼成句子
      corpus.append(review)
    print(corpus)
    
    #CountVectorizer把文本转化为向量并计算每个词的出现次数
    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer(max_features = 1500)#max_features选取出现频率最高的前n个词
    X = cv.fit_transform(corpus).toarray()
    y = dataset.iloc[:, -1].values
    
    #训练模型并预测结果
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test =train_test_split(X, y,
                             test_size = 0.20, random_state = 0)
    if model=='GaussianNB':
        from sklearn.naive_bayes import GaussianNB
        classifier = GaussianNB()
    if model=='Decision_Tree':
        from sklearn.tree import DecisionTreeClassifier
        classifier = DecisionTreeClassifier(criterion = 'entropy',
                                            random_state = 0)

    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))
    #制作混淆矩阵并评价模型
    from sklearn.metrics import confusion_matrix, accuracy_score
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    print('score:',accuracy_score(y_test, y_pred))

    return
    
do_natural_language_processing('GaussianNB')
#do_natural_language_processing('Decision_Tree')







