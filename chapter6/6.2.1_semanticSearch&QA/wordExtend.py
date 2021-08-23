#coding=utf-8

import codecs
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

import re
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from elasticsearch import Elasticsearch,helpers


es = Elasticsearch()

import re

def wordsExtend(words):
    (conn,db,col) = mongC.mqpatMongo('fieldsWord')
    wordDict  = {}
    for w in words:
        en = enWord(w)
        extendWords = {}
        esList = set()
        mongoList = set()
        '''
        es 同义词
        mongo 同位，下位词
        translate
        '''
        #es 同义词
        index = 'worddescription'
        doc_type = 'baiduwiki'
        body = {'_source':['extendWords'],'query':{'bool':{'should':[{'term':{'tagName':w}},{'term':{'tagName':en}}]}}}
        
        res = es.search(index, doc_type, body,size=1000)
        for v in res['hits']['hits']:
            data = v['_source']
            esList = esList| set(data['extendWords'])
        
        #mongo 拓展词
        for data in col.find({},{'words':1,'_id':0}).batch_size(100):
            if 'words' not in data:
                continue
            for word in data['words']:
                #print 'word = ',word
                if type(word) is not dict:
                    continue
                #print 'word = ', word
                if existJg(w,en,word):
                    mongoList = mongoList | set(word['hyponym']) | set(word['synonym']) | set([word['participles']])
        extendWords['es'] = esList
        extendWords['mongo'] = mongoList
        extendWords['en'] = en
        wordDict[w] = extendWords
    return wordDict
