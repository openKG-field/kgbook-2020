#encoding=utf-8
'''
Created on 2017��11��14��

@author: zhaoh
'''
import sys
from pymongo import MongoClient
#from ProcessForSimilar import readDataOutTemMap
from SimpleXMLRPCServer import SimpleXMLRPCServer 
from SocketServer import ThreadingMixIn 
class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer): pass
from errorFunction import  errorType
from elasticsearch import Elasticsearch
from cartesian import Cartesian
es = Elasticsearch()

words = []

step = 0
result = []
dbName = 'test'
user = 'lyj-rw'
passwd = '123456'
host = '119.18.207.121'    

dellHost = '10.0.3.2'
lcHost = '10.0.4.2'
hv1Host = '10.0.1.2'
hv2Host = '10.0.2.2'
port = 27017
areaList = ['title','abst','claimsList']
wordsLocation = {}

def temMongo():
    global dbName,user,passwd,host,port
    myTbNme = 'temDataBean'
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[myTbNme]
    return (conn,db,collection) 


def synonymWords(m):
    wordList = []
    return [m]
    res = es.search('synonym_dict','cn_patent',{'_source':['synonym'],'query':{'match_phrase':{'synonym':m}}})
     
    for data in res['hits']['hits']:
        if not data['_source'].has_key('synonym'):
            continue
        wordList = data['_source']['synonym']
    wordList.append(m)
    return wordList
def createMongo():
    global dbName,user,passwd,host,port
    tbName = 'v4all_v2'
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[tbName]
    return (conn,db,collection) 

def myMongo():
    global dbName,user,passwd,host,port
    myTbNme = 'wordPatDataBean'
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[myTbNme]
    return (conn,db,collection) 

def tbMong(tb):
    global dbName,user,passwd,host,port
    myTbNme = tb 
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[myTbNme]
    return (conn,db,collection) 



def areaSelect(m):
    global es
    global words,areaList,wordsLocation
    #areaList = ['title','abst','claimsList','description']
    
    resultList = []
    temList = []
    #print m 
    #print wordsLocation
    if wordsLocation == {}:
        temList = areaList
    else:
        if m.decode('utf-8') in wordsLocation:
            #print 'found'
            temList = wordsLocation[m.decode('utf-8')]
        elif m in wordsLocation :
            temList = wordsLocation[m]
        else:
            print m,[m],'not exists'
            temList = areaList
    
    #print 'm = ',m,'temList : ',temList 
    #print temList
    #print m, temList
    if '*' in m :
        #mList = esWildcardWords(m)
#         for i in mList:
#             words.append(i)
        
        m = m.lower().replace('*','')
        for i in temList:
            #print i 
            tem = {'match_phrase_prefix':{i:m}}
            resultList.append(tem)
            
    if '?' in m :
        m = m.lower()
        for i in temList:
            tem = {'wildcard':{i:m}}
            resultList.append(tem)
    else:
        wordList = []
#====================同义词================================================================
        wordList = synonymWords(m)
        for word in wordList:
            words.append(word)
            for i in temList:
                #print i 
                tem = {'match_phrase':{i:word}}
                resultList.append(tem)
    return resultList

def esWildcardWords(m):
    global es
    words = []
    body = {'_source':['word'],'query':{'wildcard':{'word':m}}}
    res = es.search('wildcardword','ts',body,size=800000,request_timeout=500)
    for data in res['hits']['hits']:
        if data['_source'].has_key('word'):
            words.append(data['_source']['word'])
    #print 'wildcard words = ',words
    return words

def slopAreaSelect(m,c):
    global words,areaList,wordsLocation
    #print 'c = ',c
    
    temList = []
    #print m
    #print wordsLocation
    if wordsLocation == {}:
        temList =areaList
    else:
        if m.decode('utf-8') in wordsLocation:
            #print 'found'
            temList = wordsLocation[m.decode('utf-8')]
        elif m in wordsLocation :
            temList = wordsLocation[m]
        else:
            print m,[m],'not exists'
            temList = areaList
    
    resultList = []
    if '*' in m:
        
        wordList = m.split()
        combineList = []
        for word in wordList:
            if '*' in word:
                combineList.append(esWildcardWords(word))
            else:

                subwords = synonymWords(m)
                if len(subwords) < 1:
                    subwords = [word]
                for i in subwords:
                    words.append(i)
                subwords.append(word)
                combineList.append(subwords)
                
        car = Cartesian(combineList)
        #print 'combineList = ',combineList
        t = car.assemble()
        for sub_comb in t:
            sub_comb = ' '.join(sub_comb)
            for i in temList:
                Tem = {'bool':{'must':[]}}
                tem = {'match_phrase':{i:{'query':sub_comb,'slop':c}}}
                Tem['bool']['must'].append(tem)
                vlist = sub_comb.split()
                for v in vlist:
                    vtem = {'match_phrase':{i:v}}
                    Tem['bool']['must'].append(vtem)
                
                resultList.append(Tem)
    else:
        wordList = m.split()
        combineList = []
        for word in wordList:
