'''
author: Hongyu Zhao

Data : 09/25/2017 
'''
import os
import sys

def selectWordByValue(value) :
    aimFile = open('writePCValue.txt','r')
    resultFile = open('wordResult.txt','w')
    frequencyDict = {'start':0}
    count = 0
    for line in aimFile :
        tem = line.split()
        if len(tem) == 2:
            word = tem[0] 
            frequency = float(tem[1])
            if frequency >= int(value) :
                frequencyDict[word] = frequency
    for k in sorted(frequencyDict, key=frequencyDict.get, reverse=True):
        count = count + 1
        if k == 'start':
            continue
        resultFile.write(k)
        resultFile.write('\n')
    print('The amount number of words is ' + str(count))
a = input('please enter the limited value for selection')

selectWordByValue(a)
print(a)    
    
