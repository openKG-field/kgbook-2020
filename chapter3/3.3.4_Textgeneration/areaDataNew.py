#coding=utf-8
'''
Created on 2018��10��26��

@author: zhaoh
'''

'''
领域词字段、技术词字段+权要词字段、问题词、功效词
'''
from jiebaCutPackage import jiebaInterface
from mongoC import mongC
import re
import json
def functionWords(wordDict,long,line):
    words = {}
    for i in range(len(line)-1):
        for j in range(2,long+1):
            tem = ''
            if i + 1 > len(line):
                break
            if i + j > len(line):
                tem = line[i:]
            else:
                tem = line[i:i+j]
                
            if tem == '':
                continue
            if tem in wordDict:
                words[tem] = 1
    return words

techPer = [['解决','弊端'],'本发明可','目的在于','优点是',['使','更'],'提高','降低','防止',['具有','作用'],'节省','可对',['使得','提高'],['使','增强'],'可使',\
            '使得','准确',['解决','问题'],'有效','提高',['提高','效率'],'是否正确','提升','避免','更好','生成','适应性','克服',['具有','特点'],\
           ['具备','特征'],['具有','特征'],['具有','能力'],['使','适应'],'方便',['使', '优化'],'灵活','缩短','降低','高效','完善','加强','便捷','不需要','简单','易于','体现',\
           '有效提取','有利于',['能','满足'],'成本低','成本较低',['提高','质量'],['减少','错误'],['满足','需求'],['避免','问题'],['降低','成本'],['达到','目的'], \
           ['使', '减小'],['使','减少'],['使','增加'],['使','增强'],['扩展','特征'],['防止','问题'],['改善','体验'],'改善',['建立','模式'],'开创','可靠性','准确性','适用性',\
           ['达到','效果'],'适用于','便利性','精准度','稀疏化','利用性','确保','更加','减少',['弥补','不足'],['具有','优点'],['打破','局限性'],['达到','目的'],'可玩性','容错性',\
           '可维护性','增强','降低','优点','鲁棒性',['使','加速'],'替代','代替','便于','能够','实时',['反映','效果'],'自动生成','给出',['能','自动'],'无损','新鲜度','取代','节省','利于',\
           '实用性','更多',['可','解决'],'保证','很好','便于','剔除','有利','稳定性','精度高','合理性','有效','减轻','最优',['不受','影响'],'只需','可映射','真实的','识别率',\
           '个性化','智能化','简化','改进','缩短',['实现','优化'],['满足','目标'],['能', '得到'],['能','解决'],['能','提供'],['加速','过程'],['能','及时'],['可','及时']\
           ,['可','得到'],['对','优化'],['进行','优化'],['实现','功能'],['能','适应'],['使','修复'],['可','修复'],['能','修复'],['能','快速'],['有益','效果'],['可','自动'] \
           , ['可', '用于'],['保证', '正常'],['满足', '需求'],'解决了','可以执行','可执行','实现了','性好','适于','优点','有潜力',['具有','价值'],['不受','限制'],'节省',\
           ['使之','具有'],'结论',['达','目的']]

def extractPerformance(sentence):
    global techPer
    sentence = sentence.encode('utf-8')
    for rull in techPer:
        if type(rull) == list:
            #print 'list rull match'
            current = -1
            listbool = True
            for i in rull:
                if i in sentence:
                    if current < sentence.index(i):
                        current = sentence.index(i)
                    else:
                        listbool = False
                        break
                else:
                    listbool = False
                    break
            if listbool:
                #print ' matching rull is', rull[0],rull[1]
                sub = sentence[ sentence.index(rull[0]) :]
                return sub
        else:
            #print 'word rull match'
            if rull in sentence:
                sub = sentence[ sentence.index(rull) : ]
                return sub
    return ''


def loadFunction(path):
    wordDict = {}
    f = open(path,'r')
    long = 0
    for line in f :
        if len(line) < 1 or line.isspace() :
            continue
        word = line.replace('\n','').replace('\r','')
        word = word.decode('utf-8')
        cur = len(word)
        if cur > long :
            long = cur
            
        wordDict[word] = 1
    return wordDict,long

(conn,db,col) = mongC.mqpatMongo('fieldsIndivideBase')


techProblem = ['针对', '的问题',['属于','问题'],['涉及','问题'],'缺陷是','损失大','效果有限','目的在于','技术问题在于',['针对','方法'],\
              ['针对','措施'],['针对','缺点'],['针对','途径'],'目的是','目的之一','任务是',['存在','问题'],'旨在',['目前','最'],['在于','难以'],['已有','状况'],'一般都',\
               '只具备','极不','不及',['存在','缺点'],['但','太'],['现','大多'],['由于','不'],['为','克服'],'现有的','尚无',['迄今','没'],'解决','均指','很需要',\
               ['现在','但'],['目前','只']]


