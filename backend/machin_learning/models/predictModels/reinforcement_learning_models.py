#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强化学习模型 reinforcement learning

"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import random

dataset_csv='houses_marks_record.csv'

def do_reinforcement_learning(model):
    dataset=pd.read_csv(dataset_csv)
    N=len(dataset.axes[0]) #模拟的点击数(可设为小于总记录数长度的其他数值)
    #N=5000
    d=len(dataset.axes[1]) #种类数
    houses_selected = []
    
    if model=='UCB':
        numbers_of_selections = [0] * d #每个房子被点击的次数
        sums_of_rewards = [0] * d #每个房子被收藏的次数
        total_reward = 0
        for n in range(0, N):
            house = 0
            max_upper_bound = 0
            for i in range(0, d):
                if (numbers_of_selections[i] > 0):#排除分母0
                    average_reward = sums_of_rewards[i] / numbers_of_selections[i]
                    delta_i = math.sqrt(3/2 * math.log(n + 1) / numbers_of_selections[i])
                    upper_bound = average_reward + delta_i
                else:
                    upper_bound = 1e400 #随便设置的一个巨大数字
                if upper_bound > max_upper_bound:
                    max_upper_bound = upper_bound
                    house = i
            houses_selected.append(house)
            numbers_of_selections[house] = numbers_of_selections[house] + 1
            reward = dataset.values[n, house]
            sums_of_rewards[house] = sums_of_rewards[house] + reward
            total_reward = total_reward + reward
    
    if model=='Thompson_Sampling':
        numbers_of_rewards_1 = [0] * d
        numbers_of_rewards_0 = [0] * d
        total_reward = 0
        for n in range(0, N):
            house = 0
            max_random = 0
            for i in range(0, d):
                random_beta = random.betavariate\
                    (numbers_of_rewards_1[i] + 1, numbers_of_rewards_0[i] + 1)
                if random_beta > max_random:
                    max_random = random_beta
                    house = i
            houses_selected.append(house)
            reward = dataset.values[n, house]
            if reward == 1:
                numbers_of_rewards_1[house] = numbers_of_rewards_1[house] + 1
            else:
                numbers_of_rewards_0[house] = numbers_of_rewards_0[house] + 1
            total_reward = total_reward + reward
        
    plt.hist(houses_selected)
    plt.title('Histogram of houses marked')
    plt.xlabel('Houses')
    plt.ylabel('Number of times each house was marked')
    plt.show()

    return


#do_reinforcement_learning('UCB')
do_reinforcement_learning('Thompson_Sampling')