#=====================同义词=============================
            subwords = synonymWords(m)
            if len(subwords) < 1:
                subwords = [word]
            else:
                subwords.append(word)
            for i in subwords:
                words.append(i)
            subwords = [word]
            combineList.append(subwords)
        car = Cartesian(combineList)
        t = car.assemble()
        for sub_comb in t:
            sub_comb = ' '.join(sub_comb)
            for i in temList:
                Tem = {'bool':{'must':[]}}
                tem = {'match_phrase':{i:{'query':sub_comb,'slop':c}}}
                Tem['bool']['must'].append(tem)
                vlist = sub_comb.split()
                for v in vlist:
                    vtem = {'match_phrase':{i:v}}
                    Tem['bool']['must'].append(vtem)
                
                resultList.append(Tem)
    return resultList
    
    
def orOperator(m1, m2):
    global words
    
    if type(m1) != dict and type(m2) != dict:
        words.append(m1)
        words.append(m2)
        resultList = areaSelect(m1)
        query = {'bool':{'should':[]}}
        for i in resultList:
            query['bool']['should'].append(i)
        resultList = areaSelect(m2)
        for i in resultList:
            query['bool']['should'].append(i)
        return query
    
    if type(m1) !=dict and type(m2) == dict:
        words.append(m1)
        resultList = areaSelect(m1)
        if 'should' in m2['bool']:
            for i in resultList:
                m2['bool']['should'].append(i)
            return m2
        else:
            query = {'bool':{'should':[]}}
            for i in resultList:
                query['bool']['should'].append(i)
            query['bool']['should'].append(m2)
            return query
            
    if type(m2) !=dict and type(m1) == dict:
        words.append(m2)
        resultList = areaSelect(m2)
        if 'should' in m1['bool']:
            for i in resultList:
                m1['bool']['should'].append(i)
            return m1
        else:
            query = {'bool':{'should':[]}}
            for i in resultList:
                query['bool']['should'].append(i)
            query['bool']['should'].append(m1)
            return query
          
    if type(m1) == dict and type(m2) == dict:
        query = {'bool':{'should':[]}}
        query['bool']['should'].append(m1)
        query['bool']['should'].append(m2)
        return query
            
    
            
 



def andOperator(m1,m2):
    global words

    if type(m1) != dict:
        words.append(m1)
        resultList = areaSelect(m1)
        m1Result = {'bool':{'should':[]}}
        for i in resultList:
            m1Result['bool']['should'].append(i)
    if type(m2) != dict:
        words.append(m2)
        resultList = areaSelect(m2)
        m2Result = {'bool':{'should':[]}}
        for i in resultList:
            m2Result['bool']['should'].append(i)
        
    query = {'bool':{'must':[]}}
    if type(m1) != dict:
        query['bool']['must'].append(m1Result)
#         query['bool']['must'].append(m11)
#         query['bool']['must'].append(m12)
#         query['bool']['must'].append(m13)
    else:
        query['bool']['must'].append(m1)
    if type(m2) != dict:
        query['bool']['must'].append(m2Result)
#         query['bool']['must'].append(m21)
#         query['bool']['must'].append(m22)
#         query['bool']['must'].append(m23)
    else:
        query['bool']['must'].append(m2)
    return query
def notOperator(m1,m2):
    global words
    if type(m1) != dict:
        words.append(m1)
        resultList = areaSelect(m1)
        m1Result = {'bool':{'should':[]}}
        for i in resultList:
            m1Result['bool']['should'].append(i)
    if type(m2) != dict:
        resultList = areaSelect(m2)
        m2Result = {'bool':{'must':[]}}
        for i in resultList:
            m2Result['bool']['must'].append(i)

        
    query = {'bool':{'must':[],'must_not':[]}}
    #query['bool']['must'].append(m1)
    if type(m1) != dict:
        query['bool']['must'].append(m1Result)

    else:
        query['bool']['must'].append(m1)
    if type(m2) != dict:

        query['bool']['must_not'].append(m2Result)

    else:
        query['bool']['must_not'].append(m2)
    return query

