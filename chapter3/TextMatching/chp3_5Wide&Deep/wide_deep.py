#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : books_method
# @File : wide_deep.py
# @Time    : 2020/8/13 10:21
# @Author  : Zhaohy

from keras.models import Sequential,Model
from keras.layers import Embedding,Dense,Input,LSTM,SimpleRNN,Bidirectional,BatchNormalization
import pandas as pd
import numpy as np

class wide_deep():
    '''
    LR + DNN, sigmoid结果 加和后 sigmoid输出
    '''
    input_dim = 0
    dnn_unit = 0


    def __init__(self,input_dim,dnn_unit):
        self.input_dim = input_dim
        self.dnn_unit =  dnn_unit

    def build(self,x_train,y_train,x_val,y_val,batch_size,epochs):
        lr_input = Input(shape=(self.input_dim,),dtype='int32',name='lr')
        dnn_input = Input(shape=(self.input_dim,),dtype='int32',name='dnn')

        model_input = [lr_input,dnn_input]

        #lr_part
        lr_dense = Dense(self.input_dim,input_shape=(self.input_dim,),activation='relu')(lr_input)
        lr_out = Dense(1,activation='sigmoid')(lr_dense)

        #dnn part
        dnn_dense_1 = Dense(self.dnn_unit,input_shape=(self.input_dim,),activation='relu')(dnn_input)
        dnn_normal_1 = BatchNormalization()(dnn_dense_1)
        dnn_dense_2 = Dense(self.dnn_unit, input_shape=(self.input_dim,), activation='relu')(dnn_normal_1)
        dnn_normal_2 = BatchNormalization()(dnn_dense_2)
        dnn_dense_3 = Dense(self.dnn_unit, input_shape=(self.input_dim,), activation='relu')(dnn_normal_2)
        dnn_normal_3 = BatchNormalization()(dnn_dense_3)
        dnn_out = Dense(1,activation='sigmoid')(dnn_normal_3)

        merge = dnn_out+lr_out
        predict =  Dense(1,activation='sigmoid',name='out')(merge)
        model = Model(model_input,predict)

        model.compile(loss='binary_crossentropy', metrics='acc')

        model.fit(x_train, y_train, validation_data=(x_val, y_val), batch_size=batch_size, epochs=epochs)

        model.save('wide_deep.h5')

def load_data(train_path,test_path):
    head = 'type,tfidf_cnt,tfidf&tar_cnt,tech_cnt,tech&tar_cnt,agentList_cnt,problem_cnt,problem&tar_cnt,func_cnt,func&tar_cnt,applicantFirst,target'.split(
        ',')

    train_data_pd = pd.read_csv(train_path, sep=',', header=0, encoding='utf8')
    test_data_pd = pd.read_csv(test_path, sep=',', header=0, encoding='utf8')

    x_train = train_data_pd[head[:-2]]
    y_train = train_data_pd[head[-1]]

    x_test = test_data_pd[head[:-2]]
    y_test = test_data_pd[head[-1]]


    wd= wide_deep(input_dim=len(head[:-2]),dnn_unit=16)
    wd.build({'lr':x_train,'dnn':x_train},y_train,[x_test,y_test],y_test,batch_size=50,epochs=100)


train_path = 'C:\\Users\\zhaohongyu\\PycharmProjects\\books_method\\FM_FFM_DeepFM\\data\\format_train.txt'
test_path =  'C:\\Users\\zhaohongyu\\PycharmProjects\\books_method\\FM_FFM_DeepFM\\data\\format_test.txt'

load_data(train_path,test_path)



