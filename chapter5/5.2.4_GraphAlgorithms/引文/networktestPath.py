#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
Compute some network properties for the lollipop graph.
"""
from networkx import *
import codecs
import random
import sys
from lineModifyTool import lineModify
from pymongo import MongoClient
reload(sys)
sys.setdefaultencoding('utf8')

try:
    import matplotlib.pyplot as plt
except:
    raise

dbName = 'mqpat'
user = 'mqpat-rw'
passwd = '123456'
host = '119.18.207.122'
port = 27017

def createMongo(tb):
    global dbName,user,passwd,host,port
    tbName = tb
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[tbName]
    return (conn,db,collection) 


def pubidListExact(name):
    (conn,db,col) = createMongo('fieldsIndivideBase')
    s = {'fieldsName': name, 'noisyType': 'O'}
    filter = {'pubidList': 1, 'pubid': 1}

    pubidList = []
    for data in col.find(s, filter).batch_size(100):
        if 'pubid' in data:
            pubidList.append(data['pubid'])
#     s = {'fieldsName':name}
#     filter= {'citingList':1}
#
#
#     pubidList = []
#     for data in col.find(s,filter):
#         if data.has_key('pubidList'):
#             pubidList = data['pubidList']
# #             for [weight,patent] in patents:
# #                 #print patent['pubid']
# #                 pubidList.append(patent['pubid'])
    return pubidList

def pubidPath(pubidList):
#pubids by read file=========================
#     f = codecs.open('CitingPat.txt','r')
#     file =list()
#     for line in f.readlines():
#         line = lineModify(line)
#         if 'CN' in line:
#             pubid = line[:len(line)-1]
#         else:
#             pubid = line
#         file.append(pubid+' ')
    (conn,db,col) = createMongo('cn_patent')
     
    file = pubidList
    G = nx.MultiGraph()
    i=2             
    citedList= []
    weight = 0
    for i in file:
        for j in file:
            if i !=j:
                G.add_edge(i,j,weight=1)
     
    for i in file:
        for data in col.find({'pubid':i},{'citedPubidList':1,'citedCount':1}):
            if data.has_key('citedPubidList') and data.has_key('citedCount'):
                citedList = data['citedPubidList']
                weight = data['citedCount']
        if len(citedList) < 1 :
            continue
        for t in citedList:
            G.add_edge(i,t,weight=weight)
      
    #G = lollipop_graph(4, 6)
    pathlengths = []
    # 单源最短路径算法求出节点v到图G每个节点的最短路径，存入pathlengths
    count = 0
    print("source vertex {target:length, }")
    for v in G.nodes():
        count += 1
        print count, ' Done'
        spl = single_source_shortest_path_length(G, v)
        #print('%s %s' % (v, spl))
        for p in spl.values():
            pathlengths.append(p)
            # 取出每条路径，计算平均值。
    print('')
    print("average shortest path length %s" % (sum(pathlengths) / len(pathlengths)))
    # 路径长度直方图，如果路径不存在，设为1，如果已经存在过一次，则原先基础上加1
    # histogram of path lengths
    dist = {}
    for p in pathlengths:
        if p in dist:
            dist[p] += 1
        else:
            dist[p] = 1
      
    print('')
    print("length #paths")
    verts = dist.keys()
    for d in sorted(verts):
        print('%s %d' % (d, dist[d]))
    # 内嵌函数求图G的多个属性
    print("radius: %d" % radius(G))
    print("diameter: %d" % diameter(G))
    print("eccentricity: %s" % eccentricity(G))
    print("center: %s" % center(G))
    print("periphery: %s" % periphery(G))
    print("density: %s" % density(G))
      
    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 5]
      
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=10)
    # 根据权重，实线为权值大的边，虚线为权值小的边
    # edges
    nx.draw_networkx_edges(G, pos,edgelist=elarge,
                           width=5)
    nx.draw_networkx_edges(G, pos,edgelist=esmall,
                           width=5, alpha=0.5, edge_color='b', style='dashed') #edgelist=true,
      
    # labels标签定义
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
      
    plt.axis('off')
    plt.savefig("weighted_graph1.png")  # save as png
    plt.show()  # display
     
# def exactInf(pubids):
#     print len(pubids)
#     (conn,db,col) = createMongo('cn_patent')
#     pubidInputDict ={}
#     for i in pubids:
#         pubidInputDict[i] = 1
#     missPubid = []
#     missCount = 0
#     clusterIndex = 0
#     patentDict = {}
#     cnCount = 0
#     for data in col.find({'pubid':{'$in':pubids}},{'citingList':1,'pubid':1,'citedPubidList':1}).batch_size(100):
#         cnCount += 1
#         currentIndex = -1
#         if not  data.has_key('pubid'):
#             missCount += 1
#             continue
#         if not data.has_key('citingList') and not data.has_key('citedPubidList') :
#             #print data['pubid']
#             missPubid.append(data['pubid'])
#             missCount += 1
#             continue
#         if data.has_key('citingList'):
#             citing = data['citingList']
#             for i in citing:
#                 if not pubidInputDict.has_key(i):
#                     continue
#                 if patentDict.has_key(i):
#                     currentIndex = patentDict[i]
#                 else:
#                     currentIndex = clusterIndex + 1
#                 patentDict[i] = currentIndex
#         elif data.has_key('citedPubidList'):
#             cited = data['citedPubidList']
#             for i in cited:
#                 if not pubidInputDict.has_key(i):
#                     continue
#                 if currentIndex == -1:
#                     if patentDict.has_key(i):
#                         currentIndex = patentDict[i]
#                     else:
#                         currentIndex = clusterIndex + 1
#                 patentDict[i] = currentIndex
#         else:
#             missCount += 1
#     patentCluster = {}
#     print 'found count = ',cnCount
#     print 'orginal count = ',len(patentDict)
#     for i in patentDict:
#         index = patentDict[i]
#         if patentCluster.has_key(index):
#             patentCluster[index].append(i)
#         else:
#             patentCluster[index] = []
#             patentCluster[index].append(i)
#     
#     for i in patentCluster:
#         print 'length of current cluster = ',len(patentCluster[i])
#         #print i,'  =  ', patentCluster[i]
# #         mainIpc = data['mainIpc4'][:3]
# #         if patentDict.has_key(mainIpc):
# #             patentDict[mainIpc].append(data['pubid'])
# #         else:
# #             patentDict[mainIpc] = []
# #             patentDict[mainIpc].append(data['pubid'])
# #     for i in patentDict:
# #         print i,'  =  ',patentDict[i]
# #     
#     print 'miss count  = ',missCount    
#     print missPubid[:10]

def main():
    name = '人工智能芯片'
    pubidList = pubidListExact(name)
    #exactInf(pubidList)
    print len(pubidList)
    if len(pubidList) < 1 :
        print 'we do not find any meaning result for such area'
    else:
        pubidPath(pubidList)
    
main()   
    
    
    
    
    