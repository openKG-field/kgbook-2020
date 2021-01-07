#encoding=utf-8
'''
author: Hongyu Zhao

Data : 09/25/2017 
'''
#flag keyword by jieba function and exact keywords by flag and combination 
import time
import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

sys.path.append("../")

import jieba
import jieba.posseg
jieba.load_userdict("userdict.txt")
import math

# file frequency for each unique word
fileFrequencyWrite = open ('frequency.txt',"w")

# word PC value for each unique word
writePCValue = open('writePCValue.txt',"w")

wordFrequencyWrite = open('wordFrequency.txt',"w")
#'/home/zhy/jieba/merge.txt'


file = open('xmlResult.txt',"r")
limitedWord =2



word_dict = {'start':0}
file_dict = {'start':0}
PCV_dict = {'start':0}
wordTword = {'start' : 0}
fileCount = 0

def skipWord(word):
    if word =='方法' or word =='时' or word =='装置' or word =='步骤' or word =='模式' or word =='设备' or word =='内' or word =='到' or word =='使' or word =='使得' or word=='无法':
        return True
    return False


def selectContent(head):
    if head == "#@" or head =="#!" or head == "#^":
        return True
    return False

  
#calculate the pc-value for each word
def PCValue(a, word_dict, file_dict, selection, wordTword, limitedWord):
    if selection == 'a':
        Va =math.log(3)* word_dict[a]+2*file_dict[a]
        return Va
    elif selection =='b':
        extendCount = 0
        extendFrequency = 0
        if wordTword.has_key(a):
            for word in wordTword[a]:
                if word_dict[a] < limitedWord or word =='start':
                    continue
                extendCount = extendCount + 1
                extendFrequency = extendCount + word_dict[word]
            Vb = (word_dict[a] - 1/extendCount*extendFrequency )+file_dict[a]  
        else:
            Vb = word_dict[a] + file_dict[a]
    return Vb


#checking function for pre-word
def checkPre(flag):
    if flag[0] =="v" or flag == "l" or flag =="q":
        return True
    return False
#checking function for current word and next word
def checkRull(flag):
    if flag == "n" or flag == "l"  or flag == "vn"  or flag == "eng" or flag == "v" or flag =="q":
        return True
    return False

# def createMongo(dbName,tbName,host="localhost",port=27017):
#     conn = MongoClient(host,port)
#     db = conn[dbName]
#     collection = db[tbName]
#     return (conn,db,collection)
#data manage function for 
def DataManage():
    for line in file:
        count=0
        wordList = list()
        flagList = list()
        combineList = list()
        
        if len(line)>1 and ((line[:2]=="#!" and line[:3] !='#!1') or line[:2]=="#*"):
            if line[:2] =="#*":
                global fileCount
                fileCount = fileCount +1
                wordCheckDict ={'start':0}
                print(str(fileCount) +  " file has finished. ") 
            words = jieba.posseg.cut(line[2:])
            for word, flag in words:
                word = word.decode('utf-8')
                if word =='start':
                    continue
                count = count + 1
                word = word.decode('utf-8')
                wordList.append(word)
                flagList.append(flag)
            for i in range(len(wordList)):
                boolControl1 = False
                boolControl2 = False
                pre = False
                if flagList[i] == "v":
                    if i-2 >= 0 and (checkPre(flagList[i-2]) or checkPre(flagList[i-1])):
                        pre = True
                    elif i -1 >= 0 and checkPre(flagList[i-1]):
                        pre = True
                    if not pre :
                        continue
                if i+1<len(wordList) and (checkRull(flagList[i]) or flagList[i] == "a" and not flagList[i] =='v') and flagList[i+1][0]=="n" :
                    if len(wordList[i]+wordList[i+1]) > 6:
                        continue
                    if skipWord(wordList[i]) :
                        continue
                    if skipWord(wordList[i+1]) and not flagList[i] =='v':
                        continue
                    if word_dict.has_key(wordList[i]+wordList[i+1]):
                        word_dict[wordList[i]+wordList[i+1]]= word_dict[wordList[i]+wordList[i+1]]+1;
                        boolControl1 = True
                    else :
                        word_dict[wordList[i]+wordList[i+1]]=1.2;
                        boolControl1 = True
                        combineList.append(wordList[i]+wordList[i+1])
                    if wordCheckDict.has_key(wordList[i]+wordList[i+1]):
                        wordCheckDict[wordList[i]+wordList[i+1]] = 2
                    else:
                        wordCheckDict[wordList[i]+wordList[i+1]] = 1
                        if file_dict.has_key(wordList[i]+wordList[i+1]):
                            file_dict[wordList[i]+wordList[i+1]] = file_dict[wordList[i]+wordList[i+1]]+1
                        else:
                            file_dict[wordList[i]+wordList[i+1]] = 1
                    
                if i+2<len(wordList) and (checkRull(flagList[i]) and not flagList[i] == 'v') and checkRull(flagList[i+1]) and flagList[i+2][0]=="n" :
                    if len(wordList[i]+wordList[i+1]+wordList[i+2]) > 6:
                        continue
                    if skipWord(wordList[i]) or skipWord(wordList[i+1]) :
                        continue
                    if skipWord(wordList[i+2]) and not flagList[i+1] =='v':
                        continue
                    if word_dict.has_key(wordList[i]+wordList[i+1]+wordList[i+2]):
                        boolControl2 = True
                        word_dict[wordList[i]+wordList[i+1]+wordList[i+2]]= word_dict[wordList[i]+wordList[i+1]+wordList[i+2]]+1;
                    else :
                        boolControl2 = True
                        word_dict[wordList[i]+wordList[i+1]+wordList[i+2]]=1.3;
                        combineList.append(wordList[i]+wordList[i+1]+wordList[i+2])
                    currentContent = wordList[i]+wordList[i+1]+wordList[i+2]
                    if wordCheckDict.has_key(currentContent):
                        wordCheckDict[currentContent] = 2
                    else:
                        wordCheckDict[currentContent] = 1
                        if file_dict.has_key(currentContent):
                            file_dict[currentContent] = file_dict[currentContent]+1
                        else:
                            file_dict[currentContent] = 1
                if boolControl1 and boolControl2 :
                    key1 = wordList[i]+wordList[i+1]
                    key2 = wordList[i]+wordList[i+1]+wordList[i+2]
                    key3 = wordList[i+1]+wordList[i+2]
                    if wordTword.has_key(key1):
                        if wordTword[key1].has_key(key2):
                            continue
                        else:
                            wordTword[key1][key2] = 1
                    else:
                        wordTword[key1] ={'start':0}
                        wordTword[key1][key2] = 1
                if not boolControl1 and boolControl2:
                    key1 = wordList[i]+wordList[i+1]
                    key2 = wordList[i]+wordList[i+1]+wordList[i+2]
                    key3 = wordList[i+1]+wordList[i+2]
                    if wordTword.has_key(key3):
                        if wordTword[key3].has_key(key2):
                            continue
                        else:
                            wordTword[key3][key2] = 1
                    else:
                        wordTword[key3] = {'start' : 0}
                        wordTword[key3][key2] = 1
        else:
            continue
def __init__():
    time_start = time.time()
    cwd=os.getcwd()
    print(cwd)

    DataManage()
    #collect data and manage them 
    combineCount = 0 
    limitCount = 0
    wordL3Count = 0
    wordPCVcount = 0
    commentCount = 0
    for key, value in sorted(word_dict.iteritems(), key=lambda (k,v): (v,k)):  
        combineCount = combineCount + 1      
        if value > limitedWord and str(value)[len(str(value))-1]=="3":
            limitCount = limitCount + 1
            pcV = PCValue(key, word_dict,file_dict, 'a',wordTword, limitedWord)
            PCV_dict[key] = pcV
            commentCount = commentCount + 1
            print('The ' + str(commentCount) + ' word has been finished')
            #print('{0:10}  {1:10f}'.format(key, value))
    for key, value in sorted(word_dict.iteritems(), key=lambda (k,v): (v,k)):  
        #combineCount = combineCount + 1      
        if value > limitedWord and str(value)[len(str(value))-1]=="2":
            pcV = PCValue(key, word_dict,file_dict,  "b", wordTword, limitedWord)
            PCV_dict[key] = pcV
            commentCount = commentCount + 1
            print('The ' + str(commentCount) + ' word has been finished')
            wordL3Count = wordL3Count + 1
            limitCount = limitCount + 1
            #print('{0:10}  {1:10f}'.format(key, value))
    for key, value in sorted(word_dict.iteritems(), key=lambda (k,v): (v,k)): 
        wordFrequencyWrite.write((key + '  ' + str(value)).encode('utf-8'))
        wordFrequencyWrite.write('\n')
    frequencyWordNumber = 0
    fileFrequencyWrite.write(str(fileCount))
    fileFrequencyWrite.write('\n')
    for key, value in sorted(file_dict.iteritems(), key=lambda (k,v): (v,k)): 
        if value >2 :
            fileFrequencyWrite.write((key + "   " + str(value)).encode('utf-8'))
            fileFrequencyWrite.write('\n')
            frequencyWordNumber = frequencyWordNumber + 1
    print("the amount number of frequency words is " + str(frequencyWordNumber))
    print("the amount number of files is  " + str(fileCount))        
    print ("the amount number of final terms is  " + str(limitCount))
    # write words in file sorted by pcv value 
    evaluateList = []
    evaluateList.append(int(float(limitCount)/3*2))
    evaluateList.append(int(float(limitCount)/4*3))
    evaluateList.append(int(float(limitCount)/5*4))
    evaluateList.append(int(float(limitCount)/6*5))
    evaluateList.append(int(float(limitCount)/7*6))
    evaluateCount = 0
    for key, value in sorted(PCV_dict.iteritems(), key=lambda (k,v): (v,k)): 
        evaluateCount = evaluateCount + 1
        key = key.encode('utf-8')
        if len(evaluateList)>0 and evaluateCount == evaluateList[0]:
            print(value)
            evaluateList.pop(0)
        if len(key)> 6*3:
            continue
            print(len(key))
        writePCValue.write((key + "   " + str(value)).encode('utf-8'))
        writePCValue.write('\n')
        wordPCVcount = wordPCVcount + 1
    print("the amount number of length 3 word is " + str(wordL3Count))
    

    writePCValue.close()
    fileFrequencyWrite.close()
    
    
    
    time_end = time.time()
    a = time_end - time_start
    
    timeSecond = (int)(a%60)
    timeMinutes = (int)((a/60)%60)
    timeHours = int((a/3600)%24) 
    timeDays = int(((a/3600)/24)%30)
    
    print('The function spend ' + str(timeDays) + ' day ' + str(timeHours) + ' hour ' + str(timeMinutes) + ' minutes ' + str(timeSecond) + ' second on running. ' ) 
__init__()  
