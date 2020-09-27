#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : books_method
# @File : data_process.py
# @Time    : 2020/9/1 17:40
# @Author  : Zhaohy


def load_data():
    words_dict = {}
    words_file = open('words.txt','w',encoding='utf8')
    data  = open('cluster_data','w',encoding='utf8')
    count = 0
    with open('./../noman_features.txt','r',encoding='utf8') as f:
        for line in f :
            line = line.strip().split()
            words = line[6].split(',')
            for w in words :
                if w in words_dict : continue
                else:
                    words_dict[w] = count
                    count += 1

            words = [str(words_dict[w]) for w in words]
            data.write(','.join(words) + '\n')

    for k,v in sorted(words_dict.items(),key=lambda k:k[1],reverse=False):
        words_file.write(k+'\n')





load_data()