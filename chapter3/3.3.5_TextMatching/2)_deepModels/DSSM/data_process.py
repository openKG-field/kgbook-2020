# -*- encoding: utf-8 -*-
"""
@File    : data_process.py
@Time    : 2021/3/20 17:10
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""
from jiebaCutPackage import jiebaInterface

import xmlrpc.client


def load_data(path):
    count = 0
    tar = [2, 5]
    o = open(path.replace('result', 'word_compare'), 'w', encoding='utf8')
    neg_list = []
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            count += 1

            line = line.strip().split('\t')
            tar_content = [line[2], line[5]]

            result = []
            for c in tar_content:
                words = jiebaInterface.jiebaCut(c).split(',')
                wordList = []
                for w in words:
                    w = w.split('_')[0]
                    wordList.append(w)
                wordList = ','.join(wordList)
                if count % 5 is 0 and tar_content.index(c) == 0:
                    neg_list.append(wordList)
                result.append(wordList)
            result = '\t'.join(result)
            o.write('1' + '\t' + result + '\n')
    for i in neg_list:
        for j in neg_list:
            if i != j:
                o.write('0' + '\t' + i + '\t' + j + '\n')


# path = 'E:/book_related_method/20210319/kgbook-2020/chapter3_new/3.3.5_TextMatching/chp3_5DSSM/result.txt'
# load_data(path)

proxy = xmlrpc.client.ServerProxy("http://103.105.201.54:30004")

from gensim.models import word2vec

model = word2vec.Word2Vec.load('./../wc.model')


def pmean(c1):
    c1_vec = []
    count = 0
    for w in c1.split(','):
        try:
            v = model[w].tolist()
        except:
            continue
        finally:
            count += 1
            if c1_vec == []:
                c1_vec = v
            else:
                c1_vec = [c1_vec[i] + v[i] for i in range(len(v))]
    c1_vec = [str(float(i) / float(count)) for i in c1_vec]
    return c1_vec


def data_for_dssm(path):
    o = open(path.replace('word_compare', 'data_for_dssm'), 'w', encoding='utf8')
    count = 0
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            [label, c1, c2] = line.strip().split('\t')
            c1_vec = pmean(c1)
            c2_vec = pmean(c2)
            count += 1
            if count % 100 is 0:
                print(count)
            # print(len(c1_vec))
            o.write(label + '\t' + '\t'.join(c1_vec) + '\t'.join(c2_vec) + '\n')


path = 'word_compare.txt'

data_for_dssm(path)
