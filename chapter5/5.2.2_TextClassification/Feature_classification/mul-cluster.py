#coding=utf-8
'''
Created on 2019��1��18��

@author: zhaoh
'''



def dataProcess(path):
    patent = {}
    count = 0
    with open(path,'r',encoding='utf8'  ) as f :
        for line in f :
            line = line.strip().split('\t')
            count += 1
            if count == 1 :continue
            data = {}
            data['goods']= line[9].split('$$')
            data['words'] = line[6].split('$$') + line[7].split('$$')
            patent[line[0]] = data
            # print(data)


    return patent

def cluster(lineList,curKey):
    cDict = {}
    indexList = []
    for index in range(len(lineList)):
        [k,c] = lineList[index]
        if k==curKey:
            #print index
            indexList.append(index)
    for i in range(len(indexList)):
        if i+1 >= len(indexList):
            temList = lineList[indexList[i]:]
        else:
            temList = lineList[indexList[i]:indexList[i+1]+1]
        clusterName = lineList[indexList[i]][1]
        cDict[clusterName] = {}
        cDict[clusterName] = cluster(temList,curKey+1)
    
    return cDict

def displayDict(cDict,head):
    if type(cDict) is dict:
        for i in cDict:
            #print head + i
            displayDict(cDict[i], head+'    ')
    else:
        return 0
     
    
def clusterData(path):
    f = open(path,'r',encoding='utf8')
    lineList = []
    for line in f:
        if line.isspace() or len(line) < 1 :
            continue
        line = line.replace('\n','')
        fg = False
        for i in range(5,0,-1):
            if (i*'\t') in line:
                line = line.replace((i*'\t'),(str(i) + ' '))
                fg= True
                break
        if not fg:
            line = '0 ' + line
        [k,c] = line.split()
        lineList.append([int(k),c])
    for i in lineList:
        [k,c] = i
    cDict = cluster(lineList, 0)
    return cDict

def clusterProcess(cDict,goods,words):
    cur = []
    for i in cDict:
        if u'\ufeff' in i:
            i = i.replace(u'\ufeff','')
        if i.isspace() or len(i) < 1 :
            continue
        cur.append(i)
    inter = list( set(cur) & set(goods) )
    if len(inter) == 0 :
        inter = list( set(cur) & set(words) )
        
    if len(inter) > 0 :
        max = -1
        returnList = []
        for c in inter:
            tem = clusterProcess(cDict[c], goods, words)
            if len(tem) > max:
                max = len(tem)
                returnList = [c] + tem
        return returnList
    else:
        return []

def clusterMain(fieldsName,newField=None):
    missCount = 0

    patent  = dataProcess(fieldsName)

    path = 'stuff.txt'
    cDict  = clusterData(path)

    pubidCluster = {}
    for i in patent:
        goods = patent[i]['goods']
        words = patent[i]['words']
        max = 0
        temList = []
        for c in cDict:
            tem = clusterProcess(cDict[c], goods, words)

            if len(tem) > max:
                max = len(tem)
                temList = [c] +  tem
        if max >0 :
            pubidCluster[i] = temList
        else:
            pubidCluster[i] = []
    pubidClusterDict = {}
    for i in pubidCluster:
        cur = pubidCluster[i]
        if len(cur) == 0 :
            missCount += 1
            #print i, ' miss'
        else:
            pubidClusterDict[i] = cur
            #print'exists = ', i , ' '.join(cur)
    #print 'amount miss = ',missCount

    return pubidClusterDict

                

data_path = './/..//..//data//test.txt'
classes = clusterMain(data_path)
print(classes)





