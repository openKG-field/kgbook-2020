#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import jieba
import re
import math
from gensim.models import word2vec
import networkx as nx
import itertools
import sys




def cut_sents(content):
    sentences = re.split(u"[。!！?？；;\s+]", content)
    sentences.append("")
    #print('org_after_split ',sentences)
    #sentences = ["".join(i) for i in zip(sentences[0::2],sentences[1::2])]
    return sentences

def cut_word(context):
    stopkey=[line.strip() for line in open('stopword.txt','r',encoding='utf8').readlines()]
    total_cutword = []
    total_content = []
    for i in context:
        words=jieba.cut(i)
        words_filter=[word for word in words if word[0] not in stopkey]
        if len(words_filter) !=0:
            total_cutword.append(words_filter)
            total_content.append(i)
    return total_cutword,total_content

def filter_model(sents,model):
    '''
    过滤词汇表中没有的单词
    '''
    total = []
    for sentence_i in sents:
        sentence_list = []
        for word_j in sentence_i:
            if word_j in model:
                sentence_list.append(word_j)
            #else:
            #    print(word_j, ' is miss')
        total.append(sentence_list)
    return total


def two_sentences_similarity(sents_1,sents_2):
    '''
    计算两个句子的相似性
    '''
    counter = 0
    for sent in sents_1:
        if sent in sents_2:
            counter +=1
    return counter / (math.log(len(sents_1) + len(sents_2)))

def cosine_similarity(vec1,vec2):
    '''
    计算两个向量之间的余弦相似度
    '''
    tx =np.array(vec1)
    ty = np.array(vec2)
    cos1 = np.sum(tx * ty)
    cos21 = np.sqrt(sum(tx ** 2))
    cos22 = np.sqrt(sum(ty ** 2))
    cosine_value = cos1/float(cos21 * cos22)
    return cosine_value

def computer_similarity_by_avg(sents_1,sents_2,model):
    '''
    对两个句子求平均词向量
    '''
    if len(sents_1) ==0 or len(sents_2) == 0:
        return 0.0
    vec1_avg = sum(model[word] for word in sents_1) / len(sents_1)
    vec2_avg = sum(model[word] for word in sents_2) / len(sents_2)
        
    similarity = cosine_similarity(vec1_avg , vec2_avg)
    return similarity
def create_graph(word_sent, model):
    '''
    :param word_sent: 二维list，里面是每一个句子的词
    :param model: 模型路径
    :return:
    '''
    num = len(word_sent)
    board = np.zeros((num, num))
    #构建一个二维数据用来存储句子与句子之间的相似度
    for i, j in itertools.product(range(num), repeat=2):
        if i != j:
            #利用词间相似度均值来衡量句子间相似度
            board[i][j] = computer_similarity_by_avg(word_sent[i], word_sent[j], model)
    # 返回 num*num，坐标为句子索引的相似度图
    return board
def sorted_sentence(graph, sentences, topK):
    '''
    :param graph: 句子间相似度的图
    :param sentences: 句子
    :param topK: 阈值
    :return:
    '''
    key_index = []
    key_sentences = []
    nx_graph = nx.from_numpy_matrix(graph)
    # 利用pagerank计算句子重要程度排序结果
    scores = nx.pagerank_numpy(nx_graph)
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    #选择最重要的topK句话
    for index, _ in sorted_scores[:topK]:
        key_index.append(index)
    new_index = sorted(key_index)
    for i in new_index:
        key_sentences.append(sentences[i])
    return key_sentences


def do(text,topK):
    list_sents = cut_sents(text)
    print ('input = ',list_sents)
    data,sentences = cut_word(list_sents)
    print ('sentences = ',sentences)
    print ('data = ', len(data),data)
    # 加载模型
    #return 0 
    model = word2vec.Word2Vec.load('./../wc.model')
    #model = word2vec.Word2Vec(data, size=256, window=5,iter=10, min_count=1, workers=4)
    sents2 = filter_model(data,model)
    print ('sents = ', sents2)
    graph = create_graph(sents2,model)
    print ('graph = ',graph)
    
    result_sentence = sorted_sentence(graph,sentences,topK)
    print ("关键句：")
    s = "   ".join(result_sentence)
    print (s)
    return s

text = u'涡轮增压是要创造一种在采取废气涡轮增压而且增压程度较高的情况下具有良好的低负荷工作稳定性和启动性能的柴油机。本发明的目的之三是要创造一种不需另外增添任何辅助设备和采取任何特殊措施而能燃用发火性能较差的燃料并能燃用多种燃料的柴油机。是要创造一种适合于装在柴油机活塞和连杆小端之间使用而且能在柴油机负荷和气缸压力的宽广变化范围内发生作用的弹性环节。本发明属于在活塞与连杆小端之间装有弹性环节从而使上死点处活塞与气缸盖之间的距离可以变化的活塞式内燃机，其中的弹性环节是一种利用油液的可压缩性工作的液体弹簧。'



topK = 2
s = do(text,topK)

