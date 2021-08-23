#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@File     : train_test_data.py
@Time     : 2021/3/25 16:07
@Author   : zhaohongyu
@Email    : zhaohongyu2401@yeah.net
@Software : PyCharm
"""


path = 'data_for_dssm.txt'

train_path = 'dssm_train_data'
test_path = 'dssm_test_data'

train_out = open(train_path,'w',encoding='utf8')
test_out = open(test_path,'w',encoding='utf8')
head = ['label']

for i in range(1,401):
    head.append('vec_'+str(i))

train_out.write('\t'.join(head)+'\n')
test_out.write('\t'.join(head)+'\n')

#ana = {'1':0,'0':0}
#{'1': 876, '0': 2505}
#train 500:1 1500:0

train_pos= 500
train_neg = 1500
with open(path,'r',encoding='utf8') as f :
    for line in f :
        line = line.strip().split('\t')
        y = line[0]
        tem = '\t'.join(line)+'\n'
        if y =='1' :
            if train_pos >0 :
                train_out.write(tem)
                train_pos -= 1
            else:
                test_out.write(tem)
        else:
            if train_neg >0 :
                train_out.write(tem)
                train_neg -= 1
            else:
                test_out.write(tem)

