#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@File     : tf_test.py
@Time     : 2021/3/29 20:08
@Author   : zhaohongyu
@Email    : zhaohongyu2401@yeah.net
@Software : PyCharm
"""


from bert_serving.client import BertClient
import numpy as np


class SimilarModel:
    def __init__(self):
        # ip默认为本地模式，如果bert服务部署在其他服务器上，修改为对应ip
        #self.bert_client = BertClient(ip='192.168.x.x')
        self.bert_client = BertClient()

    def close_bert(self):
        self.bert_client .close()

    def get_sentence_vec(self,sentence):
        '''
        根据bert获取句子向量
        :param sentence:
        :return:
        '''
        return self.bert_client .encode([sentence])[0]

    def cos_similar(self,sen_a_vec, sen_b_vec):
        '''
        计算两个句子的余弦相似度
        :param sen_a_vec:
        :param sen_b_vec:
        :return:
        '''
        vector_a = np.mat(sen_a_vec)
        vector_b = np.mat(sen_b_vec)
        num = float(vector_a * vector_b.T)
        denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
        cos = num / denom
        return cos

if __name__=='__main__':
    # 从候选集condinates 中选出与sentence_a 最相近的句子
    condinates = ['为什么天空是蔚蓝色的','太空为什么是黑的？','天空怎么是蓝色的','明天去爬山如何']
    sentence_a = '天空为什么是蓝色的'
    bert_client = SimilarModel()
    max_cos_similar = 0
    most_similar_sentence = ''
    for sentence_b in condinates:
        sentence_a_vec = bert_client.get_sentence_vec(sentence_a)
        sentence_b_vec = bert_client.get_sentence_vec(sentence_b)
        cos_similar = bert_client.cos_similar(sentence_a_vec,sentence_b_vec)
        if cos_similar > max_cos_similar:
            max_cos_similar = cos_similar
            most_similar_sentence = sentence_b

    print('最相似的句子：',most_similar_sentence)
    bert_client.close_bert()
    # 为什么天空是蔚蓝色的