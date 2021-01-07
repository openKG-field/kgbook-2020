#coding=utf-8
'''
Created on 2018��9��11��

@author: zhaoh
'''

from pymongo import MongoClient
def wordMongo(tb):
    #host = '192.168.1.10'
    host = '119.18.207.122'  
    dbName = 'mqpat'
    user = 'mqpat-rw'
    passwd = '123456'
    port = 27017
    myTbNme = tb
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[myTbNme]
    return (conn,db,collection) 

def rankValue(vMap,score,reJg):
    am = len(vMap)
    result = {}
    count = 0
    max = 0 
    for k,v in sorted(vMap.iteritems(),key=lambda k:k[1],reverse=reJg):
        if v > max:
            max = v 
    for k,v in sorted(vMap.iteritems(),key=lambda k:k[1],reverse=reJg):
        if max == 0:
            result[k] = 0
        else:
            result[k] = float(v)/float(max)*float(score) + 50
    
        
    
    return result
import re 
import time


import xlwt        
def function_with_excel(data,name):
    workbook=xlwt.Workbook(encoding='utf-8')  
    booksheet=workbook.add_sheet('default', cell_overwrite_ok=True)   
    for i,row in enumerate(data):  
        for j,col in enumerate(row):  
            booksheet.write(i,j,col)
    workbook.save('%s.xls'%name)

def spendTime(start_time,end_time):

    seconds, minutes, hours = int(end_time - start_time), 0, 0
    hours = seconds // 3600
    minutes = (seconds - hours*3600) // 60
    seconds = seconds - hours*3600 - minutes*60
    print("\n  Complete time cost {:>02d}:{:>02d}:{:>02d}".format(hours, minutes, seconds))
    
    
def similar(fieldsName,pubid):
    (conn,db,col) = wordMongo('fieldsIndivideBase')
    
    aimGoods = []
    aimWords = ''
    
    goodGoal = 2
    wordGoal = 3
    S = time.time()

    for data in col.find({'fieldsName':fieldsName,'pubid':pubid},{'goodsList':1,'tfidf_v1':1}).batch_size(100):
        if 'goodsList' in data:
            aimGoods = data['goodsList']
        if 'tfidf_v1' in data:
            aimWords = data['tfidf_v1']
    
    pubids = {}
    pubidTitle = {}
    
    print 'get aim Goods and Words'
    
    
    for data in col.find({'fieldsName':fieldsName,'$or':[{'noisyType':'D'},{'noisyType':'O'},{'noisyType':'A'}]},{'pubid':1,'title':1}).batch_size(1000):    
        if 'pubid' in data :
            pubids[data['pubid']] = 0 
        if 'title' in data and 'pubid' in data:
            pubidTitle[data['pubid']] = data['title']
    
    goodS = time.time()      
    if aimGoods != []:
        goodBalance = len(aimGoods)
        for good in aimGoods:
            for data in col.find({'fieldsName':fieldsName,'goodsList':good,'$or':[{'noisyType':'D'},{'noisyType':'O'},{'noisyType':'A'}]},{'pubid':1}).batch_size(100):    
                #print 'get Good'
                if 'pubid' in data:
                    if data['pubid'] in pubids:
                        pubids[data['pubid']] = pubids[data['pubid']] + float(1)/float(goodBalance)*goodGoal
    goodE = time.time()
    
    print 'aimGoods done'
    spendTime(goodS, goodE)
    
    wordS = time.time()
    if aimWords != '':
        words = re.split(r'[\s|,|$]+', aimWords)
        words = ' '.join(words)
        words = words.split()
        wordBalance = len(words)
        for word in words:
            for data in col.find({'fieldsName':fieldsName,'tfidf_v1':{'$regex':word},'$or':[{'noisyType':'D'},{'noisyType':'O'},{'noisyType':'A'}],},{'pubid':1}).batch_size(100): 
                if 'pubid' in data:
                    if data['pubid'] in pubids:
                        pubids[data['pubid']] = pubids[data['pubid']] + float(1)/float(wordBalance)*wordGoal
    wordE = time.time()
    
    print 'aimWords done' 
    o = open(pubid+'out.txt','w')
    spendTime(wordS, wordE)
    for k,v in sorted(pubids.iteritems(),key=lambda k:k[1],reverse=True):
        if v == 0:
            break
        if k in pubidTitle:
            o.write((k+' ' + pubidTitle[k] + ' '+ str(v)).encode('utf-8')+'\n') 

        
            
            
    end=time.time()
    spendTime(S, end)
            
            
            
def fourAreaSimilar(fieldsName,language,aim):
    (conn,db,col) = wordMongo('fieldsIndivideBase')
    '''
    techWords':1,'fieldWords':1,'problemWords':1,'funcWords'
    '''
    aimTech = set()
    aimField = set()
    aimProblem = set()
    aimFunc = set()
    pubidTech = {}
    pubidField = {}
    pubidProblem = {}
    pubidFunc = {}
    pubidTitle = {}
    pubidApp = {}
    for data in col.find({'fieldsName':fieldsName,'type':language,'$or':[{'noisyType':'D'},{'noisyType':'O'},{'noisyType':'A'}]},{'pubid':1,'_id':0,'title':1,'applicantList':1,'techWords':1,'fieldWords':1,'problemWords':1,'funcWords':1}).batch_size(100):        
        pubid = data['pubid']
        if 'title' in data:
            pubidTitle[pubid] = data['title']
        if 'applicantList' in data:
            pubidApp[pubid] = data['applicantList']
        if pubid == aim:
            if 'techWords' in data:
                tem = data['techWords'].split(',')
                if len(tem) > 1 :
                    tem.pop(len(tem)-1)
                    aimTech = set(tem)
            
            if 'fieldWords' in data:
                tem = data['fieldWords'].split(',')
                if len(tem) > 1 :
                    tem.pop(len(tem)-1)
                    aimField = set(tem)
            
            if 'problemWords' in data:
                tem =data['problemWords'].split(',')
                if len(tem) > 1 :
                    tem.pop(len(tem)-1)
                    aimProblem = set(tem)
            
            if 'funcWords' in data:
                tem =data['funcWords'].split(',')
                if len(tem) > 1 :
                    tem.pop(len(tem)-1)
                    aimFunc = set(tem)
        else:
            if 'techWords' in data:
                tem = data['techWords'].split(',')
                if len(tem) > 1 :
                    tem.pop(len(tem)-1)
                    pubidTech[pubid] = set(tem)
            
            if 'fieldWords' in data:
                tem = data['fieldWords'].split(',')
                if len(tem) > 1 :
                    tem.pop(len(tem)-1)
                    pubidField[pubid] = set(tem)
            
            if 'problemWords' in data:
                tem =data['problemWords'].split(',')
                if len(tem) > 1 :
                    tem.pop(len(tem)-1)
                    pubidProblem[pubid] = set(tem)
            
            if 'funcWords' in data:
                tem =data['funcWords'].split(',')
                if len(tem) > 1 :
                    tem.pop(len(tem)-1)
                    pubidFunc[pubid] = set(tem)   
    
    print 'tech'
    techScore = {}
    for i in pubidTech:
        techScore[i] = len(pubidTech[i]&aimTech)
        #print i,techScore[i]
    pCount = 0
    for k,v in sorted(techScore.iteritems(),key=lambda k:k[1],reverse=True):
        pCount += 1
        print k,v
        if pCount > 5:
            break

    techScore = rankValue(techScore, 50, True)
    #for i in techScore:
    #    print i ,techScore[i]

    fieldScore = {}
    for i in pubidField:
        fieldScore[i] = len(pubidField[i]&aimField)
        
    print 'field'
    pCount = 0
    for k,v in sorted(fieldScore.iteritems(),key=lambda k:k[1],reverse=True):
        pCount += 1
        print k,v
        if pCount > 5:
            break
    fieldScore = rankValue(fieldScore, 50, True)
    
    
        
    problemScore = {}
    for i in pubidProblem:
        problemScore[i] = len(pubidProblem[i]&aimProblem)
    
    print 'problem' 
    pCount = 0
    for k,v in sorted(problemScore.iteritems(),key=lambda k:k[1],reverse=True):
        pCount += 1
        print k,v
        if pCount > 5:
            break
        
    problemScore = rankValue(problemScore, 50, True)
    
    print 'func'
    funcScore = {}
    for i in pubidFunc:
        funcScore[i] = len(pubidFunc[i]&aimFunc)
    
    pCount = 0
    for k,v in sorted(funcScore.iteritems(),key=lambda k:k[1],reverse=True):
        pCount += 1
        print k,v
        if pCount > 5:
            break
    
    funcScore = rankValue(funcScore, 50, True)
    result = {}
    for data in col.find({'fieldsName':fieldsName,'type':language,'$or':[{'noisyType':'D'},{'noisyType':'O'},{'noisyType':'A'}]},{'pubid':1,'_id':0}).batch_size(100):        
        pubid = data['pubid']
        curCount = 0
        amount = 0
        
        if pubid in techScore:
            amount += techScore[pubid]
            curCount += 1
        
        if pubid in fieldScore:
            amount += fieldScore[pubid]
            curCount += 1
        
        if pubid in problemScore:
            amount += problemScore[pubid]
            curCount +=1
            
        if pubid in funcScore:
            amount += funcScore[pubid]
            curCount += 1
        if curCount < 2 :
            curCount = 2
        
        result[pubid] = float(float(amount)/float(curCount))

    o = open(aim+'.txt','w')
    excel = []
    excelHead = ['pubid','applicants','title','fieldWords','funcWords','problemWords','techWords','similar']
    excel.append(excelHead)
    for k,v in sorted(result.iteritems(),key=lambda k:k[1],reverse=True):
        excelData = []
        pubid = k
        excelData.append(k)
        if pubid in pubidApp:
            temApp = pubidApp[pubid]
            tem = ''
            for i in temApp:
                tem = tem + i['applicant'] + ' | '
            excelData.append(tem)
        else:
            excelData.append('')
        
        if pubid in pubidTitle:
            excelData.append(pubidTitle[pubid])
        else:
            excelData.append('')
        
        if pubid in pubidField:
            excelData.append('|'.join(list(pubidField[pubid]))) 
        else:
            excelData.append('')
            
        if pubid in pubidFunc:
            excelData.append('|'.join(list(pubidFunc[pubid])))
        else:
            excelData.append('')
            
        if pubid in pubidProblem:
            excelData.append('|'.join(list(pubidProblem[pubid])))
        else:
            excelData.append('')
        
        if pubid in pubidTech:
            excelData.append('|'.join(list(pubidTech[pubid])))
        else:
            excelData.append('')
        excelData.append(v)    
                   
        
        
        excel.append(excelData)
    function_with_excel(excel, aim)

import time
s = time.time()
fieldsName = '5g-polar'
language = 'cn'
pubid = 'CN107231158A' 
similar(fieldsName,pubid)
#fourAreaSimilar(fieldsName, language, aim)     
e = time.time()
print e - s


            
            
def startByCompany(app,fieldsName):
    (conn,db,col) = wordMongo('fieldsIndivideBase') 
    for data in col.find({'applicantList.applicant':app,'fieldsName':fieldsName},{'pubid':1}).batch_size(100):
        pubid =  data['pubid']
        print pubid
        #similar(fieldsName,pubid)
        
        
# fieldsName = '软体机器人-软抓手'
# pubid = ''
# similar(fieldsName, pubid)
# app = '北京软体机器人科技有限公司'
# orgS = time.time()
# startByCompany(app, fieldsName)
# orgE = time.time()
# 
# print 'total spend ',spendTime(orgS, orgE)
        





















