#coding=utf-8
'''
Created on 2018��4��26��

@author: zhaoh
'''

from pymongo import MongoClient
from elasticsearch import Elasticsearch
import re
from elasticsearch import helpers
es = Elasticsearch()
import json

dbName = 'test'
user = 'lyj-rw'
passwd = '123456'
host = '103.31.53.213'
port = 27017

def createMongo(tb):
    global dbName,user,passwd,host,port
    tbName = tb
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[tbName]
    return (conn,db,collection) 

def extractTechArea():
    o = open('techAreaResult.txt','w')
    (conn,db,col) = createMongo('cn_patent')
    count = 0
    actions = []
    for data in col.find({'description':{'$exists':True}},{'description':1,'pubid':1}).batch_size(30):
        desc = data['description']
        pubid = data['pubid']
        p1 = '['
        p2 = '；|。|'.decode('utf-8')
        p3 = '\\n]'
        area = ''
        desc = re.split(p1+p2+p3,desc)
        desc = ' '.join(desc)
        desc = desc.split()
        acount = 0
        for i in range(len(desc)-1):
            acount += 1
            if '技术领域'.decode('utf-8') in desc[i]:
                if len(desc[i+1]) < 7 or not re.match(r'.*[\u4e00-\u9fa5].*|.*[^\x00-\xff].*',desc[i+1]):
                    if i+2 < len(desc) -1 :
                        area = desc[i+2]
                    else:
                        area = desc[i+1]
                else:
                    area = desc[i+1]
                break
            if acount > 5:
                if area == '':
                    area = desc[0]+'\n' + desc[1]
                break
        
#         if '技术领域'.decode('utf-8') in desc[0]:
#             area = desc[1]
#         else:
#             if  '技术领域'.decode('utf-8') in desc[1]:
#                 area = desc[2]
#             else:
#                 area = desc[0] + desc[1]
#         print area
        count += 1
        if count % 500 is 0:
            print count,pubid,' Done '
        body = {'pubid':pubid,'techArea':area}
        o.write(json.dumps(body)+'\n')
#         print area
#         print 
#         #es.update('patentdata', 'cn_patent', pubid, body,request_timeout=500)
#         action = { '_op_type': 'update','_index': 'patentdata','_type': 'cn_patent','_id': pubid,'doc':body}
#         actions.append(action)
#         if count % 2000 is 0 :
#             print count, ' Done'
#             helpers.bulk(es,actions,timeout=500)
#             actions = []
#     if len(actions) > 0:
#         helpers.bulk(es,actions,timeout=500)
extractTechArea()
    

    

    
    
    
    
    
    