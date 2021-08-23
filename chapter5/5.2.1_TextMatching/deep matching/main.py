# -*- encoding: utf-8 -*-
"""
@File    : main.py
@Time    : 2021/3/20 13:21
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""

from DSSM import evalue,DSSM
import pandas as pd


def load_data(train_path,test_path):
    head = 'type,tfidf_cnt,tfidf&tar_cnt,tech_cnt,tech&tar_cnt,agentList_cnt,problem_cnt,problem&tar_cnt,func_cnt,func&tar_cnt,applicantFirst,target'.split(',')

    train_data_pd = pd.read_csv(train_path, sep=',', header=0, encoding='utf8')
    test_data_pd = pd.read_csv(test_path, sep=',', header=0, encoding='utf8')

    x_train = train_data_pd[head[:-2]]
    y_train = train_data_pd[head[-1]]

    print(x_train)
    x_test = test_data_pd[head[:-2]]
    y_test = test_data_pd[head[-1]]


    dssm= DSSM(input_dim=len(head[:-2]),dnn_unit=16)
    dssm.build({'left': x_train, 'right': x_train}, y_train, [x_test, x_test], y_test, batch_size=50,lr=0.01 ,epochs=30)
    #wd.build({'lr':x_train,'dnn':x_train},y_train,[x_test,x_test],y_test,batch_size=50,epochs=100)


train_path = '.\\..\\..\\data\\train_data.txt'
test_path =  '.\\..\\..\\data\\test_data.txt'

load_data(train_path,test_path)