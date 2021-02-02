# -*- encoding: utf-8 -*-
"""
@File    : w2v_rerank_by_used.py
@Time    : 2021/1/25 11:29
@Author  : Zhaohy
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""

from gensim.models import word2vec

currDir = './'
model_cn=word2vec.Word2Vec.load(currDir + "/wc.model")

model_en = word2vec.Word2Vec.load(currDir + '/Word2vecEnglish.model')
import json

word_fre = json.load(open('word_fre.json','r',encoding='utf8'))

def suggestion(words,N,language=1):
    '''
    @words : 输入的待推荐词  list
    @ N : top N 相似
    @ language :  推荐语言主题 1 = CN , else = EN
    '''

    if language == 1 :
        model = model_cn
    else:
        model = model_en

    for i in words :

        similar_words = model.most_similar(i,'',N)
        his_words = []
        if i in word_fre :
            his_words = word_fre[i]

