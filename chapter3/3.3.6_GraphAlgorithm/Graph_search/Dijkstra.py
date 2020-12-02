#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : books_method
# @File : dis.py
# @Time    : 2020/8/14 10:22
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

def Dijkstra(head,nodes):
    '''
    :param head:  起始点
    :param nodes:  包括起始点在内的所有点（图内点不可构成循环，如 a->b->c->a）
    :return:
    '''


    dis = {}
    flag = {}

    name_node = {}
    #初始化dis空间，并最大化赋值
    path = {}
    for i in nodes:
        dis[i.name] = 99999
        flag[i.name] = 0
        name_node[i.name] = i
        path[i.name] = []
    #初始化head点关联所有点的距离
    dis[head.name] = 0
    flag[head.name] = 1
    path[head.name].append(head.name)

    for j in range(len(head.sub)):
        sub_node = head.sub[j].name
        sub_dis = head.sub_weight[j]

        if dis[sub_node] > sub_dis:
            dis[sub_node] = sub_dis

    #每次选择dis空间内未遍历的最近点作为下一次循环的初始点，直至遍历所有点结束

    while True:
        ind = ''
        for k,v in sorted(dis.items(),key=lambda k:k[1],reverse=False):
            if flag[k] == 1 : continue
            ind = k
            break
        n = name_node[ind]
        flag[n.name] =  1
        tem = dis[n.name]
        for j in range(len(n.sub)):
            sub_node = n.sub[j].name
            sub_dis = n.sub_weight[j] + tem
            if dis[sub_node] > sub_dis :
                dis[sub_node] = sub_dis
        break_flag = True
        #print(flag)
        for i in flag :
            if flag[i] == 0 :
                break_flag = False
        if break_flag :
            break

    return dis




def main():
    '''
    map create
    '''

    v1 = Node('v1')
    v2 = Node('v2')
    v3 = Node('v3')
    v4 = Node('v4')
    v5 = Node('v5')
    v6 = Node('v6')
    v1.link([v3,v5,v6],[10,30,100])
    v2.link([v3],[5])
    v3.link([v4],[50])
    v4.link([v6],[10])
    v5.link([v4,v5],[20,60])
    v6.link([])
    nodes = [v1,v2,v3,v4,v5,v6]
    dis = Dijkstra(v1,nodes)
    print(dis)
    dis = Dijkstra(v2,nodes)
    print(dis)

main()