def slopOperator(a,c):
    global words
    if type(a) != dict:
        #print 'slop a = ',a
        for i in a.split():
            words.append(i)
        resultList = slopAreaSelect(a, int(c))
        m1Result = {'bool':{'should':[]}}
        for i in resultList:
            m1Result['bool']['should'].append(i)
        query = m1Result
        
    else:
        print 'slop input Error'
    return query
    
#=================construction area===============================
def boolCalculation(a,b,c):
    if b =='and':
        #t = a+'and'+c
        t = andOperator(a,c)
        return t
    elif b =='or':
        #t = a+'or'+c
        t = orOperator(a,c)
        return t
    elif b == 'not':
        t = notOperator(a,c)
    elif b == '~' :
        if c.isdigit():
            t = slopOperator(a,c)
        else:
            print 'slop distance error'
            t =''
    return t
    
    

def calculation(eList,left,right):
    tem = []
    
    for i in range(left,right):
        curr = eList.pop(left)
        if curr =='(' or curr ==')':
            continue
        tem.append(curr)
    eList.insert(left,tem)

    return eList

def blockRemove(aList,count):
    indexList = []
    block = []
    while count> 0:
        for i in range(len(aList)):
            if aList[i] == '(':
                indexList.append(i)
            if aList[i] == ')':
                left = indexList.pop()
                right = i+1
                block.append((left,right))
                break
        (left,right) = block.pop(0)
        aList = calculation(aList, left, right)
        count -= 1
    return aList

def dfs(aList):
    i = 0
    #print result
    #print aList
    if type(aList[0]) == list:
        dfs(aList[0])
    else:
        result.append(aList[0])
    while i < len(aList):
        #print 'result = ',result
        if i+2 >= len(aList):
            i = i+2
            #print 'happen'
            continue
        a =''
        tem = result.pop()
        if type(tem) == list:
            dfs(tem)
            a = result.pop()
        else:
            a = tem
            
        if type(aList[i+1]) == list:
            dfs(aList[i+1])
            b = result.pop()
        else:
            b = aList[i+1]
        if type(aList[i+2]) == list:
            dfs(aList[i+2])
            c = result.pop()
        else:
            c = aList[i+2]
        i = i+ 2
#         print 'a = ',a
#         print 'oper = ', b
#         print 'c = ',c
        #print a,b,c 
        result.append(boolCalculation(a,b,c))
#         print 'step = ',boolCalculation(a,b,c)
#         print 'result = ',result 
        
def operatorList(oper):
    if oper == '(' or oper ==')' or oper == 'and' or oper == 'or' or oper =='not' :
        return False
    return True


def inputFormule(inputStr):
    #aList = []
    aList = []
    tem = ''
    innerCheck = True
    for i in inputStr:
        if i =="'":
            innerCheck = not innerCheck
        #print i 
        #print innerCheck
        if i.isspace() and innerCheck:
            continue
        if i == '(' or i == ')':
            if not tem.strip() == '':
                aList.append(tem)
                tem = ''
            aList.append(i)
        elif i =="'":
            
            if not tem.strip() == '':
                aList.append(tem)
            tem = ''
        else:
            tem += i
    #print 'al = ',aList
    return inputAna(aList)


def inputAna(aList):
    count = 0
    for i in range(len(aList)):
        aList[i] = aList[i].strip()
#        get all words and exact pubid list from system 
        if operatorList(aList[i]):
            aList[i] = aList[i]
            #aList[i] = readDataFromSystem(aList[i])
    for i in aList:
        if i =='(':
            count += 1
    #print aList  
    return (aList,count)  

def display(i):
    print 'display =====>'
    print '  ',i
    if type(i) == list:
        for j in i:
            display(j)
    else:
        return 0


def manageFunction(inputStr,userid,searchArea=None,wordsArea=None):
    global areaList, wordsLocation
    if searchArea != None:
        areaList = searchArea
    if wordsArea != None:
        for word in wordsArea:
            if len(word) < 1 or word.isspace():
                continue
            tem = word
            #word = word.replace('\n','')
            if '~' in word:
                tem = word.split('~')[0]
            wordsLocation[tem] = wordsArea[word] 

        
        #for i in wordsLocation:
        #    print i,wordsLocation[i]
    errorValue = 0
    inputStr = inputStr
    aList = []
    (aList,count) = inputFormule(inputStr)
    #print 'alist = ',aList
    #print count
    
    bList = blockRemove(aList,count)


    dfs(bList)
    
    
    v = result.pop()
    
    
    if type(v) != dict:
        #print 'v = ',v
        if '*' in v:
            shouldList = areaSelect(v)
            v = {'query':{'bool':{'should':shouldList}}}
        else:
            #v = {'query':{'bool':{'should':[ {'match_phrase':{'Foreword':v}} , {'match_phrase':{'Scope':v}} , {'match_phrase':{'References':v}},{'match_phrase':{'Definition':v}},{'match_phrase':{'content':v}}]}}}
            shouldList = areaSelect(v)
            v = {'query':{'bool':{'should':shouldList}}}
    if errorValue == 0 :
  
        errorMap = {"errorCode": str(errorValue), "errorDesc": v}
    else:    
        errorMap = {"errorCode": str(errorValue), "errorDesc": errorType(errorValue)}
    areaList = ['title','asbt','claimsList']
    wordsLocation = {}
    return errorMap,words


