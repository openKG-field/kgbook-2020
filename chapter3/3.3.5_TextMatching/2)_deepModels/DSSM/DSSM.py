# -*- encoding: utf-8 -*-
"""
@File    : DSSM.py
@Time    : 2021/3/19 12:49
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""


from tensorflow.keras import optimizers
from tensorflow.keras import layers, Model
from tensorflow.keras import Input
import pandas as pd
import numpy as np
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

class DSSM():
    '''
    LSTM + DNN | LSTM + DNN, sigmoid结果 加和后 sigmoid输出
    '''
    input_dim = 0
    dnn_unit = 0


    def __init__(self,input_dim,dnn_unit):
        self.input_dim = input_dim
        self.dnn_unit =  dnn_unit

    def build(self,x_train,y_train,x_val,y_val,batch_size,lr,epochs):
        left_input = Input(shape=(self.input_dim,),dtype='int32',name='left')
        right_input = Input(shape=(self.input_dim,),dtype='int32',name='right')

        model_input = [left_input,right_input]

        #left_part
        #left_emb = Embedding(self.dnn_unit,self.input_dim)(left_input)
        #left_lstm = LSTM(self.input_dim,dropout=0.5)(left_input)
        #left_normal = BatchNormalization()(left_input)
        left_dense_1 = layers.Dense(self.input_dim, input_shape=(self.input_dim,), activation='relu')(left_input)
        left_normal_1 = layers.BatchNormalization()(left_dense_1)
        left_dense_2 = layers.Dense(self.dnn_unit, input_shape=(self.input_dim,), activation='relu')(left_normal_1)
        left_normal_2 = layers.BatchNormalization()(left_dense_2)
        left_dense_3 = layers.Dense(self.dnn_unit, input_shape=(self.input_dim,), activation='relu')(left_normal_2)
        left_normal_3 = layers.BatchNormalization()(left_dense_3)
        left_out = layers.Dense(1, activation='sigmoid')(left_normal_3)


        #dnn part
        #right_emb = Embedding(self.dnn_unit, self.input_dim)(right_input)
        #right_lstm = LSTM(self.input_dim,dropout=0.5)(right_input)
        #right_normal = BatchNormalization()(right_input)
        right_dense_1 = layers.Dense(self.input_dim, input_shape=(self.input_dim,), activation='relu')(right_input)
        right_normal_1 = layers.BatchNormalization()(right_dense_1)
        right_dense_2 = layers.Dense(self.dnn_unit, input_shape=(self.input_dim,), activation='relu')(right_normal_1)
        right_normal_2 = layers.BatchNormalization()(right_dense_2)
        right_dense_3 = layers.Dense(self.dnn_unit, input_shape=(self.input_dim,), activation='relu')(right_normal_2)
        right_normal_3 = layers.BatchNormalization()(right_dense_3)
        right_out = layers.Dense(1, activation='sigmoid')(right_normal_3)

        merge = left_out+right_out
        predict =  layers.Dense(1,activation='sigmoid',name='out')(merge)
        model = Model(model_input,predict)

        model.compile(optimizer=optimizers.Adam(learning_rate=lr),loss='binary_crossentropy', metrics='acc')

        model.fit(x_train, y_train, validation_data=(x_val, y_val), batch_size=batch_size, epochs=epochs)

        y_pred = model.predict(x_val)

        y_pred = [ 1 if i > 0.5 else 0 for i in y_pred]
        #print(y_pred)
        evalue(y_pred,x_val,y_val,'DSSM')
        model.save('dssm.h5')

def load_data(train_path,test_path):
    head = ['label']
    for i in range(1, 401):
        head.append('vec_' + str(i))
    train_data_pd = pd.read_csv(train_path, sep='\t', header=0, encoding='utf8')
    test_data_pd = pd.read_csv(test_path, sep='\t', header=0, encoding='utf8')

    x_train = train_data_pd[head[1:]]
    y_train = train_data_pd[head[0]]

    print(x_train)
    x_test = test_data_pd[head[1:]]
    y_test = test_data_pd[head[0]]


    dssm= DSSM(input_dim=len(head[1:]),dnn_unit=16)
    dssm.build({'left': x_train, 'right': x_train}, y_train, [x_test, x_test], y_test, batch_size=50,lr=0.01 ,epochs=30)
    #wd.build({'lr':x_train,'dnn':x_train},y_train,[x_test,x_test],y_test,batch_size=50,epochs=100)


train_path = 'dssm_train_data'
test_path  = 'dssm_test_data'

load_data(train_path,test_path)



