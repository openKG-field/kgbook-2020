#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@File     : FM.py
@Time     : 2021/3/25 19:49
@Author   : zhaohongyu
@Email    : zhaohongyu2401@yeah.net
@Software : PyCharm
"""


import numpy as np
import pandas as pd
import tensorflow as tf
import keras
import os

from tensorflow import Variable
import matplotlib.pyplot as plt

from keras.layers import Layer,Dense,Dropout,Input
from keras import Model,activations
from keras.optimizers import Adam
from keras import backend as K
from keras.layers import Layer

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


os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICES'] = "0"
class FM(Layer):
    def __init__(self, output_dim, latent=10,  activation='relu', **kwargs):
        self.latent = latent
        self.output_dim = output_dim
        self.activation = activations.get(activation)
        super(FM, self).__init__(**kwargs)

    def build(self, input_shape):
        self.b = self.add_weight(name='W0',
                                  shape=(self.output_dim,),
                                  trainable=True,
                                 initializer='zeros')
        self.w = self.add_weight(name='W',
                                 shape=(input_shape[1], self.output_dim),
                                 trainable=True,
                                 initializer='random_uniform')
        self.v= self.add_weight(name='V',
                                 shape=(input_shape[1], self.latent),
                                 trainable=True,
                                initializer='random_uniform')
        super(FM, self).build(input_shape)



    def call(self, inputs, **kwargs):
        x = inputs
        x_square = K.square(x)

        xv = K.square(K.dot(x, self.v))
        xw = K.dot(x, self.w)

        p = 0.5*K.sum(xv-K.dot(x_square, K.square(self.v)), 1)

        rp = K.repeat_elements(K.reshape(p, (-1, 1)), self.output_dim, axis=-1)

        f = xw + rp + self.b

        output = K.reshape(f, (-1, self.output_dim))

        return output

    def compute_output_shape(self, input_shape):
        assert input_shape and len(input_shape)==2
        return input_shape[0],self.output_dim

    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'latent': self.latent,
            'output_dim': self.output_dim,
            'activation': self.activation,
        })
        return config


import pandas as pd


def fm_model(data,target,vec_size,fea_size,x_test,y_test):
    K.clear_session()
    print(target)

    #    def __init__(self, output_dim, latent=10,  activation='relu', **kwargs):
    inputs = Input(shape=(fea_size,))
    out = FM(vec_size,name='fm')(inputs)
    #out = Dense(15, activation='sigmoid')(out)
    out = Dense(1, activation='sigmoid')(out)

    model=Model(inputs=inputs, outputs=out)
    model.compile(loss='mse',
                  optimizer='sgd',
                  metrics=['acc'])
    model.summary()


    h=model.fit(data, target, batch_size=10, epochs=2, validation_split=0.2)

    y_pred = model.predict(x_test)

    print(y_pred)
    y_pred = [1 if i > 0.5 else 0 for i in y_pred]
    # print(y_pred)
    evalue(y_pred, x_test, y_test, 'FM')
    model.save('FM.h5')

    fm_layer= model.get_layer(name='fm')



    return model,fm_layer


def run(train_path,test_path):
    head = 'type,tfidf_cnt,tfidf&tar_cnt,tech_cnt,tech&tar_cnt,agentList_cnt,problem_cnt,problem&tar_cnt,func_cnt,func&tar_cnt,applicantFirst,target'.split(
        ',')

    train_data_pd = pd.read_csv(train_path, sep=',', header=0, encoding='utf8')
    test_data_pd = pd.read_csv(test_path, sep=',', header=0, encoding='utf8')

    x_train = train_data_pd[head[:-2]]
    y_train = train_data_pd[head[-1]]

    print(x_train)
    x_test = test_data_pd[head[:-2]]
    y_test = test_data_pd[head[-1]]



    vec_size= 8
    model,fm_laryer= fm_model(x_train,y_train,vec_size,len(head[:-2]),x_test,y_test)

    weights = fm_laryer.weights



    #model.save_weights('fm_weights')

    # plt.plot(h.history['acc'],label='acc')
    # plt.plot(h.history['val_acc'],label='val_acc')
    # plt.xlabel('epoch')
    # plt.ylabel('acc')
    # plt.show()
train_path = '.\\..\\..\\..\\data\\train_data.txt'
test_path =  '.\\..\\..\\..\\data\\test_data.txt'

run(train_path,test_path)

