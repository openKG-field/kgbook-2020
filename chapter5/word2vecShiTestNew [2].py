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

model_2=word2vec.Word2Vec.load("wc.model")
#server = xmlrpclib.ServerProxy("http://localhost:8888")
#import urllib2

#print("闂備礁鎲＄敮妤冩崲閸岀儑缍栭柟閭﹀枤绾句粙鏌″搴′簽闁搞劍濞婇弻銊モ槈閾忣偄顏�".decode("UTF-8").encode("GBK") + str(sys.getdefaultencoding()))
reload(sys)
sys.setdefaultencoding('utf-8')


def w2v(modelPath, inputWord, topnn):
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
        try:
            a  = model_2.most_similar(temp, u"", topnn)  # 闂佽壈绮炬慨銈咁焽韫囨稑绠婚柛鎰级閻︽敄opn濠电偞鍨堕幖鈺傜濠靛棎锟芥帡宕奸弴鐔峰壆缂備礁顑呴悘婵娿亹閻樼粯鍋ｉ柛銉╂敱鐎氾拷
            #print y2
            print type(a)
            print a
            #print ("闂備礁鎲＄划宀�鎮锔芥櫢闁哄倶鍊栫�氾拷" + temp + "闂備線娼уΛ娆撳垂鐠烘亽锟芥帡宕奸弴鐔峰壆缂備礁顑呴悘婵娿亹閻樼粯鐓熼柕濞垮劚椤忣剟鏌ｉ敂鐣岀疄鐎殿喖鐏氬鍕槈濮樿京宕禱n")
            #word =''
            (conn,db,collection) = commonMongo()
            wordInMongo = {}
            for data in collection.find({'originWord':temp}):
                t = data['applyWord']
                wordInMongo[t] = data['count'] 
            wordMap = {}
            for i in range(len(a)):
                p = a[i][0]
                if wordInMongo.has_key(p):
                    wordMap[p] = wordInMongo[p]
                else:
                    wordMap[p] = 0
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
    errorMap['result'] = rr
    return errorMap




if __name__ == "__main__":
    path = sys.argv[1]
    Preperpare(path)

    
    server = ThreadXMLRPCServer((host, 30004))
    server.register_multicall_functions()
    server.register_function(w2v,'w2v')
    server.register_function(wordTranslateRelate,'wordTranslateRelate')
    print "Listening on port 30004..."
    server.serve_forever()
