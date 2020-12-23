# -*- coding: utf-8 -*-

from numpy import *
import numpy as np
from Nbayes_lib import *


dataSet,listClasses = loadDataSet() #导入外部数据集
nb = NBayes()                       #类的实例化
nb.train_set(dataSet,listClasses)   #训练数据集
nb.map2vocab(dataSet[3])           #随机选择一个测试句，这里2表示文本中的第三句话，不是脏话，应输出0。
print (nb.predict(nb.testset))     #输出分类结果

"""
@File    : dt.py
@Time    : 2020/7/5 15:21
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""
#data
from  sklearn.model_selection import train_test_split
import  pandas as pd
import numpy as np
#model
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression,Perceptron
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
#evaluation
from sklearn.metrics import f1_score,accuracy_score,recall_score,log_loss,roc_curve,auc



def load_data(path):
    column_names = 'type,tfidf_cnt,tfidf&tar_cnt,tech_cnt,tech&tar_cnt,agentList_cnt,problem_cnt,problem&tar_cnt,func_cnt,func&tar_cnt,applicantFirst,target'.split(',')
    df = pd.read_csv(path,header=0,sep=',',encoding='utf8')
    df = df.replace(to_replace=-1,value=np.nan)
    X_train, X_test, y_train, y_test = train_test_split(df[column_names[:9]], df[column_names[11]],
                                                        test_size=0.25, random_state=33)  # 编号没有进入训练
    return X_train,X_test,y_train,y_test

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
    #get data for model
    path = 'D:\\NLPPractice\\book_method\\chapter3\\TextClassify\\3_1LR&SVM\\data\\model_data'
    x_train,x_test,y_train,y_test = load_data(path)

    #Perceptron
    perce = Perceptron()
    perce.fit(x_train,y_train)
    y_pred = perce.predict(x_test)
    evalue(y_pred, x_test, y_test, 'Perceptron_model')

    #nbay
    nbay = MultinomialNB()
    nbay.fit(x_train,y_train)
    y_pred = nbay.predict(x_test)
    evalue(y_pred,x_test,y_test,'nbay_model')
main()