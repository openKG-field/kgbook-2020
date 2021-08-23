#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : books_method
# @File : Centrality.py
# @Time    : 2020/8/14 11:11
# @Author  : Zhaohy



import Dijkstra
from Dijkstra import  Dijkstra,Node
import re

def graph():
    v1 = Node('v1')
    v2 = Node('v2')
    v3 = Node('v3')
    v4 = Node('v4')
    v5 = Node('v5')
    v6 = Node('v6')
    v1.link([v3, v5, v6], [10, 30, 100])
    v2.link([v3], [5])
    v3.link([v4], [50])
    v4.link([v6], [10])
    v5.link([v4, v5], [20, 60])
    v6.link([])

    nodes = [v1, v2, v3, v4, v5, v6]
    return nodes

def DegreeCentrality(nodes):
    cen_re = []

    for n in nodes:
        cen_re.append(len(n.next))
    return cen_re

def ClosenessCentrality(nodes):

    cen_re = []

    for n in nodes:
        dis = Dijkstra(n,nodes)
        close = 0
        sum_dis = 0
        count = 0
        for i in dis :
            if i == n.name: continue
            elif dis[i] == 99999 : continue
            sum_dis = sum_dis + dis[i]
            count += 1
        if sum_dis != 0 :
            close = float(count)/float(sum_dis)
        cen_re.append(close)

    return cen_re



def main():
    nodes = graph()
    degree_cen = DegreeCentrality(nodes)
    print('degree_cen = ',degree_cen)
    close_cen = ClosenessCentrality(nodes)
    print('close_cen = ',close_cen)

if __name__ == '__main__':
    main()
