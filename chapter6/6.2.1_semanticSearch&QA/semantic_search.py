#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@File     : semantic_search.py
@Time     : 2021/8/20 13:29
@Author   : zhaohongyu
@Email    : zhaohongyu2401@yeah.net
@Software : PyCharm
"""
import json
from jieba import posseg as pg

hypernym = json.load(open('hypernym.json','r',encoding='utf8'))
print('hypernym 加载成功，共加载 {num}个 '.format(num=len(hypernym)))
synonym = json.load(open('synonym.json','r',encoding='utf8'))
print('synonym 加载成功，共加载 {num}个 '.format(num=len(synonym)))
def semantic_query(query):
    words=  []
    for w, f in pg.cut(query):
        if (f[0] == 'n' or f =='j') and len(w) > 1 :
            words.append(w)
    query_list = []
    for w in words :
        tem = [w]
        if w in hypernym :
            tem = tem +  [w.replace("'","") for w in hypernym[w]]
        if w in synonym:
            tem = tem + [w.replace("'","") for w in synonym[w]]

        co = []
        for i in tem :
            if len(i) > 1 :
                co.append(i)
        # "('移动支付' and '人工智能') or '区块链' or ('数据 测试'~'10')"
        co ="'" + "' or '".join(co) +"'"

        query_list.append(co)

    remodify_query  = "(" + ") and (".join(query_list) + ")"

    return remodify_query




query = '通信大数据'
print (semantic_query(query))






