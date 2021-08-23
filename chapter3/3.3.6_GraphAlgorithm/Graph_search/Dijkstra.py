#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : books_method
# @File : dis.py
# @Time    : 2020/8/14 10:22
# @Author  : Zhaohy




class Node():
    next = []
    sub_weight = []

    name = None
    def __init__(self,name):
        self.name = name
    def link(self,next,sub_weight=None):
        self.next = next

        if sub_weight == None:
            sub_weight = [1 for i in next]
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
    print('test = ',head.next)
    for j in range(len(head.next)):
        sub_node = head.next[j].name
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
        for j in range(len(n.next)):
            sub_node = n.next[j].name
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


def load_data(path):

    '''
    利用 class Node  组成 graph
    graph = list
    e.g. :
    graph = []
    a = Node('a')
    a.link([b,c,d])

    graph.append(a)

    cd = community_detect(graph)

    clusters = cd.Louvain()

    for i in clusters :
        print(i.name)  此处为当前聚类的所有原始node名称
    '''

    count = 0
    graph = []
    node_dict = {}
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            line = line.strip().split('\t')
            count += 1
            if line[1] == '-1' or count == 1 or len(line) < 4: continue
            cur = line[1].split('__')

            if line[0] in node_dict:
                node_dict[line[0]] = node_dict[line[0]] | set(cur)
            else:
                node_dict[line[0]] = set(cur)
            for i in cur:
                if i in node_dict:
                    node_dict[i] = node_dict[i] | set([line[0]])
                else:
                    node_dict[i] = set([line[0]])
            if count > 10: break

    #print(node_dict)
    str_node = {}
    cp = []
    for i in node_dict:
        name = i
        edge = list(node_dict[i])
        tem = Node(name)
        tem.link(edge)
        str_node[name] = tem
        cp.append(tem)
    for i in cp:
        #print('test = ',i,i.next)
        str_list = i.next
        cur = []
        for j in str_list:
            cur_node = str_node[j]
            cur.append(cur_node)
        i.link( cur)
        graph.append(i)

    print(graph)
    return graph


def main():
    '''
    map create
    '''

    # v1 = Node('v1')
    # v2 = Node('v2')
    # v3 = Node('v3')
    # v4 = Node('v4')
    # v5 = Node('v5')
    # v6 = Node('v6')
    # v1.link([v3,v5,v6],[10,30,100])
    # v2.link([v3],[5])
    # v3.link([v4],[50])
    # v4.link([v6],[10])
    # v5.link([v4,v5],[20,60])
    # v6.link([])
    # nodes = [v1,v2,v3,v4,v5,v6]
    path = '.\\..\\..\\data\\graph_data'
    graphs = load_data(path)

    dis = Dijkstra(graphs[0],graphs)
    print('dis ############################ ',dis)


main()


