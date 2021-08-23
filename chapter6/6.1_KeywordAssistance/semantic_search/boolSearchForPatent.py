# -*- encoding: utf-8 -*-
"""
@File    : boolSearchForPatent.py
@Time    : 2021/1/25 11:29
@Author  : Zhaohy
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""
from errorFunction import  errorType

from cartesian import Cartesian


words = []

step = 0
result = []

areaList = ['title','abst','claimsList']
wordsLocation = {}

def synonymWords(m):
    wordList = [m]

    return wordList




def areaSelect(m):

    global words,areaList,wordsLocation
    #areaList = ['title','abst','claimsList','description']
    
    resultList = []

    if wordsLocation == {}:
        temList = areaList
    else:
        if m.decode('utf-8') in wordsLocation:
            #print 'found'
            temList = wordsLocation[m.decode('utf-8')]
        elif m in wordsLocation :
            temList = wordsLocation[m]
        else:
            print (m,[m],'not exists')
            temList = areaList

    if '*' in m :
        
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

    words = [m]

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
            print (m,[m],'not exists')
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

    else:
        query['bool']['must'].append(m1)
    if type(m2) != dict:
        query['bool']['must'].append(m2Result)

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
    print(type(a))
    if type(a) is not  dict:
        #print 'slop a = ',a
        for i in a.split():
            words.append(i)
        resultList = slopAreaSelect(a, int(c))
        m1Result = {'bool':{'should':[]}}
        for i in resultList:
            m1Result['bool']['should'].append(i)
        query = m1Result
        
    else:
        print ('slop input Error')
        query = {}
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
            print(a,b,c)
            t = slopOperator(a,c)
        else:

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

    if type(i) == list:
        for j in i:
            display(j)
    else:
        return 0


def manageFunction(inputStr,searchArea=None,wordsArea=None):
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


    errorValue = 0

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
            shouldList = areaSelect(v)
            v = {'query':{'bool':{'should':shouldList}}}
    if errorValue == 0 :
  
        errorMap = {"errorCode": str(errorValue), "errorDesc": v}
    else:    
        errorMap = {"errorCode": str(errorValue), "errorDesc": errorType(errorValue)}
    areaList = ['title','asbt','claimsList']
    wordsLocation = {}
    return errorMap,words,v


def main():
    #直接通过标准布尔检索式，生成es可接受的 query，注意每一个独立的检索要素应该用 ' ' 圈定并含有无意义的空格等其他符号
    #检索式支持 * 与 ~ 其中 *为填充符可以替代多个字符，~为词组之间的距离 且 词距表述需要用（）圈定
    input = "('移动支付' and '人工智能') or '区块链' or ('数据 测试'~'10')"
    m,w,v = manageFunction(input,searchArea=['title','asbt','claimsList'])
    print(v)


if __name__ == '__main__':
    main()