#encoding=utf-8
#decoding=utf-8
'''
@author: zhaoh
'''

import sys
import jieba.posseg as pg


wordOutBag = {}
def wordSelect(wordMap):
    topMap = {}
    for k in wordMap:
        words = pg.cut(k)
        for word, flag in words:
            if len(word) <= 3*3:
                if flag[0] == 'n':
                    if topMap.has_key(k):
                        continue
                    else:
                        topMap[k] = wordMap[k]
            else:
                if topMap.has_key(k):
                    continue
                else:
                    topMap[k] = wordMap[k] 
    return topMap

def unionMap(m1, m2):
    unionM = {}
    for k in m1:
        if unionM.has_key(k):
            unionM[k] = unionM[k] + m1[k]
        else:
            unionM[k] = m1[k]
    for k in m2 :
        if unionM.has_key(k):
            unionM[k] = unionM[k] + m2[k]
        else:
            unionM[k] = m2[k]
    return unionM()      
    
def intersectionMap(m1, m2, top):
    intersectionM = {}
    for k in m1:
        if m2.has_key(k):
            if intersectionM.has_key(k):
                intersectionM[k] += 1
            else:
                intersectionM[k] = 1
    return intersectionM
        
        
def weightIndicate(head):
    if head == '#*':
        return 5
    if head == '#!':
        return 3
    if head == '#&':
        return 1
    if head == '#$':
        return 1
    return 0
    
def selectSection(head):
    if head =='#*' or head =='#!' or head =='#&' or head=='#^' or head == '#$':
        return True
    else:
        return False
    
def readPatten(path, OutPath , limited):
    global wordOutBag
    fileCount = 0
    patten = open(path,'r')
    outFile = open(OutPath,'w')
    for line in patten:
        line = line.strip().replace('\r','').replace('\n','')
        head = line[:2]
        body = line[2:]
        if selectSection(head):
            wordArray = body.strip().replace('\r','').replace('\n','').split()
            if head =='#$':
                amount = 0
                count = 0
                fileCount += 1
                print(' The ' + str(fileCount) + ' is starting. ')
                wordBag= {}
                wordWeightBag = {}
                if bool(wordOutBag):
                    outFile.write('#!' + '  ')
                    topMap = wordSelect(wordOutBag)
                    for word,value in sorted(wordOutBag.iteritems(), key=lambda k:k[1], reverse=True) :
                        if len(word) > 3*3:
                            outFile.write(word + '  ')
                            count = count + 1
                        else:
                            words =pg.cut(word)
                            for w,f in words:
                                if f[0]=='n':
                                    outFile.write(word + '  ')
                                    count = count + 1
                                    continue
                        if count > limited:
                            break
                        count += 1
                    outFile.write('\n')
                wordOutBag = {}
                outFile.write(line)
                outFile.write('\n')
                continue
            if head =='#$':
                outFile.write(line)
                outFile.write('\n')
                continue
            if head == '#*':
                outFile.write(line)
                outFile.write('\n')
                continue
            for word in wordArray:
                if wordBag.has_key(word):
                    wordBag[word] += 1
                else:
                    wordBag[word] = 1
                weight = weightIndicate(head)
                amount += weight
                if wordWeightBag.has_key(word):
                    wordWeightBag[word] += weight
                else:
                    wordWeightBag[word] = weight
        if  head =='#&':
            for word in wordBag:
                if wordOutBag.has_key(word):
                    wordOutBag[word] += float(wordWeightBag[word])/float(amount)
                else:
                    wordOutBag[word] = float(wordWeightBag[word])/float(amount)
    outFile.write('#!  ')
    for k,v in sorted(wordOutBag.iteritems(),key=lambda k:k[1], reverse=True):
        if len(k)<=3*3:
            words = pg.cut(k)
            for word,flag in words:
                if flag[0] =='n':
                    if wordOutBag.has_key(word):
                        continue
                    else:
                        outFile.write(k+'  ')
                        continue
        else:
            outFile.write(k + '  ')
def main():
    #path = sys.argv[1]
    #outPath = sys.argv[2]
    #limited = int(sys.argv[3])
    path = 'divideWordResult.txt'
    outPath = 'remodify.txt'
    limited = 30
    readPatten(path, outPath, limited)
if __name__ == '__main__':
    main()