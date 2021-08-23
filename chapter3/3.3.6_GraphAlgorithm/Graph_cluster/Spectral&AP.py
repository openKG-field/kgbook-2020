#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@File     : graph_metho.py
@Time     : 2021/3/25 16:13
@Author   : zhaohongyu
@Email    : zhaohongyu2401@yeah.net
@Software : PyCharm
"""

# 近邻传播
from sklearn.cluster import AffinityPropagation


def ap_method(x, y=None):
    y_pred = AffinityPropagation(preference=-50).fit_predict(x)

    #("Calinski-Harabasz Score", metrics.calinski_harabaz_score(x, y_pred))

    return y_pred


# 谱聚类
from sklearn.cluster import SpectralClustering


def sc_method(x, n=2, y=None):
    y_pred = SpectralClustering(n_clusters=n, gamma=0.1).fit_predict(x)

    #print("Calinski-Harabasz Score", metrics.calinski_harabaz_score(x, y_pred))
    return y_pred


# sample data
from sklearn import metrics
from sklearn.datasets import make_blobs

centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=300, centers=centers, cluster_std=0.5,
                            random_state=0)

import numpy as np
# 相似度矩阵
import math
from sklearn.metrics.pairwise import cosine_similarity


def data2metrix(path):
    '''
    :param path:  数据路径
    :return: 相似度矩阵

    data :  0_label 1-200位 doc_1_pmean_vec 201-400位 doc_2_pmean

    '''

    docs = {}
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            line = line.strip().split('\t')
            label = line[0]
            vec1 = ','.join(line[1:201])
            vec2 = ','.join(line[201:])
            if vec1 not in docs:
                docs[vec1] = 1
            if vec2 not in docs:
                docs[vec2] = 1

    # build matrix , 变索引是 遍历docs的顺序

    doc_arr = []
    for i in docs:
        i = i.split(',')
        doc_arr.append([float(j) for j in i])

    # sample data

    doc_arr = doc_arr[:50]


    m = cosine_similarity(doc_arr)

    return m


path = 'data_for_dssm.txt'
X = data2metrix(path)
ap_result = ap_method(X)
sc_result = sc_method(X)

print(ap_result)

print(sc_result)