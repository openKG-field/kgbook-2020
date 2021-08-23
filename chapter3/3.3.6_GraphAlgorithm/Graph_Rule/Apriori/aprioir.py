# -*- encoding: utf-8 -*-
"""
@File    : aprioir.py
@Time    : 2021/3/19 12:49
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""

'''
#请从最后的main方法开始看起
Apriori算法，频繁项集算法
A 1,   B 2,   C 3,   D 4,   E 5
1 [A C D]       1 3 4
2 [B C E]       2 3 5
3 [A B C E]     1 2 3 5
4 [B E]         2 5

min_support = 2  或  = 2/4
'''

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

step = 0
result = []


def item(dataset):      #求第一次扫描数据库后的 候选集，（它没法加入循环）
    c1 = []     #存放候选集元素

    for x in dataset:       #就是求这个数据库中出现了几个元素，然后返回
        for y in x:
            if [y] not in c1:
                c1.append( [y] )
    c1.sort()
    #print(c1)
    return c1

def get_frequent_item(dataset, c, min_support):
    cut_branch = {}     #用来存放所有项集的支持度的字典
    for x in c:
        for y in dataset:
            if set(x).issubset(set(y)):     #如果 x 不在 y中，就把对应元素后面加 1
                cut_branch[tuple(x)] = cut_branch.get(tuple(x), 0) + 1     #cut_branch[y] = new_cand.get(y, 0)表示如果字典里面没有想要的关键词，就返回0
    #print(cut_branch)

    Fk = []       #支持度大于最小支持度的项集，  即频繁项集
    sup_dataK = {}  #用来存放所有 频繁 项集的支持度的字典

    for i in cut_branch:
        if cut_branch[i] >= min_support:    #Apriori定律1  小于支持度，则就将它舍去，它的超集必然不是频繁项集
            Fk.append( list(i))
            sup_dataK[i] = cut_branch[i]
    #print(Fk)
    return Fk, sup_dataK

def get_candidate(Fk, K):       #求第k次候选集
    ck = []    #存放产生候选集

    for i in range(len(Fk)):
        for j in range(i+1, len(Fk)):
            L1 = list(Fk[i])[:K-2]
            L2 = list(Fk[j])[:K-2]
            L1.sort()
            L2.sort() #先排序，在进行组合

            if L1 == L2:
                if K > 2:       #第二次求候选集，不需要进行减枝，因为第一次候选集都是单元素，且已经减枝了，组合为双元素肯定不会出现不满足支持度的元素
                    new = list(set(Fk[i]) ^ set(Fk[j]) ) #集合运算 对称差集 ^ （含义，集合的元素在t或s中，但不会同时出现在二者中）
                    #new表示，这两个记录中，不同的元素集合
                    # 为什么要用new？ 比如 1，2     1，3  两个合并成 1，2，3   我们知道1，2 和 1，3 一定是频繁项集，但 2，3呢，我们要判断2，3是否为频繁项集
                    #Apriori定律1 如果一个集合不是频繁项集，则它的所有超集都不是频繁项集
                else:
                    new = set()
                for x in Fk:
                    if set(new).issubset(set(x)) and list(set(Fk[i]) | set(Fk[j])) not in ck:  #减枝 new是 x 的子集，并且 还没有加入 ck 中
                        ck.append( list(set(Fk[i]) | set(Fk[j])) )
    #print(ck)
    return ck

def Apriori(dataset, min_support = 2):
    c1 = item (dataset) #返回一个二维列表，里面的每一个一维列表，都是第一次候选集的元素
    f1, sup_1 = get_frequent_item(dataset, c1, min_support)       #求第一次候选集

    F = [f1]      #将第一次候选集产生的频繁项集放入 F ,以后每次扫描产生的所有频繁项集都放入里面
    sup_data = sup_1       #一个字典，里面存放所有产生的候选集，及其支持度

    K = 2 #从第二个开始循环求解，先求候选集，在求频繁项集

    while (len(F[K-2]) > 1):  #k-2是因为F是从0开始数的     #前一个的频繁项集个数在2个或2个以上，才继续循环，否则退出
        ck = get_candidate(F[K-2], K)  #求第k次候选集
        fk, sup_k = get_frequent_item(dataset, ck, min_support)     #求第k次频繁项集

        F.append(fk)    #把新产生的候选集假如F
        sup_data.update(sup_k)  #字典更新，加入新得出的数据
        K+=1

    filter_data = {}

    for i in sup_data:
        if len(i) == 1 : continue
        filter_data[i] = sup_data[i]

    return F, filter_data    #返回所有频繁项集， 以及存放频繁项集支持度的字典


from jiebaCutPackage import jiebaInterface
import codecs

f =codecs.open('RelateCorpus.txt','r',encoding='utf-8')

wordAll=[]
for i in f.readlines():
    wordsList = []
    i=jiebaInterface.jiebaCut(i.encode('utf-8').strip())
    i=i.split(',')
    for k  in i:
        if k.split('_')[0] ==None or len(k.split('_')[0]) <2:
            continue
        w = k.split('_')[0]
        if len(w) < 1 or w.isspace():
            continue
        wordsList.append(w)

    wordAll.append(wordsList)
print(len(wordAll))
import time



if __name__ == '__main__':
    relations=[]


    dataset = wordAll[:20]  #relations#wordAll #funList #wordAll[:50] #[[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]       #装入数据 二维列表

    s=time.time()
    F, sup_data = Apriori(dataset, min_support = 3)   #最小支持度设置为2

    e=time.time()
    print ('the time is', e-s)
    print("具有关联的词是{}".format(F))   #带变量的字符串输出,必须为字典符号表示
    print('------------------')
    print("对应的支持度为{}".format(sup_data))
