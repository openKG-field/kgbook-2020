# -*- encoding: utf-8 -*-
"""
@File    : collect_data.py
@Time    : 2020/7/5 14:35
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""

from mongoC import mongC

(conn,db,col) = mongC.hvMongo('fieldsIndivideBase')

names = col.distinct('fieldsName')
def display():
    def count_field(name):

        amount = col.count({'fieldsName':name,'type':'cn'})
        if amount < 50000 : return 0
        print(name, ' = ', amount)

    for n in names :
        count_field(n)


#display()

def get_data(name):

    o =open('E:\\book_related_method\\data\\cluster_data.txt','w',encoding='utf8')
    datas = []
    head = {}
    count = 0
    for data in col.find({'fieldsName':name,},{'_id':0,'patentCitationList':0,'assigneeCurrentList':0,'agencyList':0,'legalTagList':0,'claimsIndList':0,'numberList':0,'description':0,'claimsList':0,'abst':0,'applicantList':0}).batch_size(100):
        for i in data :
            if i not in head :
                head[i] = 1
            if type(data[i]) is list :
                if len(data[i]) == 0 :
                    data[i] = '-1'
                else:
                    data[i] = '__'.join(data[i])

        count += 1
        if count % 100 is 0 :
            print(count , ' done ')

        if count > 80000 : break
        datas.append(data)

    #print('data = ',datas[0])

    header = []
    for i in head :
        header.append(i)
    o.write('\t'.join(header) +'\n')

    for i in datas :
        tem = []
        for h in header :
            cur = '-1'
            if h in i :
                cur = str(i[h])
            tem.append(cur)
        o.write('\t'.join(tem) + '\n')





name = '人工智能'
get_data(name)


(conn,db,col) = mongC.ipc('ipcInfo')

ipcData = open('ipcDesc.txt','w',encoding='utf8')
datas = []
head = []
for data in col.find({},{'_id':0}).batch_size(300):
    if 'ipcVal' not in data : continue
    if len(data['ipcVal']) >4 : continue


    for i in data :
        if i not in head : head.append(i)
        if type(i) is list :
            data[i] = '__'.join(data[i])

    datas.append(data)

ipcData.write('\t\t'.join(head) + '\n')

for d in datas :
    cur = []
    for i in head :
        tem = '-1'
        if i in d :
           tem = str(d[i])
        cur.append(tem)
    ipcData.write('\t\t'.join(cur) + '\n')
