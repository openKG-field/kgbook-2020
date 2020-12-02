#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : books_method
# @File : textRank.py
# @Time    : 2020/7/31 11:39
# @Author  : Zhaohy

from jieba import  posseg as pg
import  jieba

#jieba.load_userdict('')

def data_process(path):
    '''
    :param path:
    :return:
    当前方法默认K可以接受

    将所有语料分词处理
    处理后的词按照前后顺序整理in，out 计数后的graph 作为textRank的网络结构


    '''

    doc = []
    with open(path,'r',encoding='utf8') as f :
        for line in f :
            line = line.strip()
            tem = []
            for w,f in pg.cut(line):
                if len(w) <2 or f[0] != 'n' : continue
                tem.append(w)
            doc.append(tem)

    graph = {}

    for i in doc :
        for w in range(len(i)) :
            for j in range(w+1,len(i)) :
                if w == j : continue
                if (i[w],i[j]) in graph :
                    graph[(i[w],i[j])] += 1
                else:
                    graph[(i[w],i[j])] = 1


    out_graph = {}
    in_graph = {}

    words = []

    for i in doc :
        words = words + i

    words = set(words)
    for w in words:
        in_graph[w] = []
        out_graph[w] = []
        for (in_w,out_w) in graph :
            if out_w == w :
                in_graph[w].append(in_w)
            if in_w == w :
                out_graph[w].append(out_w)
        in_graph[w] = set(in_graph[w])
        out_graph[w] = set(out_graph[w])


    return words,graph,in_graph,out_graph

def weight(graph,i,j):
    if (i,j) not in graph:
        return 0
    return  graph[(i,j)]

def textRank(words,graph,in_graph,out_graph,iter,d):
    '''

    :param words:  所有语料
    :param graph:   所有语料词
    :param in_graph:  每个词的前链接计数
    :param out_graph:  每个词的后链接计数
    :param iter:  迭代次数
    :param d: 阻尼系数
    :return:
    '''
    word_matrix = {}

    pw = [1 for i in words]
    for i in range(iter):
        print(i, ' iter is begining')
        #每一次循环
        for i in range(len(words)) :
            w = words[i]
            #输入点边权重处于当前作为输出点变权重之和作为sum
            sum = 0
            if w not in in_graph:
                sum =0
            else:
                for j in in_graph[w]:
                    wij = weight(graph,w,j)
                    tem = 0
                    if j not in out_graph :
                        tem = 0
                    else:
                        for k in out_graph[j]:
                            tem += weight(graph,j,k)
                    if tem != 0 :
                        sum = sum + float(wij)/float(tem)

            #textRank迭代公式
            pw[i] = (1-d) + d*sum*pw[i]
    re = {}
    for i in range(len(words)):
        re[words[i]] = pw[i]
    return re


'''
1. 将文章按句子切分并移除所有特殊符号

2.  计算每一个句子的向量 （word2vec or bert 等）

3.  cos 求所有句子相互距离的矩阵

4、 迭代 无监督  textRank 直至收敛， 得到 当前文章内句子重要成都排序

'''
import math
def sentence_textRank(path,threshold,in_thresh,iter,d):
    '''
        #句子部分
    将所有句子分词，并整理句子内的保留词
    将句子之间的关系按照 共献词/对数（句子词数量） 之和 计数句子之间的相关度
    设立阈值过滤低关联度句子
    将所有句子之间关系默认为 双向即 in-out 关系并存
    输出关系
    @path: 文件路径
    @threshold : 相似度最低阈值
    @in_thresh: 入链接句子最低相似度
    @iter : 迭代次数
    @d : 阻尼系数
    :return:
    '''
    sentences = {}
    sen_list = []
    with open(path,'r',encoding='utf8') as f:
        for line in f :
            line = line.strip().split('。')
            for s in line :
                if len(s) <10 or s.isspace() :continue
                tem = []
                for w, f in pg.cut(s):
                    if len(w) < 2 or f[0] != 'n': continue
                    tem.append(w)
                sentences[s] = tem
                sen_list.append(s)
    sen_sim = {}

    relations = {}
    for i in range(len(sen_list)) :
        for j in range(i,len(sen_list)) :
            a = sen_list[i]
            b = sen_list[j]
            if len(sentences[a]) == 0 or len(sentences[b]) == 0 : continue
            sim = float( len(set(sentences[a]) & set(sentences[b])) ) / ( math.log(len(sentences[a]),2)  + math.log(len(sentences[b]),2)   )
            sim =  1/(1+math.exp(-sim))
            if sim < threshold : continue
            sen_sim[(a,b)] = sim
            if a in relations :
                relations[a].append(b)
            else:
                relations[a] = [b]

            sen_sim[(b, a)] = sim
            if b in relations :
                relations[b].append(a)
            else:
                relations[b] = [a]

    pw = [1 for i in sen_list]

    for it in range(iter):
        for i in range(len(sen_list)) :
            s = sen_list[i]
            link_sum = 0
            total = 0
            if s in relations :
                link_sen = relations[s]
                ws = []
                for ls in link_sen:
                    if (s,ls) in sen_sim :

                        ws.append(sen_sim[(s,ls)])
                link_sum = sum(ws)

                for w in ws :
                    if w > in_thresh:
                        total += float(w)/float(link_sum)
                if int(total ) == 1 :
                    print(ws)

            pw[i] = (1-d) + d* total * pw[i]

    weight_dict  = {}
    count = 0
    for i in pw :
        if i == 1 :
            count += 1
    print(pw)
    print('pw = ',count)
    for i in range(len(sen_list)) :
        weight_dict[sen_list[i]] = pw[i]

    return weight_dict

weight_dict = sentence_textRank('Abstract.txt',0.5,0.7,10,0.85)


for k,v in sorted(weight_dict.items(),key=lambda k:k[1],reverse=True):
    if v == 1 :continue
    print(k,v)





def main():
    path = 'Abstract.txt'
    #通过分词等方法获得每一个词节点 进出边的权重和进出边图集合
    words,graph,in_graph,out_graph = data_process(path)

    print(graph)
    #textRank(words,graph,in_graph,out_graph,iter,d):
    re = textRank(words=words,graph=graph,in_graph=in_graph,out_graph=out_graph,iter=10,d=0.85)

    for k,v in sorted(re.items(),key=lambda k:k[1],reverse=True):
        print(k,v)


#main()