techMethod = [['涉及','方法'],['涉及','装置'],['涉及','系统'],['对','工艺'],['涉及','领域'],'涉及',['为解决','问题'],['属于','问题'], '公开','采用',\
            ['属于','领域'],['基于','方法'],['基于','装置'],['提出','系统'],['提出','方法'],['建立','系统'],['建立','方法'],'本说明',\
            ['提供','方法'],['一种','方法'],['一种','装置'], ['一种','方案'],['一种','系统'],'本发明','申请''公布','领域','属于','平台','揭示','发明','该技术','本实用新型' \
            ,['由', '组成'],['采用', '方案']]


techField = [['发明','涉及'],'本发明属于',['属','领域'],'发明公开了','一种',['一种','方法'],'总体涉及','是一种',['涉及', '领域'],'公开了',['涉及', '一种'],['用于', '领域'],\
             ['涉及', '领域'],['用于', '方法'],['用于', '装置'],'目的在于', '还涉及',['研究','一种'],'提供','本发明提出',['发明','任务'],['发明','系'],['发明','是'], \
             ['发明', '属'],['发明', '方法'],['发明', '目的']]

claimAfter = ['特征在于']

def extractSentByRull(sentence,tech,functionType=0):
    sentence = sentence
    if functionType == 0:
        for rull in tech:
            if type(rull) == list:
                #print 'list rull match'
                current = -1
                listbool = True
                for i in rull:
                    if i in sentence:
                        if current < sentence.index(i):
                            current = sentence.index(i)
                        else:
                            listbool = False
                            break
                    else:
                        listbool = False
                        break
                if listbool:
                    #print ' matching rull is', rull[0],rull[1]
                    sub = sentence[ sentence.index(rull[0]) :]
                    return sub
            else:
                #print 'word rull match'
                if rull in sentence:
                    sub = sentence[ sentence.index(rull) : ]
                    return sub
        return ''
    else:
        for rull in tech:
            if type(rull) == list:
                #print 'list rull match'
                current = -1
                listbool = True
                for i in rull:
                    if i in sentence:
                        if current < sentence.index(i):
                            current = sentence.index(i)
                        else:
                            listbool = False
                            break
                    else:
                        listbool = False
                        break
                if listbool:
                    #print ' matching rull is', rull[0],rull[1]
                    return sentence
            else:
                #print 'word rull match'
                if rull in sentence:
                    return sentence
        return ''
    

error = open('error.txt','w')
from elasticsearch import Elasticsearch
es = Elasticsearch(['10.0.2.2:9200'])

wordDict,long = loadFunction('Functionwords.txt')
claimsDict, claimsLong = loadFunction('Dict20181026.txt')
def areaValue(data):
    count = 0
    global error,wordDict,long,claimsDict,claimsLong
    #(lconn,ldb,lcol) = mongC.testMongo(country)
    fieldSent = ''
    techSent = ''
    problemSent = ''
    claimSent = ''
    func = ''
    #pubid = data['pubid']
    if 'abst' in data:
        func = func + data['abst']
    if 'claimsList' in data:
        for i in data['claimsList']:
            func = func + i
    func = re.split("；|。||\t", func)
    funcAb = ''
    for i in func:
        funcAb = funcAb + extractPerformance(i).decode('utf-8')

    funcWords = functionWords(wordDict, long, funcAb)
    funcTem = ''
    for i in funcWords:
        funcTem = funcTem + i + ','

        if 'title' in data:
            fieldSent = fieldSent + data['title']
        if 'techArea' in data:
            fieldSent = fieldSent + data['techArea']
        techSent = techSent + data['techArea']
        if 'abst' in data:
            techSent = techSent + data['abst']
        problemSent = problemSent + data['abst']
        if 'claimsIndList' in data:
            techSent = techSent + '。'.join(data['claimsIndList'])
        problemSent = problemSent + '。'.join(data['claimsIndList'])
        if 'claimsList' in data:
            for i in data['claimsList']:
                claimSent = claimSent + i

        fieldSent = fieldSent

        techSent = re.split("；|。||\t", techSent)
        techSentAb = ''
        for i in techSent:
            techSentAb = techSentAb + extractSentByRull(i.encode('utf-8'), techMethod, 0)

        problemSent = re.split("；|。||\t", problemSent)
        problemSentAb = ''
        for i in problemSent:
            problemSentAb = problemSentAb + extractSentByRull(i.encode('utf-8'), techProblem, 0)

        claimSent = re.split("；|。||\t", claimSent)
        claimSentAb = ''
        for i in claimSent:
            claimSentAb = claimSentAb + extractSentByRull(i.encode('utf-8'), claimAfter, 0)

        for i in claimSent:
            claimsWords = functionWords(claimsDict, claimsLong, i)
        for i in claimsWords:
            claimSentAb = claimSentAb + i + ','

    fieldWords = jiebaInterface.jiebaCut(fieldSent)
    fieldWords = re.sub(r'[_0-9]', '', fieldWords)

    techWords = jiebaInterface.jiebaCut(techSentAb)
    techWords = re.sub(r'[_0-9]', '', techWords)

    problemWords = jiebaInterface.jiebaCut(problemSentAb)
    problemWords = re.sub(r'[_0-9]', '', problemWords)

    claimWords = jiebaInterface.jiebaCut(claimSentAb)
    claimWords = re.sub(r'[_0-9]', '', claimWords)

    return funcTem, fieldWords, techWords + claimWords, problemWords
	

