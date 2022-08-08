#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关联规则学习模型 association rule learning

"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset_csv='furniture_factory.csv'

def do_association_rule_learning(model):
    #* 注:这次csv没有表头所以记得加上header=None
    df=pd.read_csv(dataset_csv,header=None)
    total_rows=len(df.axes[0])#获取总行数
    total_cols=len(df.axes[1])#获取总列数
    #print(total_rows,total_cols)
    
    transactions = []
    for i in range(0, total_rows):
    #for i in range(0, 10):
        transactions.append([str(df.values[i,j]) \
                             for j in range(0, total_cols)])

    from apyori import apriori
    rules = apriori(transactions = transactions,\
                    min_support = 0.001, min_confidence = 0.1,\
                    min_lift = 2, min_length = 2, \
                    max_length = 2)
        
    results = list(rules)
    print(results)
    
    lhs         = [tuple(result[2][0][0])[0] for result in results]
    rhs         = [tuple(result[2][0][1])[0] for result in results]
    supports    = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lifts       = [result[2][0][3] for result in results]
    if model=='Apriori':
        results_in_dateframe = pd.DataFrame(\
           list(zip(lhs, rhs, supports, confidences, lifts)),\
           columns = ['Left Hand Side', 'Right Hand Side', 'Support',\
                      'Confidence', 'Lift'])
        print(results_in_dateframe.nlargest(n = 10, columns = 'Lift'))
    if model=='Eclat':
        results_in_dateframe = pd.DataFrame(\
           list(zip(lhs, rhs, supports)),\
           columns = ['Product 1', 'Product 2', 'Support'])
        print(results_in_dateframe.nlargest(n = 10, columns = 'Support'))
    
    return


do_association_rule_learning('Apriori')
#do_association_rule_learning('Eclat')









