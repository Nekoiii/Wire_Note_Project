#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关联规则学习模型 association rule learning

"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset_csv='furniture_factory.csv'
#dataset_csv='Market_Basket_Optimisation.csv'

def do_association_rule_learning(model):
    #* 注:这次csv没有表头所以记得加上header=None
    df=pd.read_csv(dataset_csv,header=None)
    total_rows=len(df.axes[0])#获取总行数
    total_cols=len(df.axes[1])#获取总列数
    #print(total_rows,total_cols)
    
    '''old_transactions = []
    for i in range(0, 10):
        old_transactions.append([str(df.values[i,j])for j in range(0, 18)])

    print('a-1',old_transactions[0])
    transactions=[]
    for a_list in old_transactions:#去掉空值
        new_list=list(filter(lambda x : x != 'nan', a_list))
        transactions.append(new_list)
    print('a-2',transactions[0])'''
    
    transactions = []
    for i in range(0, 100):
        transactions.append([str(df.values[i,j]) for j in range(0, 18)])

    from apyori import apriori
    rules = apriori(transactions = transactions,\
                    min_support = 0.003, min_confidence = 0.2,\
                    min_lift = 3, min_length = 2, \
                    max_length = 2)
        
    #print(rules)
    results = list(rules)
    results
    print(results)
    
    return

do_association_rule_learning('Apriori')