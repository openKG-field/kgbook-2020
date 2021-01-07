#encoding=utf-8
'''
author: Hongyu Zhao

Data : 09/25/2017 
'''

#flag keyword by jieba function and exact keywords by flag and combination 

import os
import sys
import time
reload(sys)
sys.setdefaultencoding( "utf-8" )
from pymongo import MongoClient 

    
sys.path.append("../")

import jieba.posseg
jieba.load_userdict("wordMerge.txt")

limitedWord =2
mainIPC = 'G06F'
limitedWord = 3
dbName = 'test'
tbName = 'zhyPatDataBean'
user = 'lyj-rw'
passwd = '123456'
host = '172.10.30.74'  
port = 27017

cwd=os.getcwd()
print(cwd)


def skipWord(word):
    if word =='方法' or word =='装置' or word =='步骤' or word =='模式' or word =='设备' or word =='内' or word =='到' or word =='使' or word =='使得' or word=='无法':
        return True
    return False


def checkRull(flag, word):
    if (flag[0] =='n' or flag == 'x' or flag == 'eng' or flag =='l' or flag =='b' or flag[0] =='v') and len(word)>=2:
        return True
    return False 

def headCheck(head):
    if head == "#*" or head == "#@" or head == "#!" or head =='#&' or head =='#^' or head =='#$' :
        return True
    return False
#filename = input("please input the filename with path ")
#resultName = input("please input the result name with path ")
# here is the input entire patent paper file
def createMongo():
    global dbName,tbName,user,passwd,host,port
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[tbName]
    return (conn,db,collection) 
def dividWord():
    # read the input data
    stopwordFile = open('stopword.txt','r')
    # Word dividing for the input data
    divideWordResult = open('divideWordResult.txt','w')
    fileFrequency = open('fileFrequency.txt','w')
    checkWordMap = {'start':0}
    fileCount = 0
    fileFrequencyMap = {'start':0}
    stopwordMap = {'start':0}
    for line in stopwordFile:
        wordContent = line.split()
        for t in wordContent:
            if stopwordMap.has_key(t.decode('utf-8')):
                continue
            else:
                stopwordMap[t.decode('utf-8')]=1
#     (conn,db,collection) = createMongo()   
#     select_where = {"$or":[{"title":{"$regex":"核磁共振"}},{"abst":{"$regex":"核磁共振"}},{"claims":{"$regex":"核磁共振"}}]}
#     for dataContent in collection.find(select_where):
#         file = list()
#         tem ='#@'
#         file.append('#^' + '  ' + dataContent['pubid'])
#         file.append('#*' + '  ' + dataContent['title'])
#         for i in dataContent['inventors']:
#             tem = tem + '  ' + i
#         file.append('#!' + '  ' + dataContent['abst'])
#         file.append('#&' + '  ' + dataContent['claims'])
    file = open('qinghuaTest.txt','r')
    for line in file:
    # read file line by line
        line = line.decode('utf-8')
        if len(line)>1 and headCheck(line[:2]):
            head = line[:2]
            if head == '#$':
                divideWordResult.write(line)
                continue
            if head == "#*":
                fileCount = fileCount + 1
                wordCheckDict = {'start':0}
                print(str(fileCount)+ "  " +line[2:] +  " file has finished. ")
            if head == '#@':
                divideWordResult.write(line[:2])
                nameList = line[2:].split(',')
                for k in nameList:
                    tem = '  ' + k
                    divideWordResult.write(tem)
                continue
            words = jieba.posseg.cut(line[2:])
            divideWordResult.write(head)
            for word, flag in words:
                if word.isspace():
                    continue
                if checkRull(flag, word):
                    word = word.replace('\r','').replace('\n','')
                    for k in stopwordMap:
                        if k in word:
                            word = word.replace(k,'')
                    tem = '  ' + word
                    divideWordResult.write(tem)
                    if wordCheckDict.has_key(tem):
                        continue
                    else:
                        wordCheckDict[tem] = 1
                        if fileFrequencyMap.has_key(tem):
                            fileFrequencyMap[tem] = fileFrequencyMap[tem] + 1
                        else:
                            fileFrequencyMap[tem] = 1
            divideWordResult.write('\n')
        else:
            divideWordResult.write('\n')
            checkWordMap.clear()
    divideWordResult.close()
    for key, value in sorted(fileFrequencyMap.iteritems(), key=lambda (k,v): (v,k)):  
        fileFrequency.write(key + ' ' + str(value))
        fileFrequency.write('\n')
time_start = time.time()
dividWord()
time_end = time.time()
a = time_end - time_start
timeSecond = (int)(a%60)
timeMinutes = (int)((a/60)%60)
timeHours = int((a/3600)%24) 
timeDays = int(((a/3600)/24)%30)

print('The function spend ' + str(timeDays) + ' day ' + str(timeHours) + ' hour ' + str(timeMinutes) + ' minutes ' + str(timeSecond) + ' second on running. ' ) 
    
