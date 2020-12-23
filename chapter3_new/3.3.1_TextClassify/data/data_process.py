# -*- encoding: utf-8 -*-
"""
@File    : data_process.py
@Time    : 2020/7/5 15:23
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""
import json

import pandas as pd

def ipc_process():
    ipc =  pd.read_csv('ipcDesc.txt',encoding='utf8',header=0,sep='\t\t')

    ipc = ipc[['ipcDesc','ipcVal']]

    ipcDict = {}
    for id,row in ipc.iterrows():
        if type(row['ipcDesc']) is float :
            row['ipcDesc'] = ''
        ipcDict[row['ipcVal']] = row['ipcDesc'].split()

    json.dump(ipcDict,open('ipcDict.json','w',encoding='utf8'))


def target_ana():
    target = ['mainIpcCpc4']
    count =  0
    index = []
    ana = {}

    with open('cluster_data.txt','r',encoding='utf8') as f:
        for line in f :
            line = line.strip().split('\t')
            count += 1
            if count == 1 :
                for i in range(len(line)):
                    if line[i] in target :
                        index.append(i)
            else:
                if len(line) < index[0]: continue
                cur = line[index[0]]
                cur = cur[:4]
                if cur in ana :
                    ana[cur] += 1
                else:
                    ana[cur] = 1

    for k,v in sorted(ana.items(),key=lambda k:k[1],reverse=False):
        print(k,v)

def select_data():


    df = pd.read_csv('cluster_data.txt',header=0,sep='\t')

    #                                                   3                               6           7                                                               12
    select_head = 'patTypeExtended,tfidf_v1,pubDate,techWords,warnLevelRe,pubMonth,applicantFirst,agentList,patType,citedAppidList,kindCode,applicantFirstType,problemWords,fieldWords,funcWords,mainIpcCpc4'

    select_head = select_head.split(',')
    df = df[select_head]
    df = df.to_csv('select_data.txt',sep='\t',encoding='utf8')

def line_process(line,ipcDict):

    target_words = set(ipcDict[line[-1][:4]])

    '''
    feature
    0           1               2               3           4                               
    发明与否      tfidf_cnt      tfidf&tar_cnt   tech_cnt   tech&tar_cnt        
      
    5                   6               7                   8             9                10
    agentList_cnt       problem_cnt     problem&tar_cnt     func_cnt      func&tar_cnt      applicantFirst
    
    11
    target
    
    '''
    tem = []

    i =1
    if line[i] == '发明':
        tem.append(1)
    else:
        tem.append(0)
    i =2
    cur = line[i].split()
    tem.append(len(cur))
    tem.append(len(set(cur) & target_words))
    i = 4
    cur = line[i].split(',')
    tem.append(len(cur))
    tem.append(len(set(cur) & target_words))

    i = 8
    #print(line)
    cur = line[i].split('__')
    tem.append(len(cur))
    i = 13
    cur = line[i].split(',')
    tem.append(len(cur))
    tem.append(len(set(cur)&target_words))
    i = 15
    cur = line[i].split(',')
    tem.append(len(cur))
    tem.append(len(set(cur)&target_words))

    i = 7
    tem.append(line[i])

    cur = line[-1][:4]

    if cur == 'G06F':
        tem.append(1)
    else:
        tem.append(0)

    return tem







def data_process():
    ipcDict = json.load(open('ipcDict.json', 'r', encoding='utf8'))
    count = 0
    header = 'type,tfidf_cnt,tfidf&tar_cnt,tech_cnt,tech&tar_cnt,agentList_cnt,problem_cnt,problem&tar_cnt,func_cnt,func&tar_cnt,applicantFirst,target'

    o = open('model_data','w',encoding='utf8')

    o.write(header+'\n')
    with open('select_data.txt','r',encoding='utf8') as f :
        for line in f :
            if len(line) <1 or line.isspace() : continue

            line = line.strip().split('\t')
            if len(line) < 10: continue

            count += 1
            if count == 1 : continue
            if line[-1][:4] != 'G06F' and line[-1][:4] != 'G06Q' : continue
            line = line_process(line,ipcDict)
            line = [str(i) for i in line]
            o.write(','.join(line) + '\n')



#select_data()
data_process()
