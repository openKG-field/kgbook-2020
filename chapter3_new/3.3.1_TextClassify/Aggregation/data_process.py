#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : books_method
# @File : data_process.py
# @Time    : 2020/9/4 17:40
# @Author  : Zhaohy



def procee(path):

    count = 0

    train = open('train_data.txt','w',encoding='utf8')
    test = open('test_data.txt','w',encoding='utf8')
    with open(path,'r',encoding='utf8') as f:
        for line in f :

            count += 1
            if count < 22000 :
                train.write(line)
            else:
                test.write(line)

    print(count)


path = 'model_data.txt'
procee(path)