def esSearch(query):
    global es,words
    patentList = []

    body = {'_source':['title','abst','claimsList'],'query':query}    
    res = es.search('patentdata', 'cn_patent', body,size=3, request_timeout=500)
    for data in res['hits']['hits']:
        if not data['_source'].has_key('title') or not data['_source'].has_key('abst') or not data['_source'].has_key('claimsList'):
            continue
        tem = ''
        tem = tem + data['_source']['title'] + '\n'
        tem = tem + data['_source']['abst'] + '\n'
        for i in data['_source']['claimsList']:
            tem = tem + i + '\n'
        tem = tem.encode('utf-8')
        patentList.append(tem)
    for i in range(len(patentList)):
        for word in words:
            change = "<em class='blue'>"+word + "</em>"
            if type(patentList[i]) ==list:
                for j in range(len(patentList[i])):
                    patentList[i][j] = patentList[i][j].replace(word,change)
            else: 
                patentList[i] = patentList[i].replace(word,change)
    words = []
    return patentList
    

def esSearchBasic(query):
    global es,words
    body = {'_source':['_id','type','Version'],'query':query}
    #==================3gpp and ts ================================================    
    res = es.search('3gpp', 'ts', body,size=1000, request_timeout=500)
    print 'res = ',res
    basicList = []
    standardType = '3GPP'
    docType = 'TS'
    standardDict={}
    for data in res['hits']['hits']:
        if not data['_source'].has_key('type'):
            continue
        #print 'Found'
        if not data['_source'].has_key('Version'):
            data['_source']['Version'] = data['_id'].replace(data['_source']['type'],'')
        standardFile = {}
        standardFile['standardType'] = standardType
        standardFile['docType'] = docType
        standardFile['_id'] = data['_id']
        standardFile['_type'] = data['_source']['type']
        standardFile['Version'] = data['_source']['Version']
        
        if standardDict.has_key(data['_source']['type']):
            vD = standardDict[data['_source']['type']]['Version']
            vT = data['_source']['Version']
            if vD > vT:
                continue
            else:
                standardDict[data['_source']['type']]['Version'] = vT
            
                standardDict[data['_source']['type']]['content']= standardFile
        else:
            standardDict[data['_source']['type']] = {'Version':data['_source']['Version'],'content':standardFile}
            
        #basicList.append(standardFile)
    for i in standardDict:
        basicList.append(standardDict[i]['content'])
    return basicList
        


def standardExact(word,userid):
    global words
    words = []
    print word
    error,aList = manageFunction(word, userid)
    print error
    if error['errorCode'] == '0':
        query = error['errorDesc']
    else:
        return error
    print words
    (conn,db,col) = tbMong('userwords')
    col.remove({'userid':userid})
    col.insert({'userid':userid,'words':words})
    
    error = {'errorCode':'0','errorDesc':esSearchBasic(query)}
    return json.dumps(error)
