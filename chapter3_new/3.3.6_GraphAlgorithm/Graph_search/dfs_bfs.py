  #!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : books_method
# @File : dfs_bfs.py
# @Time    : 2020/7/30 16:58
# @Author  : Zhaohy


def dfs(head):
    '''
    :param head:  head of map, node
    :return: rank_list
    '''
    deep_arr = []
    rank_list = [head.name]

    if head.sub is None:
        return rank_list

    deep_arr = deep_arr + head.sub

    for i in deep_arr :
        tem = dfs(i)
        rank_list = rank_list + tem

    return rank_list






def bfs(head):

    '''
    :param head:  head of map, node
    :return: rank_list
    '''
    break_arr = []
    rank_list = [head.name]

    if head.sub is None:
        return rank_list

    break_arr = break_arr + head.sub
    while len(break_arr) > 0 :
        tem = break_arr.pop(0)
        rank_list.append(tem.name)
        if tem.sub is not None :
            break_arr = break_arr + tem.sub

    return rank_list



'''
data format 

A-->b edge_weight = 1
 -->c edge_weight = 2

node :
    A.sub = [b,c]
    A.subweight = [1,2]

'''
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
'''
data 
            A
    B       C       D
E   F       G       H   I

J           K       L
M           N                           
            O

'''


def main():
    a = Node('a')
    b = Node('b')
    c = Node('c')
    d = Node('d')
    e = Node('e')
    f = Node('f')
    g = Node('g')
    h = Node('h')
    i = Node('i')
    j = Node('j')
    k = Node('k')
    l = Node('l')
    m = Node('m')
    n = Node('n')
    o = Node('o')
    a.link([b,c,d])
    b.link([e,f])
    c.link([g])
    d.link([h,i])
    e.link([j])
    g.link([k])
    h.link(([l]))
    j.link([m])
    k.link([n])
    n.link([o])


    v = dfs(a)
    print(v)

    v = bfs(a)
    print(v)


main()















