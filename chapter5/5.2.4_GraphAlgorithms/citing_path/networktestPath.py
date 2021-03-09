#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
Compute some network properties for the lollipop graph.
"""
#from networkx import *

import sys

from pymongo import MongoClient
#reload(sys)
#sys.setdefaultencoding('utf8')

try:
    import matplotlib.pyplot as plt
except:
    raise




def pubidListExact(path):
    count = 0
    pubidList = []
    with open(path,'r',encoding='utf8') as f :
        for line in f :
            line = line.strip().split('\t')
            count += 1
            if count == 1 :continue
            pubidList.append(line[0])

    return pubidList



def pubidPath(pubidList,citing_path):
    citing_dict = {}
    count=0
    with open(citing_path,'r',encoding='utf8') as f :
        for line in f :
            line = line.strip().split('\t')
            line[1] = line[1].split(',')
            count += 1
            if count == 1 :continue
            citing_dict[line[0]] = {'citedList':line[1],'weight':line[2]}


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

        if  i in citing_dict :
            citedList = citing_dict[i]['citedList']
            weight = citing_dict[i]['weight']
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
        print (count, ' Done')
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
    # print("radius: %d" % radius(G))
    # print("diameter: %d" % diameter(G))
    # print("eccentricity: %s" % eccentricity(G))
    # print("center: %s" % center(G))
    # print("periphery: %s" % periphery(G))
    # print("density: %s" % density(G))
      
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


def main():
    path = './/..//..//data//test.txt'
    citedPath = ''
    pubidList = pubidListExact(path)
    #exactInf(pubidList)
    print (pubidList)
    import json

    json.dump(pubidList,open('pubids.json','w',encoding='utf8'))
    if len(pubidList) < 1 :
        print ('we do not find any meaning result for such area')
    else:
        pubidPath(pubidList,citedPath)
    
main()   
    
    
    
    
    