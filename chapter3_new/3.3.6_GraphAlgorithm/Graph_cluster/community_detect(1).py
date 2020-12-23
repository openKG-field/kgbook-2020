#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : books_method
# @File : community_detect.py
# @Time    : 2020/8/14 14:05
# @Author  : Zhaohy
import math

class Node():
    name = ''
    edge = ''
    next = []
    def __init__(self,name):
        self.name = name

    def link(self,edge,next):
        self.next = next
        self.edge = edge

class community_detect():
    graph = None
    def __init__(self,grpah):
        self.graph = grpah

    def Louvain(self):

        def modularity_Q(communitys, m):
            # result between 0.3 - 0.7 is good result
            tem = 0

            for i in communitys:
                e = i.edge
                v = i.degree
                tem = tem + float(e) / float(m) - math.pow(float(v) / float(m) * 2, 2)

        def merge_node(nodes):
            new_name = ''
            new_edge = 0
            new_next = []
            for i in nodes :
                new_name = new_name + i.name
                new_edge += i.edge
                new_next = new_next + i.next
            new_next = list(set(new_next))
            new = Node(new_name)
            new.link(new_edge,new_next)
            return new

        nodes = self.graph.nodes
        m = self.graph.edges
        while True:
            left_node = []
            used_node = []
            break_flag = True
            for node in self.graph.nodes:
                cur_q = modularity_Q(node,m)
                tem = node.next
                merge_list = []
                #当前点的链接点
                for n in tem :
                    tem_q = modularity_Q([node,n],m)
                    if tem_q - cur_q > 0 :
                        merge_list.append(n)
                        break_flag = False

                used_node = used_node + merge_list
                new_node = merge_node(merge_list)
                left_node.append(new_node)

            left_node = left_node + list(set(nodes) - set(used_node))
            if break_flag :
                break
            else:
                nodes=left_node
        #nodes 中 每一个node.name 中包含 当前类内所有分组node的name
        return nodes
def load_data():

    '''
    利用 class Node  组成 graph
    graph = list
    e.g. :
    graph = []
    a = Node('a')
    a.link(3,[b,c,d])

    graph.append(a)

    cd = community_detect(graph)

    clusters = cd.Louvain()

    for i in cluster :
        print(i.name)  此处为当前聚类的所有原始node名称


    '''