'''
europeCountryCodeMap.put("AL","阿尔巴尼亚");
        europeCountryCodeMap.put("AD","安道尔共和国");
        europeCountryCodeMap.put("AT","奥地利");
        europeCountryCodeMap.put("BY","白俄罗斯");
        europeCountryCodeMap.put("BE","比利时");
        europeCountryCodeMap.put("BG","保加利亚");
        europeCountryCodeMap.put("CZ","捷克");
        europeCountryCodeMap.put("DK","丹麦");
        europeCountryCodeMap.put("EE","爱沙尼亚");
        europeCountryCodeMap.put("FI","芬兰");
        europeCountryCodeMap.put("FR","法国");
        europeCountryCodeMap.put("DE","德国");
        europeCountryCodeMap.put("GR","希腊");
        europeCountryCodeMap.put("HU","匈牙利");
        europeCountryCodeMap.put("IS","冰岛");
        europeCountryCodeMap.put("IE","爱尔兰");
        europeCountryCodeMap.put("IT","意大利");
        europeCountryCodeMap.put("LV","拉脱维亚");
        europeCountryCodeMap.put("LI","列支敦士登");
        europeCountryCodeMap.put("LT","立陶宛");
        europeCountryCodeMap.put("LU","卢森堡");
        europeCountryCodeMap.put("MT","马耳他");
        europeCountryCodeMap.put("MD","摩尔多瓦");
        europeCountryCodeMap.put("MC","摩纳哥");
        europeCountryCodeMap.put("NL","荷兰");
        europeCountryCodeMap.put("NO","挪威");
        europeCountryCodeMap.put("PL","波兰");
        europeCountryCodeMap.put("PT","葡萄牙");
        europeCountryCodeMap.put("RO","罗马尼亚");
        europeCountryCodeMap.put("RU","俄罗斯");
        europeCountryCodeMap.put("SM","圣马力诺");
        europeCountryCodeMap.put("SK","斯洛伐克");
        europeCountryCodeMap.put("ES","西班牙");
        europeCountryCodeMap.put("SE","瑞典");
        europeCountryCodeMap.put("CH","瑞士");
        europeCountryCodeMap.put("UA","乌克兰");
        europeCountryCodeMap.put("GB","英国");
        
        europeCountryCodeMap.put("EP", "欧洲专利局");
        europeCountryCodeMap.put("XN", "北欧专利研究所");
        europeCountryCodeMap.put("QZ", "欧洲共同体之植物多样性部署");
        europeCountryCodeMap.put("EA", "欧亚专利组织");
        //自定义
        europeCountryCodeMap.put("OUZHOU", "欧洲");
        
        //波黑[BA]、克罗地亚[HR]、联邦德国[DD]、前苏联[SU]、塞尔维亚[RS]、黑山[ME]
        europeCountryCodeMap.put("BA","波黑");
        europeCountryCodeMap.put("HR","克罗地亚");
        europeCountryCodeMap.put("DD","联邦德国");
        europeCountryCodeMap.put("SU","前苏联");
        europeCountryCodeMap.put("RS","塞尔维亚");
        europeCountryCodeMap.put("ME","黑山");
'''




def jundgeCountry(appid):
    head = appid[:2]
    europeCountryCodes = 'AL AD AT BY BE BG CZ DK EE FI FR DE GR HU IS IE IT LV LI LT LU MT MD MC NL NO PL PT RO RU SM SK ES SE CH UA GB EP XN QZ EA BA HR DD SU RS ME'
    europeMap = {}
    for code in europeCountryCodes.split():
        europeMap[code] = 1
    if europeMap.has_key(head):
        return 'ep_patent'
    if head == 'CN' or head =='US' or head =='TW' or head =='KR' or head =='JP' or head =='WO' or head =='EP':
        return head.lower()+'_patent'
    return 'other_patent'
import json   

def getClaimsList(appid):
    global es
    doc_type = jundgeCountry(appid)
    appid = appid.replace(' ','').replace('/','')
    subIndex = appid.find('.')
    if subIndex != -1:
        appid = appid[:subIndex]
    pubid = appid+'*'
    pubid = pubid.lower()
    print doc_type,pubid
    body = {'_source':['claimsList','pubid','appid','description'],'query':{'wildcard':{'appid':pubid}}}
    print 'body = ',body
    res = es.search('patentdata', doc_type, body, size=10,request_timeout=500)
    R = []
    print res
    for data in res['hits']['hits']:
        if data['_source'].has_key('claimsList'):
            R.append(data['_source'])
    #R = json.dumps(R)
    return json.dumps({'errorCode':'0','errorDesc':R})


def contentGet(id,userid):
    global es
    words = []
    (conn,db,col) = tbMong('userwords')
    for data in col.find({'userid':userid}):
        words = data['words']
    res = es.get('3gpp', id, 'ts')
#     for i in res:
#         if i=='_source':
#             continue
#         print i,' = ',res[i]
    for i in res['_source']:
        for word in words:
            change = "<em class='blue'>"+word + "</em>"
            if type(res['_source'][i]) == list:
                for j in range(len(res['_source'][i])):
                    res['_source'][i][j] = res['_source'][i][j].replace(word,change)
            else:
                res['_source'][i] = res['_source'][i].replace(word,change)
    return json.dumps({'errorCode':'0','errorDesc':res['_source']})




def main():

    server = ThreadXMLRPCServer(('103.31.53.156',30007))
    server.register_multicall_functions()
    server.register_function(standardExact,'standardExact')
    server.register_function(contentGet,'contentGet')
    server.register_function(getClaimsList,'getClaimsList')
    print "Listening on port 30007..."
       
    server.serve_forever()
if __name__ =='__main__':
    main()


        
        
