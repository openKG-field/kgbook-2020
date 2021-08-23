#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
Compute some network properties for the lollipop graph.
"""
import re
from networkx import *
import codecs
import random
import sys



try:
    import matplotlib.pyplot as plt
except:
    raise


def longestPath(deepMap,start):
    if start not in deepMap:
        return [start]
    else:
        pathList = deepMap[start]
        cur = []
        for i in pathList:
            tem = longestPath(deepMap, i)
            #print 'tem = ',tem
            if len(tem) > len(cur):
                cur = tem    
        #print 'cur =', cur 
        return [start] + cur
        


    
def deepCount(patentCluster,startKey,deep,pointPath):
    pointPath = []
    cur = 0
    #curPoint = ''
    #pointPath.append('')
    temPath = []
    for i in patentCluster[startKey]:
        if i in patentCluster:
            (tem,temPath) = deepCount(patentCluster, i, deep,pointPath)
            if cur < tem:
                cur = tem
                pointPath = temPath
            else:
                temPath = []
                
    pointPath.append(startKey)
    deep = cur + 1
    return (deep,pointPath)
    


def extractMaxN(m,n):
    r = {}
    for k,v in sorted(m.iteritems(),key=lambda k:k[1],reverse=True):
        if n < 1:
            break
        r[k] = v
        n = n -1
    
    return r
        


def relatedPatent(pubidList,citing_path):
    citing_dict = {}
    count=0
    patentDict = {}
    appYearList = {}
    pathDict = {}
    with open(citing_path, 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            line[1] = line[1].split(',')
            count += 1
            if count == 1: continue
            citing_dict[line[0]] = {'citedList': line[1], 'weight': line[2]}
            patentDict[line[0]] = line[2]
            appYearList[line[0]] = line[3]
            for p in line[1] :
                cur = line[0] + '$$$$' + p
                if line[0] in pubidList:
                    pathDict[cur] =  1

    pointDict = {}
    xAll = []
    yAll = []
    vMax = -1
    for k,v in sorted(patentDict.items(),key=lambda k:k[1],reverse=True):
        xAll.append(int(appYearList[k]))
        yAll.append(v)
        if vMax == -1:
            vMax = v
        pointDict[k] = (int(appYearList[k]),v)
    
    
    
    newest = ''
    oldest = ''
    for k,v in sorted(appYearList.items() ,key=lambda k:k[1],reverse=True):
        if newest =='':
            newest = k
        oldest = k
        #print k,v
    
#     print newest, appYearList[newest]
#     print oldest, appYearList[oldest]
    
    lx = []
    ly = []
    
    forewordWeight = {}
    backwordWeight = {}
    
    patentCluster = {}
    
    count = 0
    for i in pathDict:
        [a,b] = i.split('$$$$')
        if a in patentCluster:
            patentCluster[a].append(b)
        else:
            patentCluster[a] = [b]
            
    R = {}
    P = {}

    for i in patentCluster:
        #if i == 'US3837602A':
        (R[i],P[i]) = deepCount(patentCluster, i, 0,[])

        
    topK = []
    n = 5
    mainPathX = {}
    mainPathY = {}
    mainPathPointX = []
    mainPathPointY = []
    mainPubid = []
    for k,v in sorted(R.items(),key=lambda k:k[1],reverse=True):
        if n < 0:
            break
        print (k,'deep Count value =', v)
        topK.append(k)
        mainPathX[k] = []
        mainPathY[k] = []
        for i in range(len(P[k])-1):
            a = P[k][i]
            b = P[k][i+1]
            if a in pointDict and b in pointDict:
                (x1,y1) = pointDict[a]
                (x2,y2) = pointDict[b]
                mainPathX[k].append([x1,x2])
                mainPathY[k].append([y1,y2])
                mainPathPointX.append(x1)
                mainPathPointY.append(y1)
                mainPubid.append(a)
                if i+2 == len(P[k]):
                    mainPathPointX.append(x2)
                    mainPathPointY.append(y2)
                    mainPubid.append(b)
        n -= 1
        

    for i in pathDict:
        [a,b] = i.split('$$$$')
        if a in pointDict and b in pointDict:
            if a in forewordWeight:
                forewordWeight[a] += 1
            else:
                forewordWeight[a] =1
            if b in backwordWeight:
                backwordWeight[b] += 1
            else:
                backwordWeight[b] = 1
                 
#     maxFore = extractMaxN(forewordWeight, 10)
#     maxBack = extractMaxN(backwordWeight, 10)       
            
            
    x = []
    y = []
    for i in pathDict:
        [a,b] = i.split('$$$$')
        if a in pointDict and b in  pointDict:
             if True:
                (x1,y1) = pointDict[a]
                (x2,y2) = pointDict[b]
                lx.append((x1,x2))
                ly.append((y1,y2))     
                x.append(x1)
                x.append(x2)
                y.append(y1)
                y.append(y2)

    #==================color ===========================
    #b---blue   c---cyan  g---green    k----black
    #m---magenta r---red  w---white    y----yellow
    #
    #
    #===================================================
    
    colorList = ['b','c','g','k','m','r','w','y']
    
    
    
    plt.plot(mainPathPointX,mainPathPointY,'bo') 
#     plt.plot(x, y, 'r*')
    print ('amount line = ',len(mainPathX))
    
    for i in mainPathX:
        color = colorList.pop(0)+'-'
        for j in range(len(mainPathX[i])):
            plt.plot(mainPathX[i][j],mainPathY[i][j],color)
#     for i in range(len(mainPathX)):
#         plt.plot(mainPathX[i],mainPathY[i],'-')
    begin = int(appYearList[oldest]) -2
    end = int (appYearList[newest]) + 2
    eva = int(vMax)-1
    plt.axis([begin,end,-2,eva])
    for x, y in zip(mainPathPointX, mainPathPointY):
        plt.annotate(
            mainPubid.pop(0),
            xy=(x, y),
            xytext=(-10, 10),
            textcoords='offset points',
            ha='center',
            va='top')
    plt.show()
    plt.savefig('imageUS.png',format='png')

import json
def main():
    citedPath = 'citing_file.txt'
    pubidList = json.load(open('pubids.json','r'))
    if len(pubidList) < 1 :
        print ('we do not find any meaning result for such area')
    else:
        relatedPatent(pubidList,citedPath)

main()


    
    
    
    
    
    
    
    
    
    

    