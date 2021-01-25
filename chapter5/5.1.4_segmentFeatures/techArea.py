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

def load_data(path):
    datas = []
    count = 0
    header = []
    with open(path,'r',encoding='utf8') as f :
        for line in f :
            line = line.strip().split('\t')
            count += 1
            if count == 1 :
                header = line
            else:
                data = {}
                for i in range(len(line)) :
                    data[header[i]] = line[i]
                datas.append(data)
    return datas

def extractTechArea(path):
    o = open('techAreaResult.txt','w',encoding='utf8')
    datas =load_data(path)
    count = 0
    for data in datas :
        count += 1
        desc = data['description']
        pubid = data['pubid']
        p1 = '['
        p2 = '；|。|'
        p3 = '\\n]'
        area = ''
        desc = re.split(p1+p2+p3,desc)
        desc = ' '.join(desc)
        desc = desc.split()
        acount = 0
        for i in range(len(desc)-1):
            acount += 1
            if '技术领域' in desc[i]:
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

        count += 1
        if count % 500 == 0:
            print (count,pubid,' Done ')
        body = {'pubid':pubid,'techArea':area}
        o.write(json.dumps(body)+'\n')

path = './/..//data//test.txt'
extractTechArea(path)
    

    

    
    
    
    
    
    