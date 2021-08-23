#!/usr/bin/env python
# _*_coding:utf-8_*_
"""
@File    : TFIDF.py
@Time    : 2021/3/19 10:19
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""

import  math
def tfidf(word, document_len, documents):
    # tf
    # print ('the length is',document_len)

    tf = 0
    len_tf = 0
    for doc in documents:
        amount = len(doc)
        if amount == 0: continue
        cur = 0
        for w in doc:
            if word == w:
                cur += 1

        cur_fre = float(cur) / float(amount)
        tf += cur_fre
        len_tf += 1

    if len_tf == 0:
        print ('tf',word)
        return 0

    tf = float(tf) / float(len_tf)

    # print ('tf is',tf)
    # idf
    df = 0
    for d in documents:
        dd = ''.join(d)
        if word in dd:
            df += 1

    if df == 0 or document_len == 0:
        print ('df',df,document_len)
       # print (word)
        for d in documents:
            print (''.join(d))

        return 0
    tem = float(document_len) / float(df)
    # print ('tem is', tem)
    idf = math.log10(tem)

    return round(tf * idf, 8)
