#coding=utf-8
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

from pymongo import MongoClient
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

step = 0
result = []
def wordMongo(tb):
    host = '10.0.5.12'
    port = 27017
    passwd = 'mq2019'
    dbName = 'mqpat'
    user = 'mqpat-rw'
    myTbNme = tb
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[myTbNme]
    return (conn,db,collection)


#from elasticsearch import Elasticsearch

#from elasticsearch import helpers
#es = Elasticsearch(['10.0.5.18:9200'], headers={'content-type': 'application/json'})
def test(tb):
    host = '10.0.5.11'
    port = 27017
    passwd = '123456'
    dbName = 'test'
    user = 'lyj-rw'
    myTbNme = tb
    conn = MongoClient(host, port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[myTbNme]
    return (conn, db, collection)

def v4Mongo(tb):
    host = '10.0.5.12'
    port = 27017
    passwd = 'mq2019'
    dbName = 'mqpatv4'
    user = 'mqpatv4-rw'
    myTbNme = tb
    conn = MongoClient(host, port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[myTbNme]
    return (conn, db, collection)

# (wconn ,wdb ,lcol) = v4Mongo('fieldsIndivideBase')
# import  codecs
#
# funList = []
# count = 0
# for data in lcol.find({'userid': 'wangnan', 'fieldsName': '小红象'}, {'pubid': 1, 'title': 1, 'fieldWords': 1,'techWords':1,
#                                                                     'techArea': 1,'funcWords':1}).batch_size(100):
#     print ('true')
#     dataList=[]
#     if 'funcWords' not in data:
#         continue
#     for i in data['funcWords']:
#         if i ==None or len(i)<2:
#             continue
#         dataList.append(i)
#     funList.append(dataList)
#     # for i in data['fieldWords']:
#     #     count += 1
#     #     funList.append(i)
# print (len(funList))

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
    return F, sup_data    #返回所有频繁项集， 以及存放频繁项集支持度的字典


from jiebaCutPackage import jiebaInterface
import codecs

f =codecs.open('RelateCorpus.txt','r',encoding='utf-8')

wordAll=[]
for i in f.readlines():
    wordsList = []
    i=jiebaInterface.jiebaCut(i.encode('utf-8'))
    i=i.split(',')
    for k  in i:
        if k.split('_')[0] ==None or len(k.split('_')[0]) <2:
            continue
        print (k)
        wordsList.append(k.split('_')[0])

    wordAll.append(wordsList)
print(len(wordAll))
import time


# import json
# from predictKG_link_modify_online import *
# import codecs
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
# import xmlrpclib
# #proxy = xmlrpclib.ServerProxy("http://119.18.207.122:30018")
# proxy = xmlrpclib.ServerProxy("http://10.0.5.10:30018")
# #a =  proxy.searchInfoByApp(person, app, area, school, regionTime, tech)
# import time
# # fieldsName = '通信用光器件'
# # #通信用光器件-光源
# # language = 'cn'
# # a = proxy.evalueAlert(fieldsName)
# s =time.time()
# from mongoC import mongC
# file = r'/home/pydep/wangnan/BERT-BiLSTM-CRF-NER-master/resultSentField-sat.txt'
#
# a = proxy.predict_online(file)
#
# e = time.time()
#
# print ('the cost time is',e-s)
# print ('.........................................')
# count =0
# relationList=[]
# relationOne=[]
# for k,v in a.items():
#     if v[0] =='' or len(v[0]) < 2:
#         continue
#     print (len(v[0]),'...',len(v[1][0]))
#     relation = run(v[0],v[1])
#     sentence =''.join(v[0])
#
#     print ('the relation is',relation)
#
#     if type(relation) =='int' or relation == -1 or relation =='-1':
#         continue
#     if relation==[] or len(str(relation))<2:
#         continue
#     if type(relation) !='int':
#             relationList.append(relation)
#
#     count +=1
# print (count)


if __name__ == '__main__':
    relations=[]
    # #funList=[['人工','智能'],['深度学习','智能','深度','智能'],['深度','智能','人工智能','智能'],['人工','深度智能','人工','智能'],['人工','人工智能']]
    # for i in relationList:
    #     relation=[]
    #     for j in i:
    #         j=j.split('_')
    #         relation.append(j[0]+'_'+j[1])
    #     relations.append(relation)
    # print (len(relations))

    dataset = wordAll[:20]  #relations#wordAll #funList #wordAll[:50] #[[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]       #装入数据 二维列表

    s=time.time()
    F, sup_data = Apriori(dataset, min_support = 3)   #最小支持度设置为2
    # f=codecs.open('resultRlation.txt','w',encoding='utf-8')
    # for i in F[0]:
    #     if len(i)==1:
    #         f.write(str(i).decode("string_escape"))
    #         f.write('\n')
    #     else:
    #         f.write(str(i).decode("string_escape"))
    #         f.write('\n')
    #
    # f.write('.....................................................')
    # for k,v in sup_data.iteritems():
    #    f.write(str(k).decode("string_escape"))
    #    f.write('\n')
    # f.close()
    e=time.time()
    print ('the time is', e-s)
    print("具有关联的商品是{}".format(F))   #带变量的字符串输出,必须为字典符号表示
    print('------------------')
    print("对应的支持度为{}".format(sup_data))
