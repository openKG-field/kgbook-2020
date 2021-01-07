#coding=utf-8
'''
Created on 2018��6��1��

@author: zhaoh
'''

from elasticsearch import Elasticsearch
import json
import time
es = Elasticsearch()

def processLog(spendTime,amount):
    average = 1000
    seconds = float(amount)/float(average)*float(spendTime)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    
    return ("%02d 小时:%02d 分钟:%02d 秒" % (h, m, s))




def experimentData():
    appYearRange = [1990,2017]
    
    begin = appYearRange[0]
    end = appYearRange[1]
    
    o = open('enTechAreaExperimentData.txt','w')
    
    i = begin
    
    descMiss = 0
    
    startTime = time.time()
    
    while i < end:
        appYear = str(i)
        query = {'bool':{'must':[{'match_phrase':{'appYear':appYear}},{'exists':{'field':'description'}}]}}
        source = ['description','title','pubid','appYear']
        body = {'_source':source,'query':query}
        res = es.search('patentdata', 'us_patent', body, size= 10,request_timeout=500)
        for data in res['hits']['hits']:
            curData = data['_source']
            
            o.write(json.dumps(curData)+'\n')
            
            if 'description' not in curData:
                descMiss += 1
        cur = time.time()
        
        
        predictTime =  processLog(float(cur-startTime), end-i)
        
        startTime = cur
        
        rate = float(i-begin+1)/float(end-begin)
            
        print"完成度为：%.2f%%"  %(rate*100),' 预计耗时 ', predictTime 
        i = i+1
    print descMiss,' 没有说明文' 
experimentData()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    