#coding=utf8
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

import pandas as pd 
import math
break_flag ='$$$$'
keys = ['pubid','fieldsName','fieldWords','techWords','funcWords','tfidf_v1','goodsList','warnlevelRe','indLen','claimsIndCount','feature','mainIpc3']
##      0        1            2            3            4            5        6            7            8            9            10       11
clusters = {}

import codecs
def load_data():
    
    train = []
    test = []
    
    path  = r'./data/noman_feautures.txt'
    
    h1_count = 0 
    h2_count = 0 
    h2b_count = 0 
    g1_count = 0
    h2j_count = 0
    h1f_count = 0
    h1r_count =0
    
    
    f1_count = 0
    f2_count = 0 
    
    
    count = 0 
    f = codecs.open(path,'r',encoding='utf-8')
    for line in f:
        print ('true')
        count += 1 
        if count == 1 : continue
        line = line.strip().split(break_flag)
        c = line[-1] 
        if c  in clusters :
            clusters[c] += 1 
        else:
            clusters[c] =  1
        
        if c =='H01H' and h1_count < 1000:
            test.append(line)
            h1_count += 1 
        elif c =='H02H' and h2_count<300 :
            test.append(line)
            h2_count += 1
        elif c== 'H02B' and h2b_count < 80:
            test.append(line)
            h2b_count += 1
        elif c == 'G01R' and g1_count < 80 :
            test.append(line)
            g1_count += 1
        elif c == 'H02J' and h2j_count < 30 :
            test.append(line)
            h2j_count += 1  
        elif c == 'H01F' and h1f_count < 25 :
            test.append(line)
            h1f_count += 1 
        elif c == 'H01R' and h1r_count < 14 :
            test.append(line)
            h1r_count += 1
        elif c == 'H01R' or c == 'H01F' or c == 'H02J' or c == 'GO1R' or c == 'H02B' or c == 'H01H' or c == 'H01H' :
            train.append(line)
    
    
    for k,v in sorted(clusters.items(),key=lambda k:k[1],reverse=True):
        print(k,v)
    
    return train,test
            



def distance(block,a,b):
    '''
    tar : 训练目标
    a:待分组数据
    b：现有分组数据
    '''
    
    tmp_a = []
    tmp_b = []
    
    for i in range(len(a)):
        if i in block:
            continue
        tmp_a.append(a[i])
        tmp_b.append(b[i])
        
    a = tmp_a
    b = tmp_b
    
    # 特征属性数据 ： 相同内容/全部内容  平方
    # 数值数据 ：  (a - b) 平方
    
    cal = 0 
    for i in range(len(a)):
        tem_a = a[i]
        tem_b = b[i]
        if tem_a =='None_Value' or tem_b =='None_value' :
            continue
        elif tem_a.isdigit() and tem_b.isdigit() :
            cal = cal +  math.pow((int(tem_a) - int(tem_b)), 2)
        else:
            tem_a = tem_a.split(',')
            tem_b = tem_b.split(',')
            
            v = float(len(set(a)&set(b)))/float(len(set(a)))
            cal = cal + math.pow(v, 2)
    
    return math.sqrt(float(cal))  
    
    
def KNN(train,test,tar):
    import numpy as np
    block = [0,1,7,11]
    
    result = {}
    
    
    for i in train :
        
        belong = {}
        for j in test :
            
            dis = distance(block, i, j)
            t = j[tar]
            if t in belong :
                belong[t].append(dis)
            else:
                belong[t] = [dis]
        
        compare = {}
        for t in belong :
            compare[t] = np.mean(np.array(belong[t]))
        
        
        for k,v in sorted(compare.items(),key=lambda k:k[1],reverse=True):
            result[i[0]] = {'real':i[tar],'predict':k}
            break
    #print(result)
    return result

def evaluation(result):
    
    match =0 
    # if len(result) >0:
    #      break
    for i in result :
        real = result[i]['real']
        pred = result[i]['predict']
        if real == pred :
            match += 1

    #if len(result) == 0:


    acc = float(match)/float(len(result))
    for i in result :
        print (i, result[i])
    print('arrcuary = ',acc)
     


if __name__ == '__main__':
    train,test = load_data()
    tar = -1 #mainIpc
    print(len(train))
    
    result = KNN(train, test, tar)
    # if result is None:
    #     continue
    evaluation(result)
    
    