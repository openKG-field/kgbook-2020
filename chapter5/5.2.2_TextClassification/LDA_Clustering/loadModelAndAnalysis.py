#encoding=utf-8
'''
Created on 2017年12月12日

@author: zhaoh
'''

from gensim.models import LdaModel
from gensim import models,corpora
from pymongo import MongoClient
from errorFunction import errorType
import os



def unionKeep(doc):
    map = {}
    for i in doc:
        if i in map:
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
        if word in topicContent:
            topicContent[word] += 1
    topicWord[clusterNum] = topicContent
    return topicWord

train = []
pubid = []

def cutOffSum(index, clusterNum, cutOffWord):
    index = int(index)
    global train,pubid
    docContent = train[index]
    pubidContent = pubid[index]

    cutOffContent = cutOffWord[clusterNum]

#     print 'doc = ',docContent
#     print 'pubid = ', pubidContent
#     print 'topic = ',topicContent
#     docContent = unionKeep(docContent)
    countMap = {}
    for i in cutOffContent :
        countMap[i] = 0
    for word in docContent:
        if word in countMap:
            countMap[word] += 1
    #print 'countMap = ',countMap
    count = 0
    for k,v in sorted(countMap.items(), key=lambda k:k[1],reverse=True):
        cutOffContent[k] += 1

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
                if word in rMap:
                    continue
                else:
                    rMap[word] = 0
            else:
                curIndex = i
    return rMap
#k cluster t top words and userid
def clusterPattern(k,t,path):
    #os.makedirs(path)
    global train,pubid
    errorValue = 0
#====================read data from file =============================
    fr = open('smallTest.txt', 'r',encoding='utf8')
    stopwords = ['#$','#*','#@','#!','#&','实用新型']

    tem = []
    for line in fr.readlines():
        head = line[:2]
        line = line[2:]
        if head == '#^':
            #line = line.split()
            pubid.append(line)
        if head == '#*':
            tem = line.split()
        if head == '#!':
            for i in line.split():
                tem.append(i)
            train.append([w for w in tem if w not in stopwords])

#===============train data and save model======================
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
        if currentCluster in clusterMap:
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
    cutOffFile = open(path+'cutOffCluster.txt','w',encoding='utf8')

    outFile = open(path+'clusterResult.txt','w',encoding='utf8')
    for i in clusterMap:
        pubidStr = ''
        for j in clusterMap[i]:
            topicWord = sumPattern(j,i,topicWord)
            cutOffWord = cutOffSum(j,i,cutOffWord)
            pubidStr = pubidStr + '  ' +  pubid[int(j)]
        outFile.write(str(i)+'  ' + pubidStr.replace('\n', '').replace('\r', '')+'\n')

            #return 0
    count = 0
    subClusterFile = open(path+'subClusterFile.txt','w',encoding='utf8')
    #print topicWord
    for i in topicWord:
        subClusterFile.write('cluster : '+ str(count)+'\n')
        count += 1
        for j in i:
            if i[j] == 0:
                continue
            subClusterFile.write('           '+ j+'  ' + str(i[j])+'\n')
    count = 0
    #print cutOffWord
    for i in cutOffWord:
        cutOffFile.write('cluster : '+ str(count)+'\n')
        count += 1
        for j in i:
            if i[j] == 0:
                continue
            cutOffFile.write('           '+ j+'  ' + str(i[j])+'\n')


def main():
#===========local test ========================   
    clusterNum = 10    
    topNum = 20
    path = 'shenjian\\'
#==========search from all database by select_where 
    aimObject = '人工智能'

#==================================================

    clusterPattern(clusterNum,topNum,path)
#==============================================

if __name__ =='__main__':
    main()
