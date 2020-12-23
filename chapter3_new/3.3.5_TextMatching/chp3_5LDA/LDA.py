#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : books_method
# @File : LDA.py
# @Time    : 2020/8/10 9:16
# @Author  : Zhaohy

from sklearn.decomposition import LatentDirichletAllocation as lda
from sklearn.feature_extraction.text import CountVectorizer
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                max_features=1500,stop_words='english')


def lda_run(word_path,data,n_components):
    def load_words(word_path):

        word_dict = {}
        word_dict = {'':-1}
        count = 0
        with open(word_path,'r',encoding='utf8') as f :
            for line in f:
                line = line.strip()
                word_dict[count] = line
                count += 1
        return word_dict

    word_dict = load_words(word_path)


    import  pandas as pd
    import numpy as np

    data_set = []

    count = 0
    with open(data,'r',encoding='utf8') as f:
        for line in f :
            line = line.strip().split(',')


            if '-1' in line :
                line.remove('-1')
            data_set.append(' '.join(line))

            count += 1


    #print(data_set[0])

    tf = tf_vectorizer.fit_transform(data_set)
    vocs = tf_vectorizer.get_feature_names()

    tem  =  tf_vectorizer.vocabulary_
    word_bag = {}
    for i in tem :
        word_bag[tem[i]] = i

    #print(word_bag)

    model = lda(n_components=n_components)
    docs = model.fit_transform(tf)

    words = model.components_

    word_file = open('word_score','w',encoding='utf8')

    cluster=  0

    for tt_m in words:
        word_file.write('cluster = ' + str(cluster) + ' : \n')
        tt_dict = [(name, tt) for name, tt in zip(vocs, tt_m)]
        tt_dict = sorted(tt_dict, key=lambda x: x[1], reverse=True)
        # 打印权重值大于0.6的主题词
        tt_dict = [ (word_dict[int(tt_threshold[0])],tt_threshold[1]) for tt_threshold in tt_dict if tt_threshold[1] > 0.6]
        for (word,value) in tt_dict :
            word_file.write(word + '\t' + str(value) + '\n')
        cluster += 1
        word_file.write('\n\n')


    doc_key = {}

    count = 0
    for i in docs :
        key = np.where(i==max(i))
        count += 1
        if len(key[0]) > 1 :

            continue
        #doc : cluster
        c = key[0][0]
        c = int(c)
        if c in doc_key :
            doc_key[c].append(count-1)
        else:
            doc_key[c] = [count-1]

    print (doc_key)
    import json
    json.dump(doc_key,open('doc_cluster.json','w',encoding='utf8'))

#param
word_path= 'words.txt'
data = 'cluster_data'
n_components = 500
lda_run(word_path,data,n_components)

