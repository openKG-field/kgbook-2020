#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : books_method
# @File : xgb.py
# @Time    : 2020/7/6 15:20
# @Author  : Zhaohy

import  xgboost as xgb
import  config
import pandas as pd
from sklearn.metrics import  accuracy_score


class xgb_model():
    params = {}

    def __init__(self,params):
        self.params= dict(params.items())

    def load_data(self,train_data_path,test_data_path,target,sep,ignore_list=None):
        print(train_data_path)
        print('sep = ',sep)
        train_data = pd.read_csv(train_data_path,header=0,sep=sep,encoding='utf8')
        test_data = pd.read_csv(test_data_path,header=0,sep=sep,encoding='utf8')
        y_train = train_data[target]
        y_test = test_data[target]

        drop_list = [target]

        if ignore_list != None :
            drop_list = drop_list + ignore_list

        x_train = train_data.drop(columns=drop_list)
        x_test = test_data.drop(columns=drop_list)

        return x_train,y_train,x_test,y_test



    def fit(self,x_train,y_train,x_test,y_test,rounds):

        data_train = xgb.DMatrix(x_train,y_train)

        print(self.params)

        model = xgb.train(params=self.params,dtrain=data_train,num_boost_round=rounds)
        data_test = xgb.DMatrix(x_test, y_test)

        pred = model.predict(data_test)


        print(pred)
        evalue(pred, x_test, y_test, 'xgb')
        acc = accuracy_score(y_test,pred)

        print('xgboost ', acc)

from sklearn.metrics import f1_score,accuracy_score,recall_score,log_loss,roc_curve,auc

def evalue(y_pred,x_test,y_test,label):
    '''
    :param y_pred:
    :param x_test:
    :param y_test:
    :param label:
    f1_score,accuracy_score,recall_score,log_loss,auc
    :return:
    '''

    f1 = f1_score(y_test,y_pred)
    acc = accuracy_score(y_test,y_pred)
    recall = recall_score(y_test,y_pred)
    log = log_loss(y_test,y_pred)
    fpr,tpr,threshold = roc_curve(y_test,y_pred)
    auc_value = auc(fpr,tpr)

    display = '''
        evluation of {label} is :
        f1_score = {f1}
        accuracy = {acc}
        recall = {recall}
        log_loss = {log}
        auc = {auc_value}
    '''
    print(display.format(label=label,f1=f1,acc=acc,recall=recall,log=log,auc_value=auc_value))

def main():
    params = config.params

    train_data_path = './../train_data.txt'
    test_data_path = './../test_data.txt'
    target = 'target'
    ignore_list = ['applicantFirst']
    sep = ','
    xg = xgb_model(params=params)
    #train_data_path,test_data_path,target,sep,ignore_list=None)
    x_train,y_train,x_test,y_test = xg.load_data(train_data_path,test_data_path,target,sep,ignore_list)

    print(x_train.info())

    xg.fit(x_train,y_train,x_test,y_test,rounds=500)


import time
a = time.time()
main()
b = time.time()

print( (b-a)/60 , (b-a%60) )