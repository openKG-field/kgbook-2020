#encoding=utf-8
'''
Created on 2017年10月24日

@author: zhaoh
'''
import sys
from nltk.corpus import stopwords
from lineModifyTool import lineModify
def readFile(inPath, outPath):
    inFile = open(inPath,'r')
    outFile = open(outPath,'w')
    count = 0
    for line in inFile:
        line = lineModify(line)
        line = line.decode('utf-8')
        head = line[:2]
        if head == '#$':
            outFile.write(line+'\n')
            continue
        if head =='#^':
            outFile.write(line)
            outFile.write('\n')
        if head == '#*':
            count = count + 1
            print (str(count)+ ' ' + line + ' is beginning')
        words = line[2:].split()
        outFile.write(head+'  ')
        for word in words:
            if word not in stopwords.words('english'):
                outFile.write(word.encode('utf-8')+'  ')
        outFile.write('\n')
        if head =='#!':
            outFile.write('\n')
if __name__ == '__main__':
#1. inPath is the result of interesting_vector
#2. outPath is the result of EnglishStopWord output
    #inPath = sys.argv[1]
    #outPath = sys.argv[2]
    inPath = 'remodify.txt'
    outPath = 'finally.txt'
    readFile(inPath, outPath)