def getData(fieldsName,language):
    count = 0

    path = 'Functionwords.txt'
    wordDict,long = loadFunction(path)

    path = 'Dict20181026.txt'
    claimsDict, claimsLong = loadFunction(path)

    for data in col.find({'fieldsName':fieldsName,'type':language},{'pubid':1,'title':1,'abst':1,'claimsList':1,'claimsIndList':1,'techArea':1}).batch_size(100):
        fieldSent = ''
        techSent = ''
        problemSent = ''
        claimSent = ''
        func = ''
        pubid = data['pubid']
        funcWords,fieldWords,techWords,problemWords = areaValue(data)
        count += 1
        if count % 300 is 0 :
            print count ,' Done '

import codecs
def updateData(country):
    count = 0
    global error
    (lconn, ldb, lcol) = mongC.testMongo(country)
    path = 'Functionwords.txt'
    wordDict, long = loadFunction(path)

    path = 'Dict20181026.txt'
    claimsDict, claimsLong = loadFunction(path)

    for data in lcol.find({}, {'pubid': 1, 'title': 1, 'abst': 1, 'claimsList': 1, 'claimsIndList': 1,
                               'techArea': 1}).batch_size(100).limit(100):
        count += 1
        # if count < 5514000 :
        #    continue
        fieldSent = ''
        techSent = ''
        problemSent = ''
        claimSent = ''
        func = ''
        pubid = data['pubid']

        if count % 1000 is 0:
            print count, pubid, ' Done'
        if count < 12649000:
            continue

        if 'abst' in data:
            func = func + data['abst']
        if 'claimsList' in data:
            for i in data['claimsList']:
                func = func + i
        func = re.split("；|。||\t", func)
        funcAb = ''
        for i in func:
            funcAb = funcAb + extractPerformance(i).decode('utf-8')

        funcWords = functionWords(wordDict, long, funcAb)
        funcTem = ''
        for i in funcWords:
            funcTem = funcTem + i + ','

        if 'title' in data:
            fieldSent = fieldSent + data['title']
        if 'techArea' in data:
            fieldSent = fieldSent + data['techArea']
            techSent = techSent + data['techArea']
        if 'abst' in data:
            techSent = techSent + data['abst']
            problemSent = problemSent + data['abst']
        if 'claimsIndList' in data:
            techSent = techSent + '。'.join(data['claimsIndList'])
            problemSent = problemSent + '。'.join(data['claimsIndList'])
        if 'claimsList' in data:
            for i in data['claimsList']:
                claimSent = claimSent + i

        fieldSent = fieldSent

        techSent = re.split("；|。||\t", techSent)
        techSentAb = ''
        for i in techSent:
            techSentAb = techSentAb + extractSentByRull(i.encode('utf-8'), techMethod, 0)

        problemSent = re.split("；|。||\t", problemSent)
        problemSentAb = ''
        for i in problemSent:
            problemSentAb = problemSentAb + extractSentByRull(i.encode('utf-8'), techProblem, 0)

        claimSent = re.split("；|。||\t", claimSent)
        claimSentAb = ''
        for i in claimSent:
            claimSentAb = claimSentAb + extractSentByRull(i.encode('utf-8'), claimAfter, 0)

        for i in claimSent:
            claimsWords = functionWords(claimsDict, claimsLong, i)
            for i in claimsWords:
                claimSentAb = claimSentAb + i + ','

        # claimSent = extractSentByRull(claimSent.encode('utf-8'), claimAfter, 0).replace('特征在于','')
        #         print 'fieldSent = ',fieldSent
        #         print 'techSent = ',techSent
        #         print 'problemSent = ',problemSent
        #         print 'claimSent = ',claimSent
        fieldWords = jiebaInterface.jiebaCut(fieldSent)
        fieldWords = re.sub(r'[_0-9]', '', fieldWords)

        techWords = jiebaInterface.jiebaCut(techSentAb)
        techWords = re.sub(r'[_0-9]', '', techWords)

        problemWords = jiebaInterface.jiebaCut(problemSentAb)
        problemWords = re.sub(r'[_0-9]', '', problemWords)

        claimWords = jiebaInterface.jiebaCut(claimSentAb)
        claimWords = re.sub(r'[_0-9]', '', claimWords)

        # print 'fieldWords = ',fieldWords
        # print 'techWords = ',techWords
        # print 'problemWords = ',problemWords
        # print 'claimWords = ',claimWords
        with codecs.open('fieldSentences.txt','w',encoding='utf-8') as f:
            print (fieldSent)
            f.write(fieldSent+'\n')


        return fieldSent,problemSent,techSent,claimSent,func


'''
TODO 
use the combination sentence of fieldSent,problemSent,techSent,claimSent,func as a patent content
then use textGeneration to give patent abstract.

'''
country = 'cn_patent'
updateData(country)

    
    
    
    
    
    
    
    
