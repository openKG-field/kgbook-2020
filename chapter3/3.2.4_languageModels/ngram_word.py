#!/usr/bin/env python
# _*_coding:utf-8_*_
"""
@File    : ngram_word.py
@Time    : 2021/3/19 10:19
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""
from math import sqrt
import time



def ngram(typeWord, compareWord, n):
    if not type(typeWord) == str or not type(compareWord) == str:
        return -1
    ngram_value = 0
    intersection_value = 0
    tlength = len(typeWord)
    clength = len(compareWord)
    tMap = {'start': 0}
    tlist = list()
    clist = list()
    combineT = 0
    combineC = 0
    # combine the each leaf of typeword and save them into a map for the next comparison
    for i in range(tlength // n):
        currentT = typeWord[i * n:(i + 1) * n]
        tlist.append(currentT)
    for i in range(len(tlist)):
        if i + 1 < len(tlist):
            temT = tlist[i] + tlist[i + 1]
            combineT = combineT + 1
            tMap[temT] = 1
    for i in range(clength // n):
        currentC = compareWord[i * n:(i + 1) * n]
        clist.append(currentC)
    for i in range(len(clist)):
        if i + 1 < len(clist):
            combineC = combineC + 1
            temC = clist[i] + clist[i + 1]
            if temC in tMap:
                intersection_value = intersection_value + 1
    ngram_value = combineC + combineT - 2 * intersection_value
    return ngram_value


a = "word"
b = 'ward'
print(ngram(a, b, 2))

