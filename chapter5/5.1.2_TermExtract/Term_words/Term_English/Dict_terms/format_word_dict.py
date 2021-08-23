#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@File     : format_word_dict.py
@Time     : 2021/3/24 15:44
@Author   : zhaohongyu
@Email    : zhaohongyu2401@yeah.net
@Software : PyCharm
"""


import json


def readEnWord(path):
    d = {}
    #o = open('singleWord.txt','w')
    f = open(path,'r',encoding='utf8')
    longest = 0
    for line in f:
        line = line.replace('\r','').replace('\n','').strip()
        if '-' not in line:
            continue
        else:
            line = line.replace('-',' ')
            cur = len(line.split())
            if cur > longest:
                longest = cur
            d[line] = 1

    return d,longest




path = 'Dictresult2018.txt'

enPathDict,longest = readEnWord(path)
en = {'enPathDict':enPathDict,'longest':longest}
json.dump(en,open('en_Path_Dict.json','w'))

