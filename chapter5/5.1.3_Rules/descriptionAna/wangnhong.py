#coding=utf-8
'''
Created on 2019��1��15��

@author: zhaoh
'''

from mongoC import mongC
(conn,db,col) = mongC.mqpatMongo('fieldsIndivideBase')
o = open('test.txt','w')
print 'amount = ', col.count({'fieldsName':'北京工业大学王楠洪峰'})
count = 0 
ipcDict = {}
ipcCount = {}
for data in col.find({'fieldsName':'北京工业大学王楠洪峰'},{'title':1,'abst':1,'mainIpcCpc3':1}).batch_size(100):
    if 'mainIpcCpc3' not in data:
        continue
    tem = ''
    ipc = data['mainIpcCpc3']
    if 'title' in data:
        tem = tem + '。' +data['title'].encode('utf-8')
    if 'abst' in data:
        tem = tem + '。'  + data['abst'].encode('utf-8')
    #o.write(tem.replace('\n','') + '\n')
    if ipc in ipcDict:
        ipcDict[ipc].append(tem)
        ipcCount[ipc] += 1
    else:
        ipcDict[ipc] = [tem]
        ipcCount[ipc] = 1
    count += 1
    if count % 1000 is 0 :
        print count ,' done '
        #break
c = 0
for k,v in sorted(ipcCount.iteritems(),key=lambda k:k[1],reverse=True):
    c += 1
    tem = ipcDict[k]
    for i in tem :
        o.write(k.encode('utf-8') + ' ' + i + '\n')
    if c >5 :
        break

    
    
    