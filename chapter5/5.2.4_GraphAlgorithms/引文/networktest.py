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
from lineModifyTool import lineModify
from elasticsearch import Elasticsearch
from pymongo import MongoClient
reload(sys)
sys.setdefaultencoding('utf8')

es = Elasticsearch()

try:
    import matplotlib.pyplot as plt
except:
    raise

dbName = 'test'
user = 'lyj-rw'
passwd = '123456'
host = '119.18.207.121'  
port = 27017

def createMongo(tb):
    global dbName,user,passwd,host,port
    tbName = tb
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[tbName]
    return (conn,db,collection) 


def lcMongo(tb):
    dbName = 'mqpat'
    user = 'mqpat-rw'
    passwd = '123456'
    host = '119.18.207.122'
    port = 27017
    tbName = tb
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[tbName]
    return (conn,db,collection) 


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
        


    
def pubidListExact(name):
    (conn,db,col) = lcMongo('fieldsIndivideBase')
     
    s = {'fieldsName':name,'noisyType':'O'}
    filter= {'pubidList':1,'pubid':1}
     
    pubidList = []
    for data in col.find(s,filter).batch_size(100):
        if 'pubid' in data:
            pubidList.append(data['pubid'])
#             for [weight,patent] in patents:
#                 #print patent['pubid']
#                 pubidList.append(patent['pubid'])
    
#     global es
#     pubidList = []
#     index = 'patentdata'
#     doc_type = 'us_patent'
#     body = {'_source':['pubid'],'query':{'bool':{'should':[{'match_phrase':{'title':name}},{'match_phrase':{'title':'UAV'}}]}}}
#     
#     res =es.search(index, doc_type, body, size = 800000,request_timeout=500)
#     for data in res['hits']['hits']:
#         if data['_source'].has_key('pubid'):
#             pubidList.append(data['_source']['pubid'])
            
    return pubidList



def pubidUSPath(pubidList,country):

    (conn,db,col) = createMongo(country)
     
    patentDict = {}
    checkPatentDict = {}
    for i in pubidList:
        checkPatentDict[i] = 1
    pathDict = {}

    appYearList = {}
    for data in col.find({'pubid':{'$in':pubidList}},{'citedCount':1,'citedPubidList':1,'citingList':1,'pubid':1,'appYear':1,'title':1}).batch_size(100):
        if data.has_key('pubid') and data.has_key('citedCount') and data.has_key('appYear') and data.has_key('title') and( data.has_key('citedPubidList') or data.has_key('citingList')):
            #data['title'] = data['title'].lower()
            #if 'uav' in data['title'] or ' unmanned aerial' in data['title'] or 'ducted fan' in data['title']:
            p = data['pubid']
            if data.has_key('citedPubidList'):
                for j in data['citedPubidList']:
                    if checkPatentDict.has_key(j):
                        pathDict[p+'$$$$'+j] = 1
            if data.has_key('citingList'):
                for j in data['citingList']:
                    if checkPatentDict.has_key(j):
                        pathDict[j+'$$$$'+p] = 1
            if data['citedCount'] >0 :
                patentDict[data['pubid']] = int(data['citedCount'])
                appYearList[data['pubid']] = int(data['appYear'])
    
    x = []
    y = []
    vMax = -1
    for k,v in sorted(patentDict.iteritems(),key=lambda k:k[1],reverse=True):
        x.append(int(appYearList[k]))
        y.append(v)
        if vMax == -1:
            vMax = v

    pointDict = {}
    xAll = []
    yAll = []
    vMax = -1
    for k,v in sorted(patentDict.iteritems(),key=lambda k:k[1],reverse=True):
        xAll.append(int(appYearList[k]))
        yAll.append(v)
        if vMax == -1:
            vMax = v
        pointDict[k] = (int(appYearList[k]),v)
    
    lx = []
    ly = []
    
    for i in pathDict:
        [a,b] = i.split('$$$$')
        if pointDict.has_key(a) and pointDict.has_key(b):        
            #if (maxFore.has_key(a) or maxBack.has_key(a)) and (maxFore.has_key(b) or maxBack.has_key(b)):
            if True:
                (x1,y1) = pointDict[a]
                (x2,y2) = pointDict[b]
                lx.append([x1,x2])
                ly.append([y1,y2])  
    
    newest = ''
    oldest = ''
    for k,v in sorted(appYearList.iteritems() ,key=lambda k:k[1],reverse=True):
        if newest =='':
            newest = k
        oldest = k
        #print k,v
    
    print newest, appYearList[newest]
    print oldest, appYearList[oldest]
    
    deepMap = {}
    
    
    for i in range(len(lx)):
        #plt.plot(lx[i],ly[i],'-')
        (x1,x2) = lx[i]
        (y1,y2) = ly[i]
        p1 = str(x1)+'_'+str(y1)
        p2 = str(x2)+'_'+str(y2)
        if p1 == p2 or (x1==x2 ) or (x1 > x2):
            continue
        if p1 in deepMap:
            deepMap[p1].append(p2)
        else:
            deepMap[p1] = [p2]
            
    
    longest = []
    for i in deepMap:
        print i,deepMap[i]         
        vPath = longestPath(deepMap, i)
        #vPath = [i] + vPath
        #print vPath
        if len(longest) < len(vPath):
            longest = vPath
    
    print longest
    for i in range(len(longest)-1):
        p1 = longest[i]
        p2 = longest[i+1]
        [x1,y1] = p1.split('_')
        [x2,y2] = p2.split('_')
        Ex = (int(x1),int(x2))
        Ey = (int(y1),int(y2))
        plt.plot(Ex,Ey,'-')
        
        
        
        
        
         
    #plt.plot(x, y, 'ro')
    #plt.axis([int(appYearList[oldest])-1,int(appYearList[newest])+1,0,vMax+5])
#     for x, y in zip(x, y):
#         plt.annotate(
#             y,
#             xy=(x, y),
#             xytext=(0, -10),
#             textcoords='offset points',
#             ha='center',
#             va='top')
    plt.show()
    plt.savefig(country + '.png',format='png')
    
    
def pubidCNPath(pubidList):

    (conn,db,col) = createMongo('cn_patent')
     
    patentDict = {}
#     for  i in pubidList:
#         if patentDict.has_key(i):
#             continue
#         else:
#             patentDict[i] = 1
    

    appYearList = {}
    for data in col.find({'pubid':{'$in':pubidList}},{'familyExtPatList':1,'familyPatList':1,'familyCount':1,'familyIdExtCount':1,'pubid':1,'appYear':1,'title':1}).batch_size(100):
        if data.has_key('pubid') and (data.has_key('familyCount') or data.has_key('familyIdExtCount'))and data.has_key('appYear') and data.has_key('title'):
            data['title'] = data['title'].lower()
            if '无人机' in data['title'] or '涵道' in data['title'] or '涵道无人机' in data['title']:
                
                v=  0
                if data.has_key('familyCount'):
                    v = v+data['familyCount']
                if data.has_key('familyExtCount'):
                    v = v + data['familyExtCount']
                patentDict[data['pubid']] = v
                appYearList[data['pubid']] = data['appYear']
                if v >8 :
                    if data.has_key('familyPatList'):
                        print 'Id = ',data['familyPatList']
                    if data.has_key('familyExtPatList'):
                        print 'Extend = ',data['familyExtPatList']
    x = []
    y = []
    pubids = []
    vMax = -1
    for k,v in sorted(patentDict.iteritems(),key=lambda k:k[1],reverse=True):
        x.append(int(appYearList[k]))
        y.append(v)
        pubids.append(k)
        if vMax == -1:
            vMax = v
     

     
    newest = ''
    oldest = ''
    for k,v in sorted(appYearList.iteritems() ,key=lambda k:k[1],reverse=True):
        if newest =='':
            newest = k
        oldest = k
        #print k,v
     
    print newest, appYearList[newest]
    print oldest, appYearList[oldest]
     
    plt.plot(x, y, 'ro')
    plt.axis([int(appYearList[oldest])-1,int(appYearList[newest])+1,0,vMax+5])
    for x, y in zip(x, y):
        plt.annotate(
            pubids.pop(0),
            xy=(x, y),
            xytext=(0, -10),
            textcoords='offset points',
            ha='center',
            va='top')
    plt.show()
    plt.savefig('imageCN.png',format='png')
    
def dfs(patentDict,clusterDict,k,t,finishDict):
    checkKey = ''
    if t != 0:
        checkKey = t
    else:
        checkKey = k

    for i in patentDict[checkKey]:
        clusterDict[k].append(i)
        if patentDict.has_key(i) and not finishDict.has_key(i):
            (clusterDict,finishDict) = dfs(patentDict, clusterDict, k, i,finishDict)

    finishDict[checkKey] = 1
    return (clusterDict,finishDict)
    
def deepCount(patentCluster,startKey,deep,pointPath):
    pointPath = []
    cur = 0
    #curPoint = ''
    #pointPath.append('')
    temPath = []
    for i in patentCluster[startKey]:
        if patentCluster.has_key(i):
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
        


def relatedPatent(pubidList,country):
    (conn,db,col) = createMongo(country)
     
    patentDict = {}
    
    
    checkPatentDict = {}
    for i in pubidList:
        checkPatentDict[i] = 1
    
    
    pathDict = {}

    appYearList = {}
    for data in col.find({'pubid':{'$in':pubidList}},{'citedCount':1,'citedPubidList':1,'citingList':1,'pubid':1,'appYear':1,'title':1}).batch_size(100):
        if data.has_key('pubid') and data.has_key('citedCount') and data.has_key('appYear') and data.has_key('title') and( data.has_key('citedPubidList') or data.has_key('citingList')):
            p = data['pubid']
            if data.has_key('citedPubidList'):
                for j in data['citedPubidList']:
                    if checkPatentDict.has_key(j):
                        pathDict[p+'$$$$'+j] = 1
            if data.has_key('citingList'):
                for j in data['citingList']:
                    if checkPatentDict.has_key(j):
                        pathDict[j+'$$$$'+p] = 1
            if data['citedCount'] >0 :
                patentDict[data['pubid']] = int(data['citedCount'])
            appYearList[data['pubid']] = int(data['appYear'])
       
    
#     for i in pathDict:
#         print i, pathDict[i]

    pointDict = {}
    xAll = []
    yAll = []
    vMax = -1
    for k,v in sorted(patentDict.iteritems(),key=lambda k:k[1],reverse=True):
        xAll.append(int(appYearList[k]))
        yAll.append(v)
        if vMax == -1:
            vMax = v
        pointDict[k] = (int(appYearList[k]),v)
    
    
    
    newest = ''
    oldest = ''
    for k,v in sorted(appYearList.iteritems() ,key=lambda k:k[1],reverse=True):
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
        if patentCluster.has_key(a):
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
    for k,v in sorted(R.iteritems(),key=lambda k:k[1],reverse=True):
        if n < 0:
            break
        print k,'deep Count value =', v 
        topK.append(k)
        mainPathX[k] = []
        mainPathY[k] = []
        for i in range(len(P[k])-1):
            a = P[k][i]
            b = P[k][i+1]
            if pointDict.has_key(a) and pointDict.has_key(b):
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
        
        
    
    
#     for i in P:
#         print i,' = ',P[i]
    
    
    
    
    
    
            
#聚类=============================================================================================
            
#     clusterDict = {}
#     finishDict = {}
#     while True:
#         c = True
#         for i in patentCluster:
#             if finishDict.has_key(i):
#                 continue
#             clusterDict[i] = []
#             (clusterDict,finishDict) = dfs(patentCluster, clusterDict, i, 0, finishDict)
#             print 'happen'
#             c = False
#         if c:
#             break
#         
#     for i in clusterDict:
#         print i,clusterDict[i]
#=========================================================================================
            
            
        
    
    for i in pathDict:
        [a,b] = i.split('$$$$')
        if pointDict.has_key(a) and pointDict.has_key(b):
            if forewordWeight.has_key(a):
                forewordWeight[a] += 1
            else:
                forewordWeight[a] =1
            if backwordWeight.has_key(b):
                backwordWeight[b] += 1
            else:
                backwordWeight[b] = 1
                 
#     maxFore = extractMaxN(forewordWeight, 10)
#     maxBack = extractMaxN(backwordWeight, 10)       
            
            
    x = []
    y = []
    for i in pathDict:
        [a,b] = i.split('$$$$')
        if pointDict.has_key(a) and pointDict.has_key(b):        
            #if (maxFore.has_key(a) or maxBack.has_key(a)) and (maxFore.has_key(b) or maxBack.has_key(b)):
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
    print 'amount line = ',len(mainPathX)
    
    for i in mainPathX:
        color = colorList.pop(0)+'-'
        for j in range(len(mainPathX[i])):
            plt.plot(mainPathX[i][j],mainPathY[i][j],color)
#     for i in range(len(mainPathX)):
#         plt.plot(mainPathX[i],mainPathY[i],'-')
        
    plt.axis([int(appYearList[oldest])-1,int(appYearList[newest])+1,0,vMax+5])
    for x, y in zip(mainPathPointX, mainPathPointY):
        plt.annotate(
            mainPubid.pop(0),
            xy=(x, y),
            xytext=(0, -10),
            textcoords='offset points',
            ha='center',
            va='top')
    plt.show()
    plt.savefig('imageUS.png',format='png')
    
def main():
    name = '人工智能芯片'
    country = 'us_patent'
    pubidList = pubidListExact(name)
    #exactInf(pubidList)
    print len(pubidList)
    if len(pubidList) < 1 :
        print 'we do not find any meaning result for such area'
    else:
        pubidUSPath(pubidList,country)
        relatedPatent(pubidList,country)
        pubidCNPath(pubidList)
main()


    
    
    
    
    
    
    
    
    
    

    