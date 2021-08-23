# -*- encoding: utf-8 -*-
"""
@File    : fast_text.py
@Time    : 2021/3/20 12:50
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""

from jiebaCutPackage import jiebaInterface
import pandas as pd
import fasttext

def load_data(train_path):
    '''
    :param train_path: 训练数据路径
    将其处理成带有  __label__ 格式的 fasttext 的接受数据
    :return:
    '''
    o = open(train_path.replace('cnews','fasttext') , 'w',encoding='utf8')
    with open(train_path,'r',encoding='utf8') as f :
        for line in f :
            line = line.strip().split(' ')
            label = '__label__' + line[0]
            words = []
            content = jiebaInterface.jiebaCut(line[1]).split(',')
            for i in content :
                w = i.split('_')[0]
                words.append(w)
            cur = label + ' ' + ','.join(words) + '\n'
            o.write(cur)

train_path = 'cnews.train.txt'
load_data(train_path)

test_path = 'cnews.test.txt'
load_data(test_path)

def method(train_path,test_path):
    '''

    :param train_path:  训练数据路径
    :param test_path:   测试数据路径
    :return:
    '''
    def print_results(N, p, r):
        '''
        :param N:  数量
        :param p:  准确
        :param r:  找回
        :return:
        '''
        print("N\t" + str(N))
        print("P@{}\t{:.3f}".format(1, p))
        print("R@{}\t{:.3f}".format(1, r))
    model = fasttext.train_supervised(input=train_path)
    #print(model.test(test_path))
    print_results(*model.test(test_path))

train_path = 'fasttext.train.txt'
test_path = 'fasttext.test.txt'


method(train_path,test_path)