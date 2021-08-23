# -*- encoding: utf-8 -*-
"""
@File    : tf_idf.py
@Time    : 2021/3/19 14:00
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pickle

def tfdif_weight(datas):
    #计算词频
    corpus = []

    for data in datas:
        if type(data) == str:
            corpus.append(data)
        else:
            corpus.append(' '.join(data))


    #将文本中的词语转化为词频矩阵
    vectorizer = CountVectorizer()
    transformer=TfidfTransformer()
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))
    word = vectorizer.get_feature_names()
    weight = tfidf.toarray()



    return word,weight

