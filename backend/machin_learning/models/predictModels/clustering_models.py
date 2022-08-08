#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clustering Models 聚类模型
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

#dataset_csv='houses_data_affordable_2.csv'
dataset_csv='Mall_Customers.csv'


# unfinished:X要先标准化啊！！！！

def do_clustering_predict(model):
    n_clusters=2
    df = pd.read_csv(dataset_csv)
    #X：价钱和土地面积
    #X = df.iloc[:, [4, 5]].values
    X = df.iloc[:, [3, 4]].values
    '''#X:价钱,车站距离。
    X=np.hstack((df.iloc[:, 4:5].values,
                 df.iloc[:, 10:11].values))'''
    
    if model=='K-Means_Clustering':
        #画图来判断取多少个类别
        from sklearn.cluster import KMeans
        wcss = []
        for i in range(1, 11):
            kmeans = KMeans(n_clusters = i, init = 'k-means++', 
                            random_state = 0)
            kmeans.fit(X)
            wcss.append(kmeans.inertia_)
        '''plt.plot(range(1, 11), wcss)
        plt.title('The Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.show()
        return'''
        #n_clusters 的数字根据上面的图来选择
        n_clusters = 6
        kmeans = KMeans(n_clusters = n_clusters, init = 'k-means++', 
                        random_state = 0)
        y = kmeans.fit_predict(X)
        plt.scatter(kmeans.cluster_centers_[:, 0], \
                    kmeans.cluster_centers_[:, 1], s = 100,alpha=0.5,\
                    c = 'red',zorder=2, label = 'Centroids')        
    if model=='Hierarchical_Clustering':
        #画图来判断取多少个类别
        import scipy.cluster.hierarchy as sch
        '''dendrogram = sch.dendrogram(sch.linkage(X, method = 'ward'))			
        plt.title('Dendrogram')
        plt.xlabel('X1')
        plt.ylabel('X2')
        plt.show() 
        return'''
        n_clusters = 5
        from sklearn.cluster import AgglomerativeClustering
        hc = AgglomerativeClustering(n_clusters = n_clusters, 
                                     affinity = 'euclidean', 
                                     linkage = 'ward')
        y = hc.fit_predict(X)
        
    #画图, 不同分类标记不同颜色
    color_list=['tomato','olivedrab','lightskyblue','mediumpurple','darkgrey','orange']
    if n_clusters>len(color_list):return
    #color='000000'
    for i in range(0,n_clusters):
        #color=str(int(color)+102030).rjust(6,'0')[0:6]
        '''plt.scatter(X[y == i, 0], X[y == i, 1],\
                        s = 20, zorder=1,c = '#'+color, \
                    label = 'Cluster '+str(i))'''
        plt.scatter(X[y == i, 0], X[y == i, 1],\
                        s = 20, zorder=1,c = color_list[i], \
                    label = 'Cluster '+str(i))
    plt.title('Clusters')
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.legend()
    plt.show()


#do_clustering_predict('K-Means_Clustering')
do_clustering_predict('Hierarchical_Clustering')








