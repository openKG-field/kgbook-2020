# -*- encoding: utf-8 -*-
"""
@File    : techArea.py
@Time    : 2021/3/19 10:19
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""


import re
import json

techField = [['发明','涉及'],'本发明属于',['属','领域'],'发明公开了','一种',['一种','方法'],'总体涉及','是一种',['涉及', '领域'],'公开了',['涉及', '一种'],['用于', '领域'],  ['涉及', '领域'],['用于', '方法']]
def extractSentByRull(sentence,tech,functionType=0):
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
                sub = sentence[ sentence.index(rull[0]) :]
                return sub
        else:
            #print 'word rull match'
            if rull in sentence:
                sub = sentence[ sentence.index(rull) : ]
                return sub
    return ''



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







def extractTechArea(path,language=1):
    '''

    :param path: data 数据路径, 参考代码中统一的data格式
    :param language : 语言， language=1 时 默认为中文,当前只支持中英文
    :return:
    '''
    o = open('techAreaResult.txt','w',encoding='utf8')
    datas =load_data(path)
    count = 0
    if language == 1 :
        for data in datas :
            count += 1
            desc = data['description']
            pubid = data['pubid']
            p1 = '['
            p2 = '；|。|'
            p3 = '\\n]'
            area = ''
            desc = re.split(p1+p2+p3,desc)
            #将无用分割符统一切分并按照空格合并
            desc = ' '.join(desc)
            desc = desc.split()
            acount = 0
            tech_sent = ''
            for i in range(len(desc)-1):
                acount += 1
                #通过关键词 技术领域 抽取相关的描述信息
                if '技术领域' in desc[i]:
                    if len(desc[i+1]) < 7 or not re.match(r'.*[\u4e00-\u9fa5].*|.*[^\x00-\xff].*',desc[i+1]):
                        if i+2 < len(desc) -1 :
                            area = desc[i+2]
                        else:
                            area = desc[i+1]
                    else:
                        area = desc[i+1]
                    break
                if acount > 5:
                    if area == '':
                        area = desc[0]+'\n' + desc[1]
                    break
                if i < 3:
                    tech_sent = tech_sent + '\t' + extractSentByRull(desc[i], techField)

            count += 1
            if count % 500 == 0:
                print (count,pubid,' Done ')
            #将结果保存为 techArea
            body = {'pubid':pubid,'techArea':area,'tech_sent':tech_sent}
            o.write(json.dumps(body)+'\n')
    else:
        #英文处理逻辑与中文一致，只是具体关键词与切分有所不同
        for data in datas :
            desc = data['description']
            pubid = data['pubid']
            area = ''
            desc = re.split(r'[.|;]', desc)
            acount = 0

            for i in range(len(desc)):
                wordLen = desc[i].strip().split()
                if wordLen < 8:
                    continue
                if len(desc[i]) < 10 or desc[i].isupper():
                    continue
                area = desc[i].replace('Field of the Invention', '').replace('BACKGROUND OF THE INVENTION', '')
                break

            count += 1


            body = {'pubid': pubid, 'techArea': area}

            o.write(json.dumps(body) + '\n')
path = './/..//data//test.txt'
extractTechArea(path)
    

    

    
    
    
    
    
    