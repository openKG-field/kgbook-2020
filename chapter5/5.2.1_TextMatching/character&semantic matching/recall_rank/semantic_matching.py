# -*- encoding: utf-8 -*-
"""
@File    : semantic_matching.py
@Time    : 2021/3/20 13:21
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""

#from jiebaCutPackage import jiebaInterface

from  jieba import posseg as pg
import json
import pandas as pd
import  re
hypernym = json.load(open('hypernym.json','r',encoding='utf8'))
print('hypernym 加载成功，共加载 {num}个 '.format(num=len(hypernym)))
synonym = json.load(open('synonym.json','r',encoding='utf8'))
print('synonym 加载成功，共加载 {num}个 '.format(num=len(synonym)))

base_datas = open('./../../../data/test.txt','r',encoding='utf8')
#pubid	applicantList	title	abstract	claims	description	fieldWords	techWords	funcWords	goodsList
# 0         1             2       3            4        5           6            7         8         9
def patent_search(search_words):
    search_element = []
    for i in search_words:
        element = []
        if i in hypernym :
            element = element +  [w.replace("'","") for w in hypernym[i]]
        if i in synonym:
            element = element + [w.replace("'","") for w in synonym[i]]
        element.append(i)
        search_element.append(element)

    result = []
    head = 'pubid	applicantList	title	abstract	claims	description	fieldWords	techWords	funcWords	goodsList'.split('\t')
    for data in base_datas :
        data = data.strip().split('\t')
        content = {}
        if data[0] == 'pubid' : continue
        #print(len(data),len(head))
        if len(data) != len(head) :continue
        for i in range(len(data)):
            content[head[i]] = data[i]
        score = 0
        for ele in search_element:
            for e in ele:
                if e in data[2]:
                    score += 5
                if e in data[3]:
                    score += 3
                if e in data[4]:
                    score += 1
                if e in data[6] or e in data[7] or e in data[8]:
                    score += 10
                if e in data[9] :
                    score += 5
        if score >0 :
            content['score'] = score
            result.append(content)
    return result


def rankValue(vMap, score, reJg):
    '''
    :param vMap:  当前收集权重的map
    :param score:  当前特征的总分
    :param reJg:  正序或倒序的权重指标
    :return:
    '''
    am = len(vMap)
    result = {}
    count = 0
    max = 0
    for k, v in sorted(vMap.items(), key=lambda k: k[1], reverse=reJg):
        if v > max:
            max = v
    for k, v in sorted(vMap.items(), key=lambda k: k[1], reverse=reJg):
        if max == 0:
            result[k] = 0
        else:
            result[k] = float(v) / float(max) * float(score) + 50

    return result




def spendTime(start_time, end_time):
    seconds, minutes, hours = int(end_time - start_time), 0, 0
    hours = seconds // 3600
    minutes = (seconds - hours * 3600) // 60
    seconds = seconds - hours * 3600 - minutes * 60
    print("\n  Complete time cost {:>02d}:{:>02d}:{:>02d}".format(hours, minutes, seconds))


def fourAreaSimilar(datas, aim):

    '''
    techWords':1,'fieldWords':1,'problemWords':1,'funcWords'
    '''
    aimTech = set()
    aimField = set()
    aimProblem = set()
    aimFunc = set()
    pubidTech = {}
    pubidField = {}
    pubidProblem = {}
    pubidFunc = {}
    pubidTitle = {}
    pubidApp = {}
    for data in datas:
        # 收集数据，并将数据统计结果放入map，为后续规则计分排序做准备
        #print(data)
        pubid = data['pubid']
        if 'title' in data:
            pubidTitle[pubid] = data['title']
        if 'applicantList' in data:
            pubidApp[pubid] = data['applicantList']
        if pubid == aim:
            if 'techWords' in data:
                tem = data['techWords'].split('$$')
                if len(tem) > 1:
                    tem.pop(len(tem) - 1)
                    aimTech = set(tem)

            if 'fieldWords' in data:
                tem = data['fieldWords'].split('$$')
                if len(tem) > 1:
                    tem.pop(len(tem) - 1)
                    aimField = set(tem)

            if 'problemWords' in data:
                tem = data['problemWords'].split('$$')
                if len(tem) > 1:
                    tem.pop(len(tem) - 1)
                    aimProblem = set(tem)

            if 'funcWords' in data:
                tem = data['funcWords'].split('$$')
                if len(tem) > 1:
                    tem.pop(len(tem) - 1)
                    aimFunc = set(tem)
        else:
            if 'techWords' in data:
                tem = data['techWords'].split('$$')
                print(tem)
                if len(tem) > 1:
                    tem.pop(len(tem) - 1)
                    pubidTech[pubid] = set(tem)

            if 'fieldWords' in data:
                tem = data['fieldWords'].split('$$')
                if len(tem) > 1:
                    tem.pop(len(tem) - 1)
                    pubidField[pubid] = set(tem)

            if 'problemWords' in data:
                tem = data['problemWords'].split('$$')
                if len(tem) > 1:
                    tem.pop(len(tem) - 1)
                    pubidProblem[pubid] = set(tem)

            if 'funcWords' in data:
                tem = data['funcWords'].split('$$')
                if len(tem) > 1:
                    tem.pop(len(tem) - 1)
                    pubidFunc[pubid] = set(tem)

    techScore = {}
    print('########################',aimTech)
    for i in pubidTech:
        techScore[i] = len(pubidTech[i] & aimTech)
        # print i,techScore[i]
    pCount = 0
    for k, v in sorted(techScore.items(), key=lambda k: k[1], reverse=True):
        pCount += 1

        if pCount > 5:
            break

    techScore = rankValue(techScore, 50, True)
    # for i in techScore:
    #    print i ,techScore[i]

    fieldScore = {}
    for i in pubidField:
        fieldScore[i] = len(pubidField[i] & aimField)

    pCount = 0
    for k, v in sorted(fieldScore.items(), key=lambda k: k[1], reverse=True):
        pCount += 1

        if pCount > 5:
            break
    fieldScore = rankValue(fieldScore, 50, True)

    problemScore = {}
    for i in pubidProblem:
        problemScore[i] = len(pubidProblem[i] & aimProblem)

    pCount = 0
    for k, v in sorted(problemScore.items(), key=lambda k: k[1], reverse=True):
        pCount += 1

        if pCount > 5:
            break

    problemScore = rankValue(problemScore, 50, True)

    funcScore = {}
    for i in pubidFunc:
        funcScore[i] = len(pubidFunc[i] & aimFunc)

    pCount = 0
    for k, v in sorted(funcScore.items(), key=lambda k: k[1], reverse=True):
        pCount += 1

        if pCount > 5:
            break

    funcScore = rankValue(funcScore, 50, True)
    result = {}

    #print('##########################', base_datas)
    base_datas = open('./../../../data/test.txt', 'r', encoding='utf8')
    for data in base_datas:
        pubid = data.strip().split('\t')[0]
        curCount = 0
        amount = 0

        if pubid in techScore:
            amount += techScore[pubid]
            curCount += 1

        if pubid in fieldScore:
            amount += fieldScore[pubid]
            curCount += 1

        if pubid in problemScore:
            amount += problemScore[pubid]
            curCount += 1

        if pubid in funcScore:
            amount += funcScore[pubid]
            curCount += 1
        if curCount < 2:
            curCount = 2

        result[pubid] = float(float(amount) / float(curCount))

    o = open(aim + '.txt', 'w')
    excel = []
    excelHead = ['pubid', 'applicants', 'title', 'fieldWords', 'funcWords', 'problemWords', 'techWords', 'similar']
    excel.append(excelHead)
    for k, v in sorted(result.items(), key=lambda k: k[1], reverse=True):
        excelData = []
        pubid = k
        excelData.append(k)
        if pubid in pubidApp:
            temApp = pubidApp[pubid]

            excelData.append(temApp)
        else:
            excelData.append('')

        if pubid in pubidTitle:
            excelData.append(pubidTitle[pubid])
        else:
            excelData.append('')

        if pubid in pubidField:
            excelData.append('|'.join(list(pubidField[pubid])))
        else:
            excelData.append('')

        if pubid in pubidFunc:
            excelData.append('|'.join(list(pubidFunc[pubid])))
        else:
            excelData.append('')

        if pubid in pubidProblem:
            excelData.append('|'.join(list(pubidProblem[pubid])))
        else:
            excelData.append('')

        if pubid in pubidTech:
            excelData.append('|'.join(list(pubidTech[pubid])))
        else:
            excelData.append('')
        excelData.append(v)

        excel.append(excelData)

    df = pd.DataFrame(excel)
    df.to_csv(aim+'.csv',header=0)

def semantic_search(sentence):
    '''
    :param sentence: 一个用来描述专利的句子，可以是用户输入的一句话，也可以是专利中重要句子的摘抄
    :return:
    '''

    # 句子转成词

    words =[(w,f) for w,f in pg.cut(sentence)]

    #words = re.sub(r'_[0-9]+', '', words).split(',') #获取术语
    search_words = []
    for (w,f) in words :
        if len(w) > 1 and f[0] =='n':
            search_words.append(w)

    enWords = re.findall(r'[A-Z]+', sentence) #部分特殊英文词（由于术语词典覆盖面可能有问题，保证英文术语能及时提取）

    #search_word = [] + words
    for i in enWords:
        search_words.append(i)

    print(search_words)
    patents = patent_search(search_words)
    return patents




def main():
    #利用专利的公开号，与专利本身的主要信息去获取相关专利，并排序存入与 当前专利公开号 同名的 csv文件中
    pubid = 'CN85100284B'
    sentence= u'光调制自动光测弹性应力的方法和装置，属于光测弹性应力技术领域。采用非单色光源以便于作双波长测量，达到可测任意条纹级数值的目的。采用电光调制器以利用其电致双折射特性实现补偿消光。在被测模型前后加有一对旋光器以便得到被测模型相对于正交偏振光场的转动效应。测量过程在微处理机控制下自动进行，测量结果以电信号送微处理机作数据自动处理。本发明提高了光测弹性应力的自动化程度，缩短了测量周期，提高了测量精度。	1、一种光测弹性应力的方法，将被测模型置於正交偏振光场中，在电光调制器无电致双折射补偿的情况下，转动模型一个角度使检偏后的光强最小(非补偿消光态)，此角即表示主应力的方位。然后使模型反转45°，在电光调制器的电致双折射补偿的情况下使检偏后的光强最小(补偿消光态)，则电致双折射光程差就等於应力双折射光程差，由此求得主应力差；本方法的特征在于用旋光法代替测量过程中模型的转动，起偏器的入射光采用非单色光，检偏后的光分成波长为λ与λ的两束光以便测量被测点的条纹级数和主应力的确切方向。$$5、一种由光源〔1〕、起偏器〔2〕、检偏器〔3〕、电光调制器〔4〕、光电转换器〔5〕、监示器〔6〕和电光调制器电源〔15〕组成的用於测量弹性应力的装置;其特征在于光源〔1〕为非单色光源，在被测模型前后有一对旋光器〔8〕和〔9〕，'
    patents = semantic_search(sentence)

    fourAreaSimilar(patents,pubid)

if __name__ == '__main__':
    main()