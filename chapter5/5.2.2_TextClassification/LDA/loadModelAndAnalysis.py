#encoding=utf-8
'''
Created on 2017年12月12日

@author: zhaoh
'''

from gensim.models import LdaModel
from gensim import models,corpora
from pymongo import MongoClient
from SimpleXMLRPCServer import SimpleXMLRPCServer 
from SocketServer import ThreadingMixIn 
class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer): pass
from errorFunction import errorType
import os

train = []
pubid = []

dbName = 'test'
user = 'lyj-rw'
passwd = '123456'
host = '172.10.30.41'  
port = 27017

def temMongo(tbName):
    global dbName,user,passwd,host,port
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[tbName]
    return (conn,db,collection) 


def unionKeep(doc):
    map = {}
    for i in doc:
        if map.has_key(i):
            continue
        else:
            map[i] = 1
    rDoc = []
    for i in map:
        rDoc.append(i)
    return rDoc

def sumPattern(index,clusterNum,topicWord):
    index = int(index)
    global train,pubid
    docContent = train[index]
    pubidContent = pubid[index]
    topicContent = topicWord[clusterNum]
#     print 'doc = ',docContent
#     print 'pubid = ', pubidContent
#     print 'topic = ',topicContent
    docContent = unionKeep(docContent)
    for word in docContent:
        #word = word.decode('utf-8')
        if topicContent.has_key(word):
            topicContent[word] += 1
    topicWord[clusterNum] = topicContent
    return topicWord

def cutOffSum(index, clusterNum, cutOffWord):
    index = int(index)
    global train,pubid
    docContent = train[index]
    pubidContent = pubid[index]
    print clusterNum
    cutOffContent = cutOffWord[clusterNum]
    print 'cutOffContent : ',cutOffContent
#     print 'doc = ',docContent
#     print 'pubid = ', pubidContent
#     print 'topic = ',topicContent
#     docContent = unionKeep(docContent)
    countMap = {}
    for i in cutOffContent :
        countMap[i] = 0
    for word in docContent:
        if countMap.has_key(word):
            countMap[word] += 1
    #print 'countMap = ',countMap
    count = 0
    for k,v in sorted(countMap.iteritems(), key=lambda k:k[1],reverse=True):
        cutOffContent[k] += 1
        print count
        count += 1
        break
    cutOffWord[clusterNum] = cutOffContent
    return cutOffWord

def wordAbstract(words):
    rMap = {}
    doubleCount = 0
    curIndex = -1
    for i in range(len(words)):
        if words[i] == '"':
            doubleCount += 1
            if curIndex >= 0 and doubleCount %2 == 0:
                word = words[curIndex+1:i]
                if rMap.has_key(word):
                    continue
                else:
                    rMap[word] = 0
            else:
                curIndex = i
    return rMap
#k cluster t top words and userid
def clusterPattern(k,t,select_where,tbName,path):
    #os.makedirs(path)
    global train,pubid
    errorValue = 0
#====================read data from file =============================
#     fr = open('smallTest.txt', 'r')
#     stopwords = ['#$','#*','#@','#!','#&','实用新型']
#     
#     tem = []
#     for line in fr.readlines():
#             head = line[:2]
#             line = line[2:]
#             if head == '#^':
#                 #line = line.split()
#                 pubid.append(line)    
#             if head == '#*':
#                 tem = line.split()
#             if head == '#!':
#                 for i in line.split():
#                     tem.append(i)
#                 train.append([w for w in tem if w not in stopwords])
#===================read data from database ================
    (conn,db,temCollection) = temMongo(tbName)
    try:
        testFile = open(path+'content.txt','w')
        for dataContent in temCollection.find(select_where):
            if dataContent.has_key('pubid') and dataContent.has_key('title_v1') and dataContent.has_key('abst_v1') and dataContent.has_key('claims_v1'):
                if dataContent['country'] !='CN' :
                    continue
                pubid.append(dataContent['pubid'])
                tem = dataContent['title_v1'] +'  ' + dataContent['abst_v1']
                train.append(tem.split())
                testFile.write(tem.encode('utf-8')+' '+'\n')
                
        dictionary = corpora.Dictionary(train)
        corpus = [dictionary.doc2bow(text) for text in train]
        lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=k)
        dictionary = corpora.Dictionary(train)
        topic_list = lda.print_topics(100,t)
            

    #============load model and apply model data ===========================
    
    
    # count = 10
    # for i in train:
    #     print i
    #     count -= 1
    #     if count == 0:
    #         break
    
    #===============cluster all files and mark them with their pubids
        clusterMap  = {}
        for i in range(len(train)):
            doc_bow = dictionary.doc2bow(train[i])  # 文档转换成bow
            doc_lda = lda[doc_bow]  # 得到新文档的主题分布
            # 输出新文档的主题分布
            currentCluster = 0
            currentPersent = 0
            for (cluster,persent) in doc_lda: 
                if currentPersent < persent:
                    currentPersent = persent
                    currentCluster = cluster
            content = str(i)+'  '
            #content = (pubid[i],currentPersent)
            if clusterMap.has_key(currentCluster):
                clusterMap[currentCluster].append(content)
            else:
                clusterMap[currentCluster] = []
                clusterMap[currentCluster].append(content)
                
        #print len(clusterMap)
        topicWord = []
        cutOffWord = []
        for topic in topic_list:
            for i in topic:
                if type(i) == int:
                    continue
                temMap = wordAbstract(i)
                #print map
                #print 'words length = ',len(map)
                topicWord.append(temMap)
        for topic in topic_list:
            for i in topic:
                if type(i) == int:
                    continue
                temMap = wordAbstract(i)
                #print map
                #print 'words length = ',len(map)
                cutOffWord.append(temMap)
        #print topicWord
        cutOffFile = open(path+'cutOffCluster.txt','w')
        
        outFile = open(path+'clusterResult.txt','w')
        for i in clusterMap:
            pubidStr = ''
            for j in clusterMap[i]:
                topicWord = sumPattern(j,i,topicWord)
                cutOffWord = cutOffSum(j,i,cutOffWord)
                pubidStr = pubidStr + '  ' +  pubid[int(j)]
            outFile.write(str(i)+'  ' + pubidStr.replace('\n', '').replace('\r', '').encode('utf-8')+'\n')
            
                #return 0 
        count = 0
        subClusterFile = open(path+'subClusterFile.txt','w')
        #print topicWord
        for i in topicWord:
            subClusterFile.write('cluster : '+ str(count)+'\n')
            count += 1
            for j in i:
                if i[j] == 0:
                    continue
                subClusterFile.write('           '+ j.encode('utf-8')+'  ' + str(i[j])+'\n')
        count = 0
        #print cutOffWord
        for i in cutOffWord:
            cutOffFile.write('cluster : '+ str(count)+'\n')
            count += 1
            for j in i:
                if i[j] == 0:
                    continue
                cutOffFile.write('           '+ j.encode('utf-8')+'  ' + str(i[j])+'\n')
    except KeyError:
        errorValue = 2
    except UnicodeError:
        errorValue = 6
    except IndexError:
        errorValue = 3
    except:
        errorValue = 1                      
    finally:
        errorMap = {"errorCode": str(errorValue), "errorDesc": errorType(errorValue)}
        return errorMap 

def main():
#===========local test ========================   
    clusterNum = 10    
    topNum = 20
    path = 'shenjian\\'
#==========search from all database by select_where 
    aimObject = '人工智能'
    tbName = 'v4all_v2'
    select_where = {"$or":[{"abst":{"$regex":aimObject}}]}
#==========search from tem database by select where
#     aimObject = 'zhy123'
#     tbName = 'temDataBean'
#     select_where = {'userid':aimObject}
#==================================================

    clusterPattern(clusterNum,topNum,select_where,tbName,path)
#==============================================
#     server = ThreadXMLRPCServer(('172.10.30.41',30010))
#     server.register_multicall_functions()
#     server.register_function(clusterPattern,'clusterPattern')
#     print "Listening on port 30010..."
#     server.serve_forever()
if __name__ =='__main__':
    main()
