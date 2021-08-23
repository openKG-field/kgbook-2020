#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
Compute some network properties for the lollipop graph.
"""
from networkx import *

import sys

from pymongo import MongoClient

try:
    import matplotlib 
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
   
except:
    raise


def pubidListExact(path):
    count = 0
    pubidList = []
    with open(path,'r') as f :
        for line in f :
            line = line.strip().split('\t')
            count += 1
            if count == 1 :continue
            pubidList.append(line[0])

    return pubidList



def pubidPath(pubidList,citing_path):
    citing_dict = {}
    count=0
    with open(citing_path,'r') as f :
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
            weight = int(citing_dict[i]['weight'])
            #print(citedList,weight)
            if len(citedList) < 1 :
                continue
            for t in citedList:
                print(i,t,weight)
                G.add_edge(i,t,weight=weight)
    
    print('graph content \n\n')
    
    #for edge in G.edges:
#	print(edge)

    print('##################')
 
    pathlengths = []
    # 单源最短路径算法求出节点v到图G每个节点的最短路径，存入pathlengths
    count = 0
    print("source vertex {target:length, }")
    for v in G.nodes():
        count += 1
        if count > 10 : break
        spl = single_source_shortest_path_length(G, v)
        print('%s %s' % (v, spl))
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

    elarge = [(u, v) for (u, v,d) in G.edges(data=True) if d['weight'] > 10 ]
    esmall = [(u, v) for (u, v,d) in G.edges(data=True) if d['weight'] <= 10]
      
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=10)
    # 根据权重，实线为权值大的边，虚线为权值小的边
    # edges
    nx.draw_networkx_edges(G, pos,edgelist=elarge,
                           width=5)
    #nx.draw_networkx_edges(G, pos,edgelist=esmall,
    #                       width=1, alpha=0.5, edge_color='b', style='dashed') #edgelist=true,
      
    # labels标签定义
    #nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
      
    plt.axis('off')
    plt.savefig("weighted_graph1.png")  # save as png
    plt.show()  # display

import json
def main():
    #path = './/..//..//data//test.txt'
    citedPath = 'citing_file.txt'
    pubidList = json.load(open('pubids.json','r'))
    if len(pubidList) < 1 :
        print ('we do not find any meaning result for such area')
    else:
        pubidPath(pubidList,citedPath)
    
main()   
    
    
    
    
    
