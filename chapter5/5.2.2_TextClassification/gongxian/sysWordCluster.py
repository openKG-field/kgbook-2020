# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

from gensim.models import word2vec
import codecs

modelname = '/home/pydep/transport/w2v/wc.model'

def initText(handle_path):
    global pubid
    a = codecs.open(handle_path, 'r', 'utf-8')
    lines = a.readlines()
    idAndword = {}
    detail_list = []
    for line in lines:
        line = line.replace("\n", "")
        line = line.replace("\r", "")
        techWord_list = []
        if 'pubid' in line:
            pubid = line.replace("pubid : ", "")
        elif 'appYear' in line:
            appYear = line.replace("appYear: ", "")
            detail_list.append(appYear)
        elif 'applicant' in line:
            applicant = line.replace("applicant: ", "")
            detail_list.append(applicant)
        elif 'techWord' in line:
            tmp = ""
            techWord = line.replace("techWord : ", "")
            for t in techWord:
                if t != " ":
                    tmp += t
                elif t == " ":
                    techWord_list.append(tmp)
                    tmp = ""
            if tmp != '':
                techWord_list.append(tmp)
            detail_list.append(techWord_list)
            idAndword[pubid] = detail_list
            detail_list = []
    return idAndword

def get_field(base_path):
    a = codecs.open(base_path, 'r', 'utf-8')
    lines = a.readlines()
    field_list = []
    for line in lines:
        if 'field' in line:
            line = line.replace('    field  :  ', '')
            word = ''
            for l in line:
                if l != ' ':
                    word += l
                elif l == ' ':
                    if word != '':
                        field_list.append(word)
                    word = ''
    a.close()
    return field_list

def get_techword(handle_path):
    a = codecs.open(handle_path, 'r', 'utf-8')
    lines = a.readlines()
    techword_list = []
    for line in lines:
        if 'techWord : ' in line:
            line = line.replace('techWord : ', '')
            word = ''
            for l in line:
                if l != ' ':
                    word += l
                elif l == ' ':
                    if word != '':
                        techword_list.append(word)
    a.close()
    return techword_list

def get_similar(field_list, techword_list, modelname):
    model = word2vec.Word2Vec.load(modelname)
    similar_dict = {}
    for field in field_list:
        similar_dict[field] = {}
    for field in field_list:
        tmp_dict = {}
        for techword in techword_list:
            if field != techword:
                try:
                    similarity = model.similarity(field, techword)
                except KeyError:
                    similarity = 0
                tmp_dict[techword] = similarity
        tmp_dict = dict(sorted(tmp_dict.items(), key=lambda x:x[1], reverse=True))
        similar_dict[field] = tmp_dict
    return similar_dict

def deal_dict(word_dict, result_dict):
    if len(word_dict) >= 2:
        key = list(word_dict.keys())[0]
        key_list = word_dict[key]
        word_dict.pop(key)
        outword = []
        output = ''
        outword.append(key)
        for alpha in word_dict:
            if key in word_dict[alpha] and alpha in key_list:
                outword.append(alpha)
                for a in word_dict[alpha]:
                    if a not in key_list:
                        key_list.append(a)
        for out in outword:
            output += out + ' '
        if output != '':
            result_dict[output] = key_list
        if len(outword) != 1:
            for c in outword:
                if c != key:
                    word_dict.pop(c)
        result_dict = deal_dict(word_dict, result_dict)
    elif len(word_dict) == 1:
        key = list(word_dict.keys())[0]
        key_list = word_dict[key]
        result_dict[key] = key_list
    return result_dict

def find_similar(word_list, modelname):
    similar_dict = {}
    model = word2vec.Word2Vec.load(modelname)
    for key in word_list:
        result = model.most_similar(key)
        result_word = []
        for each in result:
            result_word.append(each[0])
        similar_dict[key] = result_word
    return similar_dict

def gongxian(idAndword, similar_dict):
    result_dict = {}
    for key in similar_dict:
        level_list = similar_dict[key]  # 每个类中的词
        level_list.append(key)
        for word in level_list:
            for id in idAndword:
                if word in idAndword[id]:
                    try:
                        result_dict[word].append(id)
                    except KeyError:
                        result_dict[word] = [id]
    return result_dict

def calculate(similar_dict, idAndword, modelname):
    similar_result = {}
    for id in idAndword:
        similar_result[id] = []
    model = word2vec.Word2Vec.load(modelname)
    for key in similar_dict:
        tmp = similar_dict[key]  # 1个类里的词
        level = []
        level.append(key)
        for each in tmp:
            level.append(each)  # 类中所有需要计算关联度的词
        length = len(level)  # 类中相似词个数
        for id in idAndword:  # 遍历专利
            patent_word_list = idAndword[id]  # 获取专利号的所有关键词
            similar_list = []   # 一个专利所有关键词对应的平均相似度
            for patent_word in patent_word_list:  # 遍历关键词
                sim = 0
                for level_word in level:  # 遍历类和类的相似词
                    try:
                        sim += model.similarity(patent_word, level_word)
                    except KeyError:
                        length -= 1
                if length != 0:
                    sim = sim/length  # 关键词中相似度的平均值
                else:
                    sim = 0
                similar_list.append(sim)
            score = 0
            for similar in similar_list:  # 取最高的相似度平均值
                if similar > score:
                    score = similar
            similar_result[id].append(score)
    return similar_result  # dict格式：专利号:[相似度]

def to_level(similar_result, word_dict):
    for similar in similar_result:
        score_list = similar_result[similar]
        tmp = 0
        for score in score_list:
            if score > tmp:
                tmp = score
        index = score_list.index(tmp)  # 获取最大相似度的下标
        flag = 0
        for word in word_dict:
            if flag == index:
                word_dict[word].append(similar)
            flag += 1
    return word_dict

def output(idAndword, output_list):
    details = []
    sort_dict = {}
    for id in output_list:
        sort_dict[id] = idAndword[id][0]
    for id in sorted(sort_dict, key=lambda x: sort_dict[x]):
        detail = idAndword[id]
        if len(detail) == 1:
            details.append(id)
        elif len(detail) == 2:
            details.append(id + '  ' +detail[0])
        elif len(detail) == 3:
            details.append(id + '  ' + detail[0] + '  ' + detail[1])
        else:
            tem = id + '  ' + detail[0] + '  '
            for i in range(1, len(detail) - 2):
                if i == len(detail) - 3:
                    tem += detail[i]
                else:
                    tem += detail[i] + ','
            details.append(tem)
    return details

def auto_cluster(idAndword, field_list):
    yz = 0.25
    techword_list = []
    for id in idAndword.keys():
        techword_list += idAndword[id][-1]
    similar_dict = get_similar(field_list, techword_list, modelname)
    b_dict = {}
    for similar in similar_dict:
        a_dict = similar_dict[similar]
        flag = 0
        for a in a_dict:
            if a_dict[a] > yz:
                flag += 1
        if flag != 0:
            b_dict[similar] = flag
    b_dict = dict(sorted(b_dict.items(), key=lambda x: x[1], reverse=True))
    hb_dict = {}
    for similar in b_dict:
        similar_list = []
        tmp_dict = similar_dict[similar]
        for tmp in tmp_dict:
            if tmp_dict[tmp] >= yz:
                similar_list.append(tmp)
        hb_dict[similar] = similar_list
    result_dict = {}
    result_dict = deal_dict(hb_dict, result_dict)
    length_dict = {}
    for result in result_dict:
        length_dict[result] = len(result_dict[result])
    length_dict = dict(sorted(length_dict.items(), key=lambda x: x[1], reverse=True))
    result = {}
    getted = []
    for key in length_dict:
        tec_dict = {}
        for a in result_dict[key]:
            if a in getted:
                continue
            getted.append(a)
            output_list = []
            for id in idAndword:
                if a in idAndword[id][-1]:
                    output_list.append(id)
            tec_dict[a] = output(idAndword, output_list)
        result[key] = tec_dict
    return result

def input_cluster(idAndword_w, class_list):
    flag = 1  # --------------------------词频----------------------------------#
    class_dict = {}
    for cla in class_list:
        class_dict[cla] = []

    idAndword = {}
    for key in idAndword_w.keys():
        idAndword[key] = idAndword_w[key][-1]

    similar_dict = find_similar(class_list, modelname)
    result_dict = gongxian(idAndword, similar_dict)

    # 构建其他
    result_dict['其他'] = []
    tmp = []
    for key in result_dict:
        tmp += result_dict[key]
    for key in idAndword:
        if key not in tmp:
            result_dict['其他'].append(key)

    idAndword_new = {}
    for id in result_dict['其他']:
        idAndword_new[id] = idAndword[id]

    similar_result = calculate(similar_dict, idAndword_new, modelname)
    class_dict = to_level(similar_result, class_dict)

    # w2v关联度计算后的其他
    other = result_dict['其他']
    other_tmp = {}
    other_result = {}
    for each in other:
        words = idAndword[each]
        for word in words:
            try:
                other_tmp[word] += 1
            except KeyError:
                other_tmp[word] = 1
    other_tmp = dict(sorted(other_tmp.items(), key=lambda x: x[1], reverse=True))
    for tmp in other_tmp:
        if other_tmp[tmp] >= flag:
            other_result[tmp] = []
    for tmp in other_result:
        for id in idAndword_new:
            if tmp in idAndword_new[id]:
                other_result[tmp].append(id)

    result = {}
    for similar in similar_dict:
        tec_dict = {}
        similar_list = similar_dict[similar]
        similar_list.append('其他')
        for a in similar_list:
            if a != '其他':
                try:
                    b = result_dict[a]
                    tec_dict[a] = output(idAndword_w, b)
                except KeyError:
                    pass
            elif a == '其他':
                b = class_dict[similar]
                tec_dict[a] = output(idAndword_w, b)
        result[similar] = tec_dict
    tec_dict = {}
    for d in other_result:
        other_list = other_result[d]
        tec_dict[d] = output(idAndword_w, other_list)
    result['其他'] = tec_dict
    return result
from pymongo import MongoClient
def boolMongo(tb):
    global port
    host = '192.168.1.10'
    host = '182.18.59.57'
    dbName = 'mqpat'
    user = 'mqpat-rw'
    passwd = '123456'
    port = 27017
    myTbNme = tb
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[myTbNme]
    return (conn,db,collection) 


from jiebaCutPackage.jiebaInterface import jiebaCut
def dataProcess(fieldsName):
    
    resultDict = {}
    (conn,db,col)= boolMongo('fieldsIndivideBase')
    for data in col.find({'fieldsName':fieldsName,'type':'cn','noisyType':'O'},{'pubid':1,'techArea':1}).batch_size(100):
        if 'techArea' not in data:
            continue
        techArea = jiebaCut(data['techArea'])
        techArea = techArea.replace('_1','')
        pubid = data['pubid']
        if pubid in resultDict:
            continue
        else:
            resultDict[pubid] = ['','',techArea.decode('utf-8').split(',')]
    
    return resultDict

import json
def getFieldList(fieldsName):
    field_list = []
    (coon,db,col) = boolMongo('techEvolution')
    for data in col.find({'fieldsName':fieldsName},{'evolution':1}).batch_size(1):
        if 'evolution' not in data :
            continue
        e = json.loads(data['evolution'])
        #print e
        for year in e:
            if 'field' not in e[year]:
                continue
            fields = e[year]['field']
            for field in fields:
                for k in field:
                    if k.isspace() or len(k) < 1 :
                        continue
                    else:
                        field_list.append(k.replace('_1',''))
            
    return field_list  
     

    
def clusterProcss(fieldsName,field_list=None):
    idAndWord = dataProcess(fieldsName)
    if field_list == [] or field_list==None:
        field_list = getFieldList(fieldsName)

        return auto_cluster(idAndWord, field_list) # 自动聚类
    else:
        return input_cluster(idAndWord, field_list) # 人工聚类 

a = clusterProcss('人工智能芯片')

