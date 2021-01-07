#encoding=utf-8
'''
Created on 2018��4��17��

@author: zhaoh
'''
'''
技术领域

背景技术

发明内容 实用新型内容

附图说明

具体实施方式  具体实施方案

'''
from lineModifyTool import lineModify
from time import time
from pymongo import MongoClient
import re

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

tech = ['技术领域']
 
back = ['背景技术']

content = ['发明内容',['本发明对','改进'],['本发明','制成'],['本发明','一种'],['上述','缺少'],['本发明','贡献'],'本发明的主要目的'\
           ,'本发明旨在','本发明的目的','本发明的构思','实现本目的的','本发明针对','本发明在于','为了改进',['本发明','要点'],['本发明的任务'],\
           ['本发明','结构'],['本发明','部件'],['合成工艺在'],['构造','原理'],'.内容',['为了','设计'],['发明','技术'],['发明','目的']]

imageDesc = ['附图说明','本发明的详细','图一是','图1','图（1）','图(1)',\
             '附图1','附图1','附图（1）','附图(1)','图二是','图2','图（2）','图(2)',\
             '附图2','附图2','附图（2）','附图(2)','图三是','图3','图（3）','图(3)',\
             '附图3','附图3','附图（3）','附图(3)','附图是','本发明的具体解决方案','实施例','本发明的大致过程','实例',['本发明','实施']]

#operExample = ['具体实施方式','具体实施方案']

rullDict = {'content':content,'imageDesc':imageDesc}


def rullCheck(sentence,tech):
    sentence = sentence

    for rull in tech:
        if type(rull) == list:
            #print 'list rull match'
            current = -1
            listbool = True
            for i in rull:
                if i in sentence:
                    if current < sentence.index(i):
                        current = sentence.index(i)
                    else:
                        listbool = False
                        break
                else:
                    listbool = False
                    break
            if listbool:
                #print ' matching rull is', rull[0],rull[1]
                return True
        else:
            #print 'word rull match'
            if rull in sentence:
                #sub = sentence[ sentence.index(rull) : ]
                return True
    return False
e = open('error.txt','w')

errorCount =0
def descriptionAna(desc,pubid):
    global rullDict, errorCount,e
    descDict = {'tech':[],'back':[],'content':[],'imageDesc':[],'abst':[]}
    nextRullList= ['content','imageDesc']
    curKey = ''
    nextRull = ''
    extendCount = 0
    for i in range(len(desc)):
        if desc[i][:2] == '#!':
            abst = desc[i][2:]
            abst = abst.split('。')
            descDict['abst'] = abst
            continue
        if i == 0:
            if '技术领域' in desc[i] and len(desc[i]) <8:
                extendCount += 1

            curKey = 'tech'
        if i == 1+extendCount:
            curKey = 'back'
            nextRull =nextRullList.pop(0)
        if i > 1:
            if nextRull !='' and curKey !='imageDesc':
                if rullCheck(desc[i], rullDict[nextRull]):
                    curKey = nextRull
                    if nextRull != 'imageDesc':
                        nextRull = nextRullList.pop(0)
        descDict[curKey].append(desc[i])

    if len(descDict['tech']) <1 or len(descDict['back']) <1 or len(descDict['content']) <1 :
        #print errorCount
        e.write('pubid : ' + pubid)
        e.write('技术领域 : ' + '\n')
        e.write('\n'.join(descDict['tech']))
        e.write('\n')
        e.write('\n')
        e.write('背景技术 : ' + '\n')
        e.write('\n'.join(descDict['back']))
        e.write('\n')
        e.write('\n')
        e.write('发明内容 : ' + '\n')
        e.write('\n'.join(descDict['content']))
        e.write('\n')
        e.write('\n')
        e.write('附图说明与实施例 : ' + '\n')
        e.write('\n'.join(descDict['imageDesc']))
        e.write('\n')
        e.write('\n')
        return None
    return descDict


def dataProcess():
    errorList = []
    (conn,db,col) = createMongo('cn_patent')
    (conn,db,insertCol) = createMongo('descTest')
    count = 0
    w = 0
    for data in col.find({'description':{'$exists':True}},{'pubid':1,'abst':1,'claimsList':1,'description':1}).limit(1000).batch_size(10):
        #print w 
        w += 1
        if (not data.has_key('pubid')) or (not data.has_key('abst')) or (not data.has_key('claimsList')) or (not data.has_key('description')):
            continue
        #print 'F'
        pubid = data['pubid']
        abst = data['abst'].encode('utf-8')
        abst = re.split("；|。||\t",abst)
        claims = data['claimsList']
        desc = data['description'].encode('utf-8')
        desc = re.split("；|。||\t",desc)
        tem =  descriptionAna(desc,pubid)
        if tem != None:
            desc = tem
        else:
            errorList.append(pubid)
            continue
        count += 1
        if count % 200 == 0:
            print count,' Done '
        insertData = {}
        insertData['pubid'] = pubid
        insertData['abst'] = abst
        insertData['claims'] = claims
        insertData['desc'] = desc
        
        insertCol.insert(insertData)
    error = open('errorPubid.txt','w')
    error.write('\n'.join(errorList))       
    
    
def extractDesc(path):
    #CN2+   实用新型

    (conn,db,col) = createMongo('descTest')

    o = open('descriptionFormat.txt','w')

            
#descDict = {'tech':[],'back':[],'content':[],'imageDesc':[]}
    errorCount = 0
    
    for data in col.find({},{'claims':1,'abst':1,'desc':1}):
        i = data['desc']
        i['abst'] = data['abst']
        i['claims'] = data['claims']
        o.write('摘要 : ' + '\n')
        o.write('\n'.join(i['abst']))
        o.write('\n')
        o.write('\n')
        o.write('技术领域 : ' + '\n')
        o.write('\n'.join(i['tech']))
        o.write('\n')
        o.write('\n')
        o.write('背景技术 : ' + '\n')
        o.write('\n'.join(i['back']))
        o.write('\n')
        o.write('\n')
        o.write('发明内容 : ' + '\n')
        o.write('\n'.join(i['content']))
        o.write('\n')
        o.write('\n')
        o.write('附图说明与实施例 : ' + '\n')
        o.write('\n'.join(i['imageDesc']))
        o.write('\n')
        o.write('\n')
        if len(i['tech']) <1 or len(i['back']) <1 or len(i['content']) <1 or len(i['imageDesc']) < 1:
            errorCount +=1
            e.write('技术领域 : ' + '\n')
            e.write('\n'.join(i['tech']))
            e.write('\n')
            e.write('\n')
            e.write('背景技术 : ' + '\n')
            e.write('\n'.join(i['back']))
            e.write('\n')
            e.write('\n')
            e.write('发明内容 : ' + '\n')
            e.write('\n'.join(i['content']))
            e.write('\n')
            e.write('\n')
            e.write('附图说明与实施例 : ' + '\n')
            e.write('\n'.join(i['imageDesc']))
            e.write('\n')
            e.write('\n')
    print errorCount
    
def manage():
    dataProcess()
def process():
    path = 'testFile.txt'
    extractDesc(path)   

s = time()
print 'function is beginning'

manage()
process()



  
print 'function is Done'        
e = time()

print 'spend ', e-s,' second'        

        
        
        
        