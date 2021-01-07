#coding=utf-8
'''
Created on 2019��2��22��

@author: zhaoh
'''

from mongoC import mongC
from elasticsearch import Elasticsearch
from jiebaCutPackage import jiebaInterface
import codecs
es = Elasticsearch(['10.0.3.2:9200'])

dataEs = Elasticsearch(['10.0.2.2:9200'])

import re
def getWords(data,op):
    
    input = ''
    if op !='sent':
        (conn,db,col) = mongC.testMongo('test')
        for v in col.find({op:data},{'_id':0,'abst':1}).limit(1):
            if 'abst' in v:
                input = v['abst']
    else:
        input = data
        
    sents = re.split(u'[,|.|，|。]', input)
    tem = ''
    for s in sents:
        if s.isspace() or len(s) <=5 :
            continue
        tem += s
    outWords = {}
    words = jiebaInterface.jiebaCut(tem)
    words = re.sub(r'_[0-9]+', '', words).split(',')
    enWords = re.findall(r'[A-Z]+', tem)
    for w in words:
        if w.isspace() or len(w) < 1 :
            continue
        w = w.decode('utf-8')
        if w in outWords:
            outWords[w] += 1
        else:
            outWords[w] = 1
    for w in enWords:
        if w.isspace() or len(w) < 3:
            continue
        if w in outWords:
            outWords[w] += 1
        else:
            outWords[w] = 1
    
    return outWords

def existJg(w,en,word):
    if w == word['participles'] or en  == word['participles']:
        return True
    
    for i in word['synonym']:
        if w == i or en == i  :
            return True
    
    for i in word['hyponym']:
        if w == i  or en == i:
            return True
    return False

def enWord(w):
    '''
    translate
    '''
    return w 
    
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
        
def searchPart(wordDict):
    query = {'bool':{'should':[]}}
    
    for w in wordDict:
        wordPare = {}
        wordPare[w] = 1
        wordPare[wordDict[w]['en']] = 1
        
        for i in list(wordDict[w]['es']):
            if i in wordPare:
                continue
            wordPare[i] = 0.8
        for i in list(wordDict[w]['mongo']):
            if i in wordPare:
                continue
            wordPare[i] = 0.6
        
        temQuery = {'bool':{'should':[]}}
        for i in wordPare:
            #print i,'  ',
            pare = wordPare[i]
            temQuery['bool']['should'].append({'match_phrase_prefix':{'title':{'query':i,'boost':20*pare}}})
            temQuery['bool']['should'].append({'match_phrase_prefix':{'abst':{'query':i,'boost':5*pare}}})
            temQuery['bool']['should'].append({'match_phrase_prefix':{'claimsList':{'query':i,'boost':5*pare}}})
            temQuery['bool']['should'].append({'match_phrase_prefix':{'techWords':{'query':i,'boost':5*pare}}})
            temQuery['bool']['should'].append({'match_phrase_prefix':{'funcWords':{'query':i,'boost':5*pare}}})
            temQuery['bool']['should'].append({'match_phrase_prefix':{'goods':{'query':i,'boost':5*pare}}})

        query['bool']['should'].append(temQuery)
    #print 'query = ',query
    countryList = ['cn_patent','us_patent','ep_patent','jp_patent','kr_patent','tw_patent','wo_patent','other_patent']
    pubidScore = {}
    for c in countryList:
        print c , 'done '
        res = dataEs.search(index=c, doc_type=c, body={'_source':['title','pubid'],'query':query}, size=50,request_timeout=1000)
        for v in res['hits']['hits']:
            #print v 
            pubid = v['_source']['pubid']
            title = v['_source']['title']
            score = v['_score']
            pubidScore[(pubid,title)] = score
    return pubidScore

f =codecs.open('title.txt','a',encoding='utf-8')   
def similarPatent(data,op):
    print 'function start'
    words = getWords(data, op)
    print 'get words'
    wordDict = wordsExtend(words)
    print 'get extendWords'
    pubidScore = searchPart(wordDict)
    print 'search Finish'
    count = 0
    for k,v in sorted(pubidScore.iteritems(),key=lambda k:k[1],reverse=True):
        count += 1
        if count > 50 :
            break
        (pubid,title) = k
        score = v
        print pubid , title,v
        f.write(pubid+'		'+title+' '+str(v)+'\n')
    f.close()
#     
    
    
data= u'本发明提供一种全球定位系统接收天线,没有粘接剂的漏出,由磁体所产生的吸附可靠,并且,天线主体部的安装坚固。在本发明的GPS接收天线中,在形成凹部2e的底壁2a 上设置连通凹部2e和容纳部2c>的孔2f,通过设在该孔2f中的粘接剂12,来粘接天线主体部4和磁体11,因此,粘接剂12不会漏出到凹部2e外,外观良好,同时,能够可靠地进行磁体11的面吸附。'
op = 'sent'
similarPatent(data,op)
    
    
