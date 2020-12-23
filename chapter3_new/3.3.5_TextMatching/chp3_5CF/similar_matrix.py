#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : books_method
# @File : similar_matrix.py
# @Time    : 2020/6/18 17:35
# @Author  : Zhaohy

import pandas as pd
import numpy as np
import json

'''
CF :  mainIpc3(applicant) 作为user ,   techWord,funcWord,techword&funcword,goodslist,warnlevelRe作为 item相似评价维度 产出 top N 推荐数据
'''

'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 23890 entries, 0 to 23889
Data columns (total 13 columns):
pubid             23890 non-null object
fieldsName        23890 non-null object
applicantFirst    23887 non-null object
fieldWords        21874 non-null object
techWords         21849 non-null object
funcWords         20609 non-null object
tfidf_v1          22104 non-null object
goodsList         4968 non-null object
warnlevelRe       0 non-null float64
indLen            0 non-null float64
claimsIndCount    23309 non-null float64
feature           0 non-null float64
mainIpc3          23886 non-null object
dtypes: float64(4), object(9)
memory usage: 2.4+ MB
None
'''


def similar_process(key, df):
    similar_dict = {}

    for c_n, c_row in df.iterrows():
        tem_dict = {}
        cur_pubid = c_row['pubid']
        cur_key = c_row[key]
        if type(cur_key) != str: continue
        cur_key = cur_key.split(',')
        if len(cur_key) == 0: continue
        for n, row in df.iterrows():
            pubid = row['pubid']
            if pubid == pubid: continue
            similar_key = row[key]

            similar_key = similar_key.split(',')

            similar = float(len(set(cur_key) & set(similar_key))) / float(len(cur_key))

            tem_dict[pubid] = similar
        similar_dict[cur_pubid] = tem_dict
    return similar_dict


def item_cf_by_collocate(group, key, df):
    '''
    假设用户（申请人），对于每篇专利高警度的评价即为优秀，专利之间技能关系的评价应该是可以体现专利相似度的。
    基于item_cf的推荐，我们可以将与原用户标记的高警专利相似度较高的专利推荐给当前用户，并按照相似度由高到低排序召回

    '''

    pass


# techWord,funcWord,techword&funcword,goodslist

def data_process(path):
    # load datab by path
    df = pd.read_csv(path, header=0, sep='\t')
    print(df.info())

    df.fillna(' ')
    keys = ['techWords', 'funcWords', 'fieldWords', 'goodsList']
    for key in keys:
        similar_dict = similar_process(key, df)
        json.dump(similar_dict, open(key + '_similar.json', 'w'))
        print(key, ' json is done')

    # print('data = ',df['applicantFirst'])

    # group_df = df.groupby('applicantFirst')

    count = 0


def similar_matrix_json(data, key):
    similar_dict = {}

    count = 0
    for pubid in data:
        count += 1

        if count % 100 is 0:
            print(count, ' matrix is done')
            break

        tem_dict = {}
        content = data[pubid]

        cur_key = content[key]

        cur_key = cur_key.split(',')
        if len(cur_key) == 0: continue

        for tem_pubid in data:
            if tem_pubid == pubid: continue

            similar_key = data[tem_pubid][key].split(',')

            similar = float(len(set(cur_key) & set(similar_key))) / float(len(cur_key))

            tem_dict[tem_pubid] = similar
        similar_dict[pubid] = tem_dict
    return similar_dict

import pandas as pd 

def data_process_dict(path):
    
    data = {}
    count = 0
    
    
    
    
    
    head  = ''
    
    with open(path, 'r') as f:
        for line in f:
            line = line.strip().split('$$$$')
            count += 1
            if count == 1: 
                head = line 
                #print(head)
                continue

            pubid = line[0]
            fieldWords = line[2]
            techWords = line[3]
            funcWords = line[4]
            goodsList = line[6]
            data[pubid] = {'fieldWords': fieldWords, 'techWords': techWords, 'funcWords': funcWords,
                           'goodsList': goodsList}

    keys = ['techWords', 'funcWords', 'fieldWords', 'goodsList']

    for k in keys:
        similar_dict = similar_matrix_json(data, k)
        print(len(similar_dict))

        json.dump(similar_dict, open(k + '_similar.json', 'w'))
        # break
        print(k, ' json is done')


path = '.\\..\\..\\data\\feautures.txt'
data_process_dict(path)



