# -*- encoding: utf-8 -*-
"""
@File    : text_similarity.py
@Time    : 2021/3/19 14:00
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""
from tf_idf import *


def load_data(path):
    """
    :param path:  数据路径
    :return:
    获取专利数据中，分词结果，代表当前专利的文本内容描述
    """
    datas = []
    count = 0
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            count += 1
            if count == 1: continue
            line = line.strip().split('\t')
            [fieldWords, techWords, funcWords, goodsList] = line[-4:]
            words = fieldWords.split('$$') + techWords.split('$$') + funcWords.split('$$') + goodsList.split('$$')
            datas.append(words)
            if count > 100 :break
    return datas


def text_similar(doc_words):
    """
    :param doc_words: 目标数据
    :param datas:  仓库数据
    :return:
    """
    path = './../../../data/test.txt'
    datas = load_data(path)
    datas.append(' '.join(doc_words))
    word,weight = tfdif_weight(datas)

    return word,weight,datas


def main():
    text_similar(doc_words=['移动'])


if __name__ == '__main__':
    main()
