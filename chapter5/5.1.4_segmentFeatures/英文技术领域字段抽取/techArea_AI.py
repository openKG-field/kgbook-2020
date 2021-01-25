#coding=utf-8
'''
Created on 2018锟斤拷4锟斤拷26锟斤拷

@author: zhaoh
'''

from pymongo import MongoClient
from elasticsearch import Elasticsearch
import re
from elasticsearch import helpers
import json

import json
def extractTechArea(pubidList):
    o = open('techAreaResult_AInew.txt','w',encoding='utf8')
    (conn,db,col) = createMongo('us_patent')
    count = 0
    #actions = []
    query = {}
    if len(pubidList) >  0 :
        query = {'description':{'$exists':True},'pubid':{'$in':pubidList}}
    else:
        query = {'description':{'$exists':True}}
    for data in col.find(query,{'description':1,'pubid':1,'title':1}).batch_size(30):
        if 'description' not in data or 'pubid' not in data or 'title' not in data:
            continue
        desc = data['description']
        pubid = data['pubid']
        title = data['title']
        area = ''
        desc = re.split(r'[.|;]',desc)
        acount = 0
        

        
        for i in range(len(desc)):
            wordLen = desc[i].strip().split()
            if wordLen < 8 :
                continue
            if len(desc[i]) < 10 or desc[i].isupper():
                continue
            area = desc[i].replace('Field of the Invention','').replace('BACKGROUND OF THE INVENTION','')
            break
        
        
#         if '鎶�鏈鍩�'.decode('utf-8') in desc[0]:
#             area = desc[1]
#         else:
#             if  '鎶�鏈鍩�'.decode('utf-8') in desc[1]:
#                 area = desc[2]
#             else:
#                 area = desc[0] + desc[1]
#         print area
        count += 1
        #US5349079A
        if count % 500 is 0:
            print count,pubid,' Done '
            print area
        body = {'pubid':pubid,'title':title,'techArea':area}
        
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
    print count

def fieldPubids(fieldsName):
    pubidList = []
    (mqconn,mqdb,mqcol) = lcMongo('fieldsIndivideBase')
    for data in mqcol.find({'fieldsName':fieldsName,'type':'en','noisyType':'O'},{'pubid':1}).limit(2000).batch_size(100):
        pubidList.append(data['pubid'])
    return pubidList

def process():
    fieldsName = '区块链'
    pubidList = fieldPubids(fieldsName)
    print len(pubidList)
    extractTechArea(pubidList)
    

process()

    
    
    
    
    
    