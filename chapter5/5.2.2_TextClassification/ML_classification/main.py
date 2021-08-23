# -*- encoding: utf-8 -*-
"""
@File    : main.py
@Time    : 2021/3/19 14:00
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""


from textcnn_tf2x import TextCNN
from textRNN_tf2x import TextRNN
from RCNN_tf2x import RCNN
import  pandas as pd
from sklearn.metrics import f1_score,accuracy_score,recall_score,log_loss,roc_curve,auc
import numpy as np
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



def textcnn_part(x_train,y_train,x_test,y_test):
    max_features = 5000
    maxlen = 10
    batch_size = 32
    embedding_dims = 50
    epochs = 1
    model = TextCNN(maxlen, max_features, embedding_dims)
    model.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=(x_test, y_test))

    print('Test...')
    y_pred = model.predict(x_test)
    y_pred = [ 1 if i > 0.5 else 0 for i in y_pred]

    evalue(y_pred,'',y_test,'textCNN')

def textrnn_part(x_train,y_train,x_test,y_test):
    max_features = 5000
    maxlen = 10
    batch_size = 32
    embedding_dims = 50
    epochs = 1
    model = TextRNN(maxlen, max_features, embedding_dims)
    model.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=(x_test, y_test))
    print('Test...')
    y_pred = model.predict(x_test)
    y_pred = [ 1 if i > 0.5 else 0 for i in y_pred]

    evalue(y_pred,'',y_test,'textRNN')

def RCNN_part(x_train,y_train,x_test,y_test):
    max_features = 5000
    maxlen = 10
    batch_size = 32
    embedding_dims = 50
    epochs = 1

    x_train= np.array(x_train)
    x_test = np.array(x_test)

    model = RCNN(maxlen, max_features, embedding_dims)
    model.compile('adam', 'binary_crossentropy', metrics=['accuracy'])

    x_train_left = np.hstack([np.expand_dims(x_train[:, 0], axis=1), x_train[:, 0:-1]])
    x_train_right = np.hstack([x_train[:, 1:], np.expand_dims(x_train[:, -1], axis=1)])
    x_test_left = np.hstack([np.expand_dims(x_test[:, 0], axis=1), x_test[:, 0:-1]])
    x_test_right = np.hstack([x_test[:, 1:], np.expand_dims(x_test[:, -1], axis=1)])
    print('Train...')
    model.fit([x_train, x_train_left, x_train_right], y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=([x_test, x_test_left, x_test_right], y_test))

    print('Test...')
    y_pred = model.predict([x_test,x_test_left,x_test_right])
    y_pred = [ 1 if i > 0.5 else 0 for i in y_pred]

    evalue(y_pred,'',y_test,'RCNN')

def load_data(train_path,test_path):
    head = 'type,tfidf_cnt,tfidf&tar_cnt,tech_cnt,tech&tar_cnt,agentList_cnt,problem_cnt,problem&tar_cnt,func_cnt,func&tar_cnt,applicantFirst,target'.split(',')

    train_data_pd = pd.read_csv(train_path, sep=',', header=0, encoding='utf8')
    test_data_pd = pd.read_csv(test_path, sep=',', header=0, encoding='utf8')

    x_train = train_data_pd[head[:-2]]
    y_train = train_data_pd[head[-1]]
    x_test = test_data_pd[head[:-2]]
    y_test = test_data_pd[head[-1]]

    textcnn_part(x_train,y_train,x_test,y_test)
    textrnn_part(x_train,y_train,x_test,y_test)
    RCNN_part(x_train,y_train, x_test, y_test)



train_path = './data/train_data.txt'
test_path =  './data/test_data.txt'

load_data(train_path,test_path)