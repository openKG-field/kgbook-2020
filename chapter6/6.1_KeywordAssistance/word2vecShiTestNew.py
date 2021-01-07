#!/usr/bin/env python
# -*- coding: utf-8 -*-
#encoding=utf-8
import sys
import os
from gensim.models import word2vec
from pymongo import MongoClient
from SimpleXMLRPCServer import SimpleXMLRPCServer 
from SocketServer import ThreadingMixIn 
class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer): pass
from errorFunction import errorType
import shutil
import httplib
import md5
import urllib
import random

currDir = os.path.dirname(__file__)
if currDir == '':
    currDir = '.'
model_2=word2vec.Word2Vec.load(currDir + "/wc.model")

model_en = word2vec.Word2Vec.load(currDir + '/Word2vecEnglish.model')
#server = xmlrpclib.ServerProxy("http://localhost:8888")
#import urllib2

#print("闂備礁鎲＄敮妤冩崲閸岀儑缍栭柟閭﹀枤绾句粙鏌″搴′簽闁搞劍濞婇弻銊モ槈閾忣偄顏�".decode("UTF-8").encode("GBK") + str(sys.getdefaultencoding()))
reload(sys)
sys.setdefaultencoding('utf-8')
#print("濠电儑绲藉ù鍌炲窗濡ゅ懎鏋侀柤娴嬫櫇绾句粙鏌″搴′簽闁搞劍濞婇弻銊モ槈閾忣偄顏�".encode("GBK") + str(sys.getdefaultencoding()))


dbName = 'test'
user = 'lyj-rw'
passwd = '123456'

host = 'MQ01'  
port = 27017


dellHost = 'MQ03'
lcHost = 'MQ01'
hv1Host = 'MQ01'
hv2Host = 'MQ02'

def Preperpare(path):
    global user, passwd,host,port,dbName
    f = open(path)
    for line in f:
        if 'Database Information' in line:
            continue
        if line.isspace():
            continue
        [head,body] = line.split('=')
        head = head.strip()
        body = body.strip()
        if head == 'dbName':
            dbName = body
        if head == 'user':
            user = body
        if head == 'passwd':
            passwd = body
        if head == 'host':
            host = body
        if head == 'port':
            port = int(body)
        if head == 'dellHost':
            dellHost = body
        if head =='lcHost':
            lcHost = body
        if head == 'hv1Host':
            hv1Host = body
        if head == 'hv2Host':
            hv2Host = body

def commonMongo():
    global dbName,user,passwd,host,port
    
    tbName = 'commonWordsDataBean'
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[tbName]
    return (conn,db,collection)        


def wordMongo(tb):
    #host = lcHost
    host = hv1Host  
    dbName = 'mqpat'
    user = 'mqpat-rw'
    passwd = 'mq2019'
    port = 27017
    myTbNme = tb
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[myTbNme]
    return (conn,db,collection) 


def pwd():
    return os.getcwd()

# 闂備礁鎲＄敮妤呫�冮崨鏉戝惞妞ゆ挶鍨圭粻浼存煕閵夋垵鎳忓В搴ㄦ⒑閻戔晜娅撻柛鐘崇墱缁辩偛顓奸崱娆屾灃濡炪倖鎸炬慨鐢告偩闁秵鐓曢柟閭﹀墯閸ｈ銇勯弮鎾村
def ls(directory=None):
    if directory is None:
        directory = pwd()
    try:
        return os.listdir(directory)
    except OSError as e:
        return e
    
def translation_function(type, q):
    if type == '1':
        fromLang = 'en'
        toLang = 'zh'
    else:
        fromLang = 'zh'
        toLang  = 'en'
    appid = '20171016000088616'
    secretKey = '5xymb5TwGd8nKaCFEnf9'
    #print q

    httpClient = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    try:
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        #response鏄疕TTPResponse瀵硅薄
        response = httpClient.getresponse()
        message = response.read()
        begin = message.index('dst')+6
        end = len(message)-4
        outputResult = message[begin:end].decode('unicode_escape').encode('utf-8')
        #print outputResult
        return outputResult
    except Exception, e:
        print e
        return q
    finally:
        if httpClient:
            httpClient.close()

def w2v(modelPath, inputWord, topnn,typeCode=1):
    global model_2,model_en
    if typeCode is 1:
        resultword = inputWord.split(",")
        resultList  = []
        count = 0
        for word in resultword:
            wordList = []
            errorValue = 0
            count +=1
            temp = word.decode("UTF-8")
            wordList.append(temp+'_' + str(count) + ',')
            #model_2 = word2vec.Word2Vec.load(modelPath)  # 闂佽崵濮撮鍛村疮娴兼潙鏋侀柕鍫濇啒閻旂厧鐏崇�规洖娴勯幏鐑芥晸閿燂拷
            try:
                a  = model_2.most_similar(temp, u"", topnn)  # 闂佽壈绮炬慨銈咁焽韫囨稑绠婚柛鎰级閻︽敄opn濠电偞鍨堕幖鈺傜濠靛棎锟芥帡宕奸弴鐔峰壆缂備礁顑呴悘婵娿亹閻樼粯鍋ｉ柛銉╂敱鐎氾拷
                #print y2
                #print type(a)
                #print a
                #print ("闂備礁鎲＄划宀�鎮锔芥櫢闁哄倶鍊栫�氾拷" + temp + "闂備線娼уΛ娆撳垂鐠烘亽锟芥帡宕奸弴鐔峰壆缂備礁顑呴悘婵娿亹閻樼粯鐓熼柕濞垮劚椤忣剟鏌ｉ敂鐣岀疄鐎殿喖鐏氬鍕槈濮樿京宕禱n")
                #word =''
                (conn,db,collection) = wordMongo('relatedWord')
                wordInMongo = {}
                for data in collection.find({'org':temp}):
                    t = data['words']
                    for i in t:
                        o = i.replace("'",'')
                        wordInMongo[o] = t[i]
                wordMap = {}
                for i in range(len(a)):
                    p = a[i][0]
                    #print 'w2v word = ',p,[p]
                    if wordInMongo.has_key(p):
                        wordMap[p] = wordInMongo[p]
                    else:
                        wordMap[p] = 0
                for k,v in sorted(wordMap.iteritems(), key=lambda k:k[1],reverse=True):
                    #print k,v 
                    wordList.append(k+'_'+str(count)+',')
    
        
                    
            except KeyError:
                errorValue = 2
            except:
                errorValue = 1
            finally:
                listStr = ''.join(wordList)
                print listStr
            resultList.append(listStr)
    else:
        resultword = inputWord.split(",")
        resultList  = []
        count = 0
        for word in resultword:
            wordList = []
            errorValue = 0
            count +=1
            temp = word.decode("UTF-8")
            wordList.append(temp+'_' + str(count) + ',')
            #model_2 = word2vec.Word2Vec.load(modelPath)  # 闂佽崵濮撮鍛村疮娴兼潙鏋侀柕鍫濇啒閻旂厧鐏崇�规洖娴勯幏鐑芥晸閿燂拷
            try:
                a  = model_en.most_similar(temp, u"", topnn)  # 闂佽壈绮炬慨銈咁焽韫囨稑绠婚柛鎰级閻︽敄opn濠电偞鍨堕幖鈺傜濠靛棎锟芥帡宕奸弴鐔峰壆缂備礁顑呴悘婵娿亹閻樼粯鍋ｉ柛銉╂敱鐎氾拷
                #print y2
                #print type(a)
                #print a
                #print ("闂備礁鎲＄划宀�鎮锔芥櫢闁哄倶鍊栫�氾拷" + temp + "闂備線娼уΛ娆撳垂鐠烘亽锟芥帡宕奸弴鐔峰壆缂備礁顑呴悘婵娿亹閻樼粯鐓熼柕濞垮劚椤忣剟鏌ｉ敂鐣岀疄鐎殿喖鐏氬鍕槈濮樿京宕禱n")
                #word =''
                (conn,db,collection) = wordMongo('relatedWord')
                wordInMongo = {}
                for data in collection.find({'org':temp}):
                    t = data['words']
                    for i in t:
                        o = i.replace("'",'')
                        #print 'relatedWord = ',i,[i]
                        wordInMongo[o] = t[i] 
                wordMap = {}
                for i in range(len(a)):
                    p = a[i][0]
                    #print 'w2v word = ',p,[p]
                    if wordInMongo.has_key(p):
                        wordMap[p] = wordInMongo[p]
                    else:
                        wordMap[p] = 0
                        
                #print wordMap
                for k,v in sorted(wordMap.iteritems(), key=lambda k:k[1],reverse=True):
                    wordList.append(k+'_'+str(count)+',')
            except KeyError:
                errorValue = 2
            except:
                errorValue = 1
            finally:
                listStr = ''.join(wordList)
                print listStr
            resultList.append(listStr)        
    errorMap = {"errorCode": str(errorValue), "errorDesc": errorType(errorValue)}
    rr = ''.join(resultList)
    rr = rr.replace('$',' ')
    errorMap['result'] = rr
    return errorMap


def wordTranslateRelate(modelPath, inputWord, topnn):
    global model_2
    resultword = inputWord.split(",")
    resultList  = []
    count = 0
    for word in resultword:
        wordList = []
        errorValue = 0
        count +=1
        temp = word.decode("UTF-8")
        wordList.append(temp+'_' + str(count) + ',')
        #model_2 = word2vec.Word2Vec.load(modelPath)  # 闂佽崵濮撮鍛村疮娴兼潙鏋侀柕鍫濇啒閻旂厧鐏崇�规洖娴勯幏鐑芥晸閿燂拷
        #try:
        if True:
            a  = model_2.most_similar(temp, u"", topnn)  # 闂佽壈绮炬慨銈咁焽韫囨稑绠婚柛鎰级閻︽敄opn濠电偞鍨堕幖鈺傜濠靛棎锟芥帡宕奸弴鐔峰壆缂備礁顑呴悘婵娿亹閻樼粯鍋ｉ柛銉╂敱鐎氾拷
            #print y2
#             print type(a)
#             print a
            #print ("闂備礁鎲＄划宀�鎮锔芥櫢闁哄倶鍊栫�氾拷" + temp + "闂備線娼уΛ娆撳垂鐠烘亽锟芥帡宕奸弴鐔峰壆缂備礁顑呴悘婵娿亹閻樼粯鐓熼柕濞垮劚椤忣剟鏌ｉ敂鐣岀疄鐎殿喖鐏氬鍕槈濮樿京宕禱n")
            #word =''
            (conn,db,collection) = commonMongo()
            wordInMongo = {}
            for data in collection.find({'originWord':temp}):
                t = data['applyWord']
                wordInMongo[t] = data['count'] 
            wordMap = wordInMongo
            for i in range(len(a)):
                p = a[i][0]
                if wordInMongo.has_key(p):
                    continue
                else:
                    wordMap[p] = 0
            for k,v in sorted(wordMap.iteritems(), key=lambda k:k[1],reverse=True):
                wordList.append(k+'_'+str(count)+',')
                en = translation_function('2', k.encode('utf-8'))
                if en == k or len(en) < 2 or en.isspace():
                    continue
                else:
                    wordList.append(en+'_'+str(count)+',')
    
        try:
            print         
        except KeyError:
            errorValue = 2
        except:
            errorValue = 1
        finally:
            listStr = ''.join(wordList)
        resultList.append(listStr)
    errorMap = {"errorCode": str(errorValue), "errorDesc": errorType(errorValue)}
    rr = ''.join(resultList)
    errorMap['result'] = rr
    return errorMap
import numpy as np
def wordArray(word):
    a = '-1'
    try:
	a = model_2[word].tolist()
    except:
	pass
    return a

def wordsArray(words):
    print 'array list vector begin'
    tem = {}
    for w in words:
	t = []
	try :
	    t = model_2[w].tolist() 	
	except:
	    pass
	finally:
	    if t != []:
		tem[w] = t
    print 'len return = ',len(tem)
    return tem
if __name__ == "__main__":
    path = sys.argv[1]
    Preperpare(path)
#w2v(modelPath, inputWord, topnn)
    
    server = ThreadXMLRPCServer((host, 30004))
    server.register_multicall_functions()
    # 根据中/英文 查询 model中的 数据，并返回topN结果。 流程中会参考 mongo内存的表，即 考虑用户点击量，重新调整排序
    server.register_function(w2v,'w2v')
    # 翻译词 ， 将翻译结果返回
    server.register_function(wordTranslateRelate,'wordTranslateRelate')
    # 将输入的词 带入 model中 返回 向量结果
    server.register_function(wordArray,'wordArray')
    # 将输入的 词组 带入 model中， 结果 为 map{w1:v1,w2:v2 ...} 格式
    server.register_function(wordsArray,'wordsArray')
    print "Listening on port 30004..."
    server.serve_forever()
