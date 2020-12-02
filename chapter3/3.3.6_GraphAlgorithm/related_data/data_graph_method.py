# -*- encoding: utf-8 -*-
"""
@File    : data_graph_method.py
@Time    : 2020/7/5 18:53
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""
def get_data_from_mongo():
    from mongoC import mongC

    (conn,db,col) = mongC.hvMongo('fieldsIndivideBase')

    o = open('graph_data','w',encoding='utf8')
    header = ['pubid','title','applicantFirst','citingList','citingCount','citedPubidList','citedAppidList','citedCount']
    o.write('\t'.join(header) + '\n')
    amount = col.count({'fieldsName':'人工智能'})
    count = 0

    exist_cnt = 0

    for data in col.find({'fieldsName':'人工智能'},{'_id':0,'pubid':1,'title':1,'applicantFirst':1,
                                                'citingList':1,'citedAppidList':1,
                                                'citedPubidList':1,'citingCount':1,'citedCount':1}).batch_size(100):
        cur = []

        for i in header:
            if i in data :
                try:
                    if type(data[i]) is list :
                        data[i] = '__'.join(data[i])
                    cur.append(str(data[i]))
                except:
                    print('error')
                finally:
                    exist_cnt += 1
            else:
                cur.append('-1')
        count += 1
        if count % 1000 is 0 :
            print(count, ' // ',amount)
        o.write('\t'.join(cur) + '\n')

def data_select():
    count = 0
    o= open('select_data','w',encoding='utf8')
    with open('graph_data','r',encoding='utf8') as f :
        for line in f :
            line = line.strip().split('\t')
            if line[3] == '-1' and line[4] == '-1' and line[5] == '-1' and line[6] == '-1' and line[7] == '-1':
                continue
            o.write('\t'.join(line) + '\n')
            count += 1
            if count % 10000 is 0 :
                print(count)

data_select()