#encoding=utf-8
'''
Created on 2018��4��17��

@author: zhaoh
'''
'''
技术领域

背景技术

发明内容 实用新型内容

附图说明

具体实施方式  具体实施方案

'''
from lineModifyTool import lineModify
from time import time

import re


tech = ['技术领域']
 
back = ['背景技术']

content = ['发明内容',['本发明对','改进'],['本发明','制成'],['本发明','一种'],['上述','缺少'],['本发明','贡献'],'本发明的主要目的'\
           ,'本发明旨在','本发明的目的','本发明的构思','实现本目的的','本发明针对','本发明在于','为了改进',['本发明','要点'],['本发明的任务'],\
           ['本发明','结构'],['本发明','部件'],['合成工艺在'],['构造','原理'],'.内容',['为了','设计'],['发明','技术'],['发明','目的']]

imageDesc = ['附图说明','本发明的详细','图一是','图1','图（1）','图(1)',\
             '附图1','附图1','附图（1）','附图(1)','图二是','图2','图（2）','图(2)',\
             '附图2','附图2','附图（2）','附图(2)','图三是','图3','图（3）','图(3)',\
             '附图3','附图3','附图（3）','附图(3)','附图是','本发明的具体解决方案','实施例','本发明的大致过程','实例',['本发明','实施']]

#operExample = ['具体实施方式','具体实施方案']

rullDict = {'content':content,'imageDesc':imageDesc}


def rullCheck(sentence,tech):
    '''
     :param sentence: 待分词句子
    :param tech: 识别词list，如之前展示的tech
    这里主要支持2个类型的规则识别
   1 首词识别：即找到标记词x，并将sentence中x及x之后的句子内容作为抽取内容或作为类别识别
    2 首尾词识别： 即找到标记词x,y，并将sentence中x，y之间的句子内容作为抽取内容或作为类别识别

    :return:

'''
    sentence = sentence

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
                return True
        else:
            #print 'word rull match'
            if rull in sentence:
                #sub = sentence[ sentence.index(rull) : ]
                return True
    return False
e = open('error.txt','w',encoding='utf8')

errorCount =0
def descriptionAna(desc,pubid):

    '''

    :param desc: 输入的文本内容
    :param pubid: 输入的公开号
    :return: 返回结构化字段
    '''
    global rullDict, errorCount,e
    descDict = {'tech':[],'back':[],'content':[],'imageDesc':[],'abst':[]}
    nextRullList= ['content','imageDesc']
    curKey = ''
    nextRull = ''
    extendCount = 0
    for i in range(len(desc)):
        if desc[i][:2] == '#!':
            abst = desc[i][2:]
            abst = abst.split('。')
            descDict['abst'] = abst
            continue
        if i == 0:
            if '技术领域' in desc[i] and len(desc[i]) <8:
                extendCount += 1

            curKey = 'tech'
        if i == 1+extendCount:
            curKey = 'back'
            nextRull =nextRullList.pop(0)
        if i > 1:
            if nextRull !='' and curKey !='imageDesc':
                if rullCheck(desc[i], rullDict[nextRull]):
                    curKey = nextRull
                    if nextRull != 'imageDesc':
                        nextRull = nextRullList.pop(0)
        descDict[curKey].append(desc[i])

    if len(descDict['tech']) <1 or len(descDict['back']) <1 or len(descDict['content']) <1 :
        #print errorCount
        e.write('pubid : ' + pubid)
        e.write('技术领域 : ' + '\n')
        e.write('\n'.join(descDict['tech']))
        e.write('\n')
        e.write('\n')
        e.write('背景技术 : ' + '\n')
        e.write('\n'.join(descDict['back']))
        e.write('\n')
        e.write('\n')
        e.write('发明内容 : ' + '\n')
        e.write('\n'.join(descDict['content']))
        e.write('\n')
        e.write('\n')
        e.write('附图说明与实施例 : ' + '\n')
        e.write('\n'.join(descDict['imageDesc']))
        e.write('\n')
        e.write('\n')
        return None
    return descDict



    
    
def extractDesc(datas):
    '''

    :param datas:  读取的数据结果

    :return:
    '''
    #CN2+   实用新型

    o = open('descriptionFormat.txt', 'w',encoding='utf8')

    errorCount = 0

    desc_arr = []
    for  data in datas :
        desc = data['description'].split('。')
        pubid = data['pubid']
        #对数据进行分析
        descDict = descriptionAna(desc,pubid)

        #print(descDict)
        desc_arr.append(descDict)
    return desc_arr

def load_data(path):
    datas = []
    count = 0
    header = []
    with open(path,'r',encoding='utf8') as f :
        for line in f :
            line = line.strip().split('\t')
            count += 1
            if count == 1 :
                header = line
            else:
                data = {}
                for i in range(len(line)) :
                    data[header[i]] = line[i]
                datas.append(data)
    return datas

def process():
    path = './/..//..//data//test.txt'

    datas = load_data(path)
    desc_arr = extractDesc(datas)

s = time()

process()


e = time()

print ('spend ', e-s,' second')

        
        
        
        