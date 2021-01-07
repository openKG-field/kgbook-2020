#coding=utf-8
'''
Created on 2019��1��30��

@author: zhaoh
'''

from elasticsearch import Elasticsearch
es = Elasticsearch(['10.0.2.2:9200'])
from jiebaCutPackage import jiebaInterface
 

def freCount (words,sent):
    count = 0 
    for w in words:
	if type(sent) is list:
	    for i in sent:
		if w in i :
		    count += 1
		    break
	else:
	    if w in sent:
		count += 1
		continue
    return count 

 
def loadWords(path):
    word = {}
    f = open(path,'r')
    for i in f:
        if len(i) < 1 or i.isspace():
            continue
        i = i.replace('\n','')
        i = i.replace('\r','')
        word[i.decode('utf-8')] = 1
    return word
    
#sentence = u'一种纤维增强型气凝胶隔热材料，其中，所述纤维增强型气凝胶隔热材料包含二氧化硅气凝胶和纤维材料，所述二氧化硅气凝胶以二氧化硅水溶胶为原料，通过添加催化剂来制备。'
#sentence = u'终端向移动终端发送请求消息，其中，所述请求消息用于请求获取所述移动终端的移动国家号码MCC、移动网号MNC和国际移动用户识别码IMSI；所述终端接收所述移动终端发送的包含所述移动终端的MCC、MNC和IMSI的回复消息；所述终端根据所述移动终端的MCC、MNC和IMSI进行网络注册。'
sentence = u'本发明提供一种全球定位系统接收天线,没有粘接剂的漏出,由磁体所产生的吸附可靠,并且,天线主体部的安装坚固。在本发明的GPS接收天线中,在形成凹部2e的底壁2a 上设置连通凹部2e和容纳部2c的孔2f,通过设在该孔2f中的粘接剂12,来粘接天线主体部4和磁体11,因此,粘接剂12不会漏出到凹部2e外,外观良好,同时,能够可靠地进行磁体11的面吸附。'
#sentence = u'一种全球定位系统(GPS)天线结构，其特征是包括：一天线座（32），具有一弧形表面，所述天线座包括;一接收天线（31），用以接收一全球定位系统(GPS)信号；及一配重块（33），提供一重力，所述配重块与所述接收天线配置于所述天线座之两端；以及一基座（34），具有一弧形内壁，所述弧形表面可滑动地配置于所述弧形内壁，使所述天线座可于所述基座内滚动'

#sentence = u'一种新型卡片，包括卡片本体，其特征在于，所述的卡片本体呈弧形形状，所述的卡片本体两端设有防滑齿，所述的卡片本体上设有铆接螺母孔。'
#sentence = u'制备'
#words = ''
words = jiebaInterface.jiebaCut(sentence).split(',')
import re 
enWords = re.findall(r'[a-zA-Z]+', sentence)

path = 'intendWords.txt'
intendWords = loadWords(path)
mustTitle = {}
for w in intendWords:
    mustTitle[w] = 1

mustQuery = {'bool':{'should':[]}}

for w in mustTitle:
    if w in sentence:
        mustQuery['bool']['should'].append({'match_phrase':{'title':w}})
    

wordFre = {}
for w in words:
    if len(w) < 1 or w.isspace() or '_' not in w :
        continue
    [word,fre] = w.split('_')
    if word in wordFre:
        wordFre[word] += int(fre)
    else:
        wordFre[word] = int(fre)

for en in enWords:
    if en in wordFre:
	wordFre[en] += 1
    else:
	wordFre[en] =  1
#wordFre[u'制备'] = 2
#for w in wordFre:
#    print 'word = ',w

#wordFre['GPS'] = 3 
query = {'bool':{'should':[]}}
for k,v in sorted(wordFre.iteritems(),key=lambda k:k[1],reverse=True):
    print 'search word = ',k
    #if v < 2 :
    #    break
    sub = {'bool':{'should':[{'match_phrase':{'title':{'query':k,'boost':5}}},
                             {'match_phrase':{'abst':{'query':k,'boost':3}}},
                                {'match_phrase':{'claimsIndList':{'query':k,'boost':2}}},
                                {'match_phrase':{'claimsList':{'query':k,'boost':1}}}
     
                                ]}}
    query['bool']['should'].append(sub)

tem = {'bool':{'should':[{'match_phrase':{'title':{'query':u'重力','boost':5}}},
                             {'match_phrase':{'abst':{'query':u'重力','boost':3}}},
                                {'match_phrase':{'claimsIndList':{'query':u'重力','boost':2}}},
                                {'match_phrase':{'claimsList':{'query':u'重力','boost':1}}}
				]}}
searchQuery = {'bool':{'must':[]}}
searchQuery['bool']['must'].append(query)
searchQuery['bool']['must'].append(mustQuery)
#searchQuery['bool']['must'].append(tem)
#query = {'match_phrase':{'title':'制'}}

#searchQuery = {'bool': {'must': [{'bool': {'should': [{'match_phrase': {'area': '\xe4\xbf\xa1\xe6\x81\xaf\xe5\xa4\x84\xe7\x90\x86'}}, {'match_phrase': {'area': u'highLight'}}, {'match_phrase': {'area': '\xe8\xb4\xb8\xe6\x98\x93\xe4\xbf\xa1\xe6\x81\xaf'}}, {'match_phrase': {'area': u'span'}}, {'match_phrase': {'area': u'class'}}]}}, {'bool': {'should': [{'match_phrase': {'area': u'\u663e\u793a'}}, {'match_phrase': {'area': u'\u4f9b\u5e94'}}, {'match_phrase': {'area': u'\u753b\u9762'}}, {'match_phrase': {'area': u'\u7ef4\u62a4'}}, {'match_phrase': {'area': u'\u6267\u884c'}}, {'match_phrase': {'area': u'\u4efb\u610f'}}]}}, {}, {'bool': {'should': [{'match_phrase': {'area': u'\u8d38\u6613\u4fe1\u606f'}}, {'match_phrase': {'area': u'\u4fe1\u606f\u5904\u7406'}}]}}]}}


body = {'_source':['pubid','title','abst','claimsList'],'query':searchQuery}
index = doc_type = 'cn_patent'
res = es.search(index=index, body=body, size=1000,request_timeout=100)
pubidFre = {}
o = open('title.txt','w')
for v in res['hits']['hits']:
    data = v['_source']
    pubid = data['pubid']
    title = ''
    tem = 0
    print data['pubid'], ' = ' ,data['title']
#    if 'title' in data:
#	tem += freCount(wordFre,data['title'])
#	title = data['title']
#    if 'abst' in data:
#	tem += freCount(wordFre,data['abst'])
#    if 'claimsList' in data:
#	tem += freCount(wordFre,data['claimsList'])
#    pubidFre[(pubid,title)] = tem
#count = 0
#for k,v in sorted(pubidFre.iteritems(),key=lambda k:k[1],reverse=True):
#    (pubid,title) = k 
#    print pubid , ' = ' ,title
#    count += 1
#    if count > 100 :
#	break






