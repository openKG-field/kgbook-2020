# -*- encoding: utf-8 -*-
"""
@File    : attention.py
@Time    : 2021/3/19 14:17
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""
import keras
from keras_self_attention import SeqSelfAttention
from keras.layers import Layer,Dense,Dropout,Input,Embedding
from keras import Model,activations
from keras.optimizers import Adam
from keras import backend as K
from keras.layers import Layer
from tensorflow.keras import optimizers
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

class att_model():
    input_dim = 0
    dnn_unit = 0

    def __init__(self, input_dim, dnn_unit):
        self.input_dim = input_dim
        self.dnn_unit = dnn_unit

    def build(self, x_train, y_train, x_val, y_val, batch_size, epochs):

        att_input =Input(shape=(self.input_dim,),dtype='int32',name='input')

        att_emd = Embedding(input_dim=self.input_dim,output_dim=256,mask_zero=True)(att_input)
        att = SeqSelfAttention(attention_activation='sigmoid')(att_emd)
        att_out = Dense(1, activation='sigmoid')(att)

        model = Model(att_input,att_out)
        model.compile(optimizer=optimizers.Adam(learning_rate=0.01), loss='binary_crossentropy', metrics='acc')

        model.fit(x_train, y_train, validation_data=(x_val, y_val), batch_size=batch_size, epochs=epochs)
        y_pred = model.predict(x_val)

        y_pred = [1 if i > 0.5 else 0 for i in y_pred]
        # print(y_pred)
        evalue(y_pred, x_val, y_val, 'attention')
        model.save('attention.h5')

import pandas as pd
def load_data(train_path, test_path):
    head = 'type,tfidf_cnt,tfidf&tar_cnt,tech_cnt,tech&tar_cnt,agentList_cnt,problem_cnt,problem&tar_cnt,func_cnt,func&tar_cnt,applicantFirst,target'.split(
        ',')

    train_data_pd = pd.read_csv(train_path, sep=',', header=0, encoding='utf8')
    test_data_pd = pd.read_csv(test_path, sep=',', header=0, encoding='utf8')

    x_train = train_data_pd[head[:-2]]
    y_train = train_data_pd[head[-1]]

    print(x_train)
    x_test = test_data_pd[head[:-2]]
    y_test = test_data_pd[head[-1]]
    return x_train,y_train,x_test,y_test

def main():
    train_path = '.\\..\\..\\data\\train_data.txt'
    test_path =  '.\\..\\..\\data\\test_data.txt'

    x_train,y_train,x_test,y_test = load_data(train_path,test_path)
    att = att_model(len(x_train),1)
    att.build(x_train,y_train,x_test,y_test,20,epochs=100)

if __name__ == '__main__':
    main()