#encoding=utf-8
'''
Created on 2017��12��27��

@author: zhaoh
'''
from pymongo import MongoClient
from audioop import reverse




dbName = 'test'
user = 'lyj-rw'
passwd = '123456'
host = '172.10.30.41'  
port = 27017

def createMongo():
    global dbName,user,passwd,host,port
    tbName = 'v4all_v2'
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[tbName]
    return (conn,db,collection) 

def fwordsReview(select_where,filePath):
    (conn,db,collection) = createMongo()
    wordsFile = open(filePath,'w')
    wordsDict = {}
    for data in collection.find(select_where):
        words = data['fsentences']
        words = words.split()
        for k in words:
            if wordsDict.has_key(k):
                wordsDict[k] += 1
            else:
                wordsDict[k] = 1   
    for k,v in sorted(wordsDict.iteritems(),key=lambda k:k[1],reverse=True):
        wordsFile.write(k.encode('utf-8') + '  ' + str(v) + '\n')
        print k 

select_where = {'abst':{'$regex':'人工智能'}}
filePath = 'fwordsDict.txt'
print 'function is beginning'
fwordsReview(select_where, filePath)
print 'function is done'
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    