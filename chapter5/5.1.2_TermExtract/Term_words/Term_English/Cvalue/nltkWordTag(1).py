#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@File     : test.py
@Time     : 2021/3/24 15:41
@Author   : zhaohongyu
@Email    : zhaohongyu2401@yeah.net
@Software : PyCharm
"""

'''
CC 连词 and, or,but, if, while,although
CD 数词 twenty-four, fourth, 1991,14:24
DT 限定词 the, a, some, most,every, no
EX 存在量词 there, there's
FW 外来词 dolce, ersatz, esprit, quo,maitre
IN 介词连词 on, of,at, with,by,into, under
JJ 形容词 new,good, high, special, big, local
JJR 比较级词语 bleaker braver breezier briefer brighter brisker
JJS 最高级词语 calmest cheapest choicest classiest cleanest clearest
LS 标记 A A. B B. C C. D E F First G H I J K
MD 情态动词 can cannot could couldn't
NN 名词 year,home, costs, time, education
NNS 名词复数 undergraduates scotches
NNP 专有名词 Alison,Africa,April,Washington
NNPS 专有名词复数 Americans Americas Amharas Amityvilles
PDT 前限定词 all both half many
POS 所有格标记 ' 's
PRP 人称代词 hers herself him himself hisself
PRP$ 所有格 her his mine my our ours
RB 副词 occasionally unabatingly maddeningly
RBR 副词比较级 further gloomier grander
RBS 副词最高级 best biggest bluntest earliest
RP 虚词 aboard about across along apart
SYM 符号 % & ' '' ''. ) )
TO 词to to
UH 感叹词 Goodbye Goody Gosh Wow
VB 动词 ask assemble assess
VBD 动词过去式 dipped pleaded swiped
VBG 动词现在分词 telegraphing stirring focusing
VBN 动词过去分词 multihulled dilapidated aerosolized
VBP 动词现在式非第三人称时态 predominate wrap resort sue
VBZ 动词现在式第三人称时态 bases reconstructs marks
WDT Wh限定词 who,which,when,what,where,how
WP WH代词 that what whatever
WP$ WH代词所有格 whose
WRB WH副词
'''

import nltk
import math
import time
import os
from pymongo import MongoClient
from nltk.corpus import stopwords

#nltk.download('averaged_perceptron_tagger')
def headCheck(head):
    if head =='#!' or head =='#*' or head =='#&' or head =='#%' or head == '#@' or head == '#$':
        return True
    return False

def skipWord(word):
    if word =='and/or' or word =='claim' or word =='example':
        #print('skip happened')
        return True
    return False

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

#checking function for current word and next word
def checkRull(flag):
    if flag[0] == 'N' or flag =='JJ' or flag =='VBG' :
        return True
    return False


# file frequency for each unique word
fileFrequencyWrite = open ('frequency.txt',"w")

# word PC value for each unique word
writePCValue = open('writePCValue.txt',"w")

wordFrequencyWrite = open('wordFrequency.txt',"w")
#'/home/zhy/jieba/merge.txt'

stopwordFile = open('stopword.txt','r')

limitedWord =3
word_dict = {'start':0}
file_dict = {'start':0}
PCV_dict = {'start':0}
wordTword = {'start' : 0}
fileCount = 0

#patent = open('example.txt','r')
import codecs
def load_data(path):
    count = 0
    datas = []
    with codecs.open(path,'r',encoding='utf8') as f :
        for line in f :
            line = line.strip().split('. ')
            datas = [i.strip() for i in line ]
    return datas

def DataManage(path,select_query):
    datas = load_data(path)

    for dataContent in datas:
        file = []
        file.append('#*' + '  ' + dataContent)
        for line in file:
            line = line.lower()
            count = 0
            wordList = list()
            flagList = list()
            combineList = list()
            if len(line) <1 :
                continue
            head =line[:2]
            if not headCheck(head):
                continue
            if len(line) ==2:
                continue
            if line[:2] == "#*":
                global fileCount
                fileCount = fileCount +1
                if fileCount % 1000 == 0:
                    print(str(fileCount) +' is started')
                    # if fileCount > 5000 :
                    #     return 0
                wordCheckDict ={'start':0}
            line = line[2:]
            words = nltk.word_tokenize(line)
            #filtered = [w for w in words if (w not in stopwords.words('english'))]
            # Rfiltered = nltk.pos_tag(filtered)
            word_tag = nltk.pos_tag(words)
            for (word,flag) in word_tag:
                if word =='start':
                    continue
                word = word.strip().lstrip().rstrip(',')
                # if word in stopwordFile:
                #     continue
                if len(word)<2:
                    continue
                count = count + 1
                wordList.append(word)
                flagList.append(flag)
            for i in range(len(wordList)):
                boolControl1 = False
                boolControl2 = False
                pre = False
                if i+1<len(wordList) and (checkRull(flagList[i]) and not flagList[i] == 'POS') and (flagList[i+1][0] =='N' or flagList[i+1] =='VBG' ):
                    if skipWord(wordList[i]) :
                        continue
                    if skipWord(wordList[i+1]) and not flagList[i] =='v':
                        continue
                    if wordList[i] in stopwords.words('english') or wordList[i+1] in stopwords.words('english'):
                        continue
                    
    #                 if flagList[i+1] =='POS' and i+2<len(wordList):
    #                     wordCombine2 = wordList[i] +wordList[i+1] +' ' + wordList[i+2] +'|'
    #                 else:
                    wordCombine2 = wordList[i] +' ' + wordList[i+1]
                    if word_dict.has_key(wordCombine2):
                        word_dict[wordCombine2]= word_dict[wordCombine2]+1;
                        boolControl1 = True
                    else :
                        word_dict[wordCombine2]=1.2;
                        boolControl1 = True
                        combineList.append(wordCombine2)
                    if wordCheckDict.has_key(wordCombine2):
                        wordCheckDict[wordCombine2] = 2
                    else:
                        wordCheckDict[wordCombine2] = 1
                        if file_dict.has_key(wordCombine2):
                            file_dict[wordCombine2] = file_dict[wordCombine2]+1
                        else:
                            file_dict[wordCombine2] = 1
                        
                if i+2<len(wordList) and (checkRull(flagList[i]) and not flagList[i] == 'POS') and (checkRull(flagList[i+1]))and (flagList[i+2][0] =='N' or flagList[i+2] =='VBG') :
                    if skipWord(wordList[i]) or skipWord(wordList[i+1]) :
                        continue
                    if skipWord(wordList[i+2]) and not flagList[i+1] =='v':
                        continue
                    if wordList[i] in stopwords.words('english') or wordList[i+1] in stopwords.words('english') or wordList[i+2] in stopwords.words('english') :
                        continue
                    currentContent = wordList[i]+' ' + wordList[i+1]+' ' + wordList[i+2]
    #                 if flagList[i+1] =='POS' and i+3<len(wordList):
    #                     currentContent = wordList[i]+wordList[i+1]+' ' + wordList[i+2]+ ' ' + wordList[i+3]+ '|'
    #                 if flagList[i+2] =='POS' and i+3<len(wordList):
    #                     currentContent = wordList[i]+' ' + wordList[i+1]+wordList[i+2]+ ' ' + wordList[i+3]+ '|'
                    if word_dict.has_key(currentContent):
                        boolControl2 = True
                        word_dict[currentContent]= word_dict[currentContent]+1;
                    else :
                        boolControl2 = True
                        word_dict[currentContent]=1.3;
                        combineList.append(currentContent)
                    
                    if wordCheckDict.has_key(currentContent):
                        wordCheckDict[currentContent] = 2
                    else:
                        wordCheckDict[currentContent] = 1
                        if file_dict.has_key(currentContent):
                            file_dict[currentContent] = file_dict[currentContent]+1
                        else:
                            file_dict[currentContent] = 1
                if boolControl1 and boolControl2 :
                    key1 = wordList[i]+' ' + wordList[i+1]
                    key2 = wordList[i]+' ' + wordList[i+1]+' ' + wordList[i+2]
                    key3 = wordList[i+1]+' ' + wordList[i+2]
                    if wordTword.has_key(key1):
                        if wordTword[key1].has_key(key2):
                            continue
                        else:
                            wordTword[key1][key2] = 1
                    else:
                        wordTword[key1] ={'start':0}
                        wordTword[key1][key2] = 1
                if not boolControl1 and boolControl2:
                    key1 = wordList[i]+' ' + wordList[i+1]
                    key2 = wordList[i]+' ' + wordList[i+1]+' ' + wordList[i+2]
                    key3 = wordList[i+1]+' ' + wordList[i+2]
                    if wordTword.has_key(key3):
                        if wordTword[key3].has_key(key2):
                            continue
                        else:
                            wordTword[key3][key2] = 1
                    else:
                        wordTword[key3] = {'start' : 0}
                        wordTword[key3][key2] = 1
def main():
    time_start = time.time()
    cwd=os.getcwd()
    print(cwd)
#================ this is how to start the function and exact information by select_query map
    path = './UStitle1.txt'
    select_query = {}
    DataManage(path,select_query)
#================ this is how to process information and save them into a static file which will be applied by the next function     
    global word_dict, file_dict , wordTword, limitedWord, PCV_dict
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
        if value >0 :
            fileFrequencyWrite.write((key + "| " + str(value)).encode('utf-8'))
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
        if len(evaluateList)>0 and evaluateCount == evaluateList[0]:
            print(value)
            evaluateList.pop(0)
        key = key.replace(' ','-')
        writePCValue.write((key + "| " + str(value)).encode('utf-8'))
        writePCValue.write('\n')
        wordPCVcount = wordPCVcount + 1
    print("the amount number of length 3 word is " + str(wordL3Count))
    
    wordFrequencyWrite.close()
    writePCValue.close()
    fileFrequencyWrite.close()
         
    
    
    time_end = time.time()
    a = time_end - time_start
    
    timeSecond = (int)(a%60)
    timeMinutes = (int)((a/60)%60)
    timeHours = int((a/3600)%24) 
    timeDays = int(((a/3600)/24)%30)
    
    print('The function spend ' + str(timeDays) + ' day ' + str(timeHours) + ' hour ' + str(timeMinutes) + ' minutes ' + str(timeSecond) + ' second on running. ' ) 

if __name__ == '__main__':
    main()

