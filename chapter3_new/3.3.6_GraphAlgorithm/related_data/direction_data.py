#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : books_method
# @File : direction_data.py
# @Time    : 2020/9/2 10:54
# @Author  : Zhaohy

class Node():
    sub = None
    sub_weight = []
    name = None
    def __init__(self,name):
        self.name = name
    def link(self,sub,sub_weight=None):
        self.sub = sub
        if sub_weight == None:
            sub_weight = [1 for i in sub]
        self.sub_weight = sub_weight


NodeList = []

with open('graph_data','r',encoding='utf8') as f:
    for line in f :
        line = line.strip().split()
        pubid = line[0]
        citedPubids = line[-3]
        if '_' in citedPubids:
            tem = Node(pubid)
            tem.link(citedPubids.split('_'))
            NodeList.append(tem)

