#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2017年10月20日

@author: zhaoh
'''
from lineModifyTool import lineModify



def minLenWord(w1,w2):
    if len(w1) < w2:
        return w1
    return w2

def testMerge(word , k,):
    if len(k) == len(word):
        return 0
    if len(k)<= 2*3:
        return 0
    if abs(len(k)-len(word))>2*3:
        return 0
    samller = minLenWord(k, word)
    if samller in k and samller in word :
        print k +'  ' + word
def merge(path,outPath):
    wordFile = open(path,'r')
    outFile = open(outPath,'w')
    wordMap = {}
    wordList = list()
    flagList = list()
    for line in wordFile:
        line = lineModify(line)
        wordArray = line.split()
        for word in wordArray:
            wordMap[word] = len(word)
    for k,v in sorted(wordMap.iteritems(), key=lambda k:k[1], reverse = False):
        wordList.append(k)
        flagList.append(v)
    i = 0
    count = 0
    while i<len(wordList):
        print (wordList[i] + '=========>' + str(count))
        count = count + 1
        j= i
        while j< len(wordList):
            if (wordList[i] in wordList[j]) and (wordList[i] != wordList[j]):
                wordList.pop(j)
                flagList.pop(j)
            j = j + 1
        i = i + 1
    for word in wordList:
        outFile.write(word + '\n')
def main():
    path='wordResult.txt'
    outPath = 'mergeWord.txt'
#     w1 = '数据处理模块'
#     w2 = '数据处理'
#     testMerge(w1, w2)
    merge(path, outPath)
    

if __name__ == '__main__':
    main()