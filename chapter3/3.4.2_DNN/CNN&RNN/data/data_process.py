# -*- encoding: utf-8 -*-
"""
@File    : data_process.py
@Time    : 2021/3/20 13:32
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""

from jiebaCutPackage import jiebaInterface

def load_data(path):
    o = open(path.replace('cnews','modify'),'w',encoding='utf8')
    with open(path,'r',encoding='utf8') as f :
        for line in f :
            line = line.strip().split()
            if len(line) != 2 : continue
            [key,content] = line
            words = jiebaInterface.jiebaCut(content).split(',')
            wordList = []
            for w in words :
                word = w.split('_')[0]
                wordList.append(word)
            o.write(key + ' ' + ','.join(wordList) + '\n')
    return  0


path = 'cnews.val.txt'
load_data(path)
path = 'cnews.train.txt'
load_data(path)
path = 'cnews.test.txt'
load_data(path)


