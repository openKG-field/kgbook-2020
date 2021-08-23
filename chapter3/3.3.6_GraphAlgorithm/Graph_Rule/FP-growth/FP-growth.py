# -*- encoding: utf-8 -*-
"""
@File    : FP-growth.py
@Time    : 2021/3/19 12:49
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""

#import xmlrpclib
from pymongo import MongoClient
import codecs
import dis


import xmlrpc.client


def ShowFpnodeList(fpnode_list):
    print ('---------------------------')

    for fpnode in fpnode_list:
        print ('(%s:%d)' % (fpnode.item, fpnode.f))


class FPNode:
    def __init__(self):
        self.item = 'null'
        self.frequency = 0
        self.child_list = []
        self.next_pointer = None
        self.father = None

    def Print(self):
        print ('(%s:%d)' % (self.item, self.frequency))
        for fpnode in self.child_list:
            fpnode.Print()


class Pointer:
    def __init__(self):
        self.pointer_start = None
        self.pointer_end = None


class FPTree:
    def __init__(self):
        # 头节点
        self.head = FPNode()

    def Load(self, f_list, items_list, header_table):
        for items in items_list:
            sorted_items = []
            for item in items:
                if len(sorted_items) == 0:
                    sorted_items.append(item)
                    continue
                idx = len(sorted_items) - 1
                while idx >= -1:
                    if idx == -1:
                        sorted_items.insert(idx + 1, item)
                        break;
                    elif f_list[sorted_items[idx]] < f_list[item]:
                        idx = idx - 1
                    else:
                        sorted_items.insert(idx + 1, item)
                        break;
            # items排序完毕
            # print sorted_items
            # 构造
            now_level = 0
            now_head = self.head
            level = 0
            prefix_over = 0
            for item in sorted_items:
                level = level + 1
                fpnode_list = []
                self.GetLevelList(now_head, now_level, level, fpnode_list)
                # ShowFpnodeList(fpnode_list)

                fpnode = None
                if prefix_over == 0:
                    fpnode = self.SearchInList(item, fpnode_list)

                # 没有结点
                if fpnode == None:
                    prefix_over = 1
                    fpnode = FPNode()
                    fpnode.item = item
                    fpnode.frequency += 1
                    fpnode.father = now_head
                    now_head.child_list.append(fpnode)
                    now_head = fpnode
                    now_level = level

                    # 查找header
                    header = None
                    for i in range(0, len(header_table)):
                        if header_table[i].item == item:
                            header = header_table[i]
                            break
                    if header == None:
                        print ('error!没找到header')
                        exit
                    if header.pointer.pointer_start == None:
                        header.pointer.pointer_start = fpnode
                        header.pointer.pointer_end = fpnode
                    else:
                        header.pointer.pointer_end.next_pointer = fpnode
                        header.pointer.pointer_end = fpnode

                else:
                    # 找到节点继续搜索下一层
                    now_head = fpnode
                    now_level = level
                    now_head.frequency += 1

    # 搜索item的fpnode
    def SearchInList(self, item, fpnode_list):
        for fpnode in fpnode_list:
            if fpnode.item == item:
                return fpnode
        return None

    # raise
    # 获取某一层节点列表
    def GetLevelList(self, this_fpnode, this_level, level, fpnode_list):
        if this_level == level:
            fpnode_list.append(this_fpnode)
            return

        for fpnode in this_fpnode.child_list:
            self.GetLevelList(fpnode, this_level + 1, level, fpnode_list)

    def Print(self):
        self.head.Print()


class Header:
    def __init__(self, item):
        self.item = item
        self.pointer = Pointer()
        self.frequency = 0



f =codecs.open('RelateCorpus.txt','r',encoding='utf-8')
from jiebaCutPackage import jiebaInterface
wordAll=[]
f_list = {}
for i in f.readlines():
    wordsList = []
    i=jiebaInterface.jiebaCut(i.encode('utf-8').strip())
    i=i.split(',')
    for k in i:
        word = k.split('_')[0]
        if word ==None or len(word) <2:
            continue

        wordsList.append(word)
        if word in f_list :
            f_list[word] += 1
        else:
            f_list[word] =1

    wordAll.append(wordsList)


print ('head list ',f_list)

header_table = []
for item in f_list.keys():
    a_header = Header(item)
    header_table.append(a_header)



# items_list = [['a', 'b'], ['b', 'd', 'c'], ['e', 'c', 'd', 'a'], ['a', 'd', 'e'],
#               ['a', 'b', 'c'], ['a', 'b', 'c', 'd'], ['a'], ['a', 'b', 'c'], ['a', 'b', 'd'], ['b', 'c', 'e']]
# print (items_list)

dataset = wordAll
print('####################################',dataset)
fp_tree = FPTree()
fp_tree.Load(f_list, dataset, header_table)
fp_tree.Print()




def ShowHeaderTable(header_table):
    word_relate_list = []
    fp_list =[]
    for header in header_table:
        #print (header.item)
        fpnode = header.pointer.pointer_start
        fp_list.append(fpnode)


    def recur_fp_list(cur ,fp_list):
        org = cur
        if len(fp_list) == 0 : return org
        for fpnode in fp_list:
            cur = cur + [fpnode.item]

            if list(set(cur)) != 2 :
                print('当前关联词 组合 支持度 = ', cur, fpnode.frequency)
            if fpnode :
                fp_list = fpnode.child_list
                cur = recur_fp_list(cur,fp_list)

    recur_fp_list([],fp_list)

    #
    #
    #     cur = []
    #     while fpnode != None:
    #
    #         cur.append(fpnode.item)
    #         cur = list(set(cur))
    #         if len(cur) > 1 :
    #             word_relate_list.append((cur,fpnode.frequency))
    #         fpnodes = fpnode.child_list
    #
    #     # print('##################### next tree')
    # return word_relate_list

word_relate_list = ShowHeaderTable(header_table)
print(word_relate_list)
