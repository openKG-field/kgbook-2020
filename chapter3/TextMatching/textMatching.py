#coding=utf-8


'''
Data:
mqpat database，
'''

'''
fieldsIndivideBase,利用LDA和LSI模型来做主题模型，细化一些内容。
通过领域名称和技术路径一二级名称，与主题模型进行比对），这样就可以做F1值的评价了。
'''


#import xmlrpclib
from pymongo import MongoClient
import codecs
import dis
#proxy = xmlrpclib.ServerProxy("http://103.105.201.54:30004")

import xmlrpc.client
proxy = xmlrpc.client.ServerProxy("http://103.105.201.54:30004")

def v4Mongo(tb):
    #host ='10.0.5.12'
    host = '103.105.201.54'
    port = 27017
    passwd = 'mq2019'
    dbName = 'mqpatv4'
    user = 'mqpatv4-rw'
    myTbNme = tb
    conn = MongoClient(host, port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[myTbNme]
    return (conn, db, collection)

def wordMongo(tb):
    #host ='10.0.5.12'
    host = '103.105.201.54'
    port = 27017
    passwd = 'mq2019'
    dbName = 'mqpat'
    user = 'mqpat-rw'
    myTbNme = tb
    conn = MongoClient(host, port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[myTbNme]
    return (conn, db, collection)

#(conn, db, col) = v4Mongo('fieldsIndivideBase')
(conn, db, col) = wordMongo('fieldsIndivideBase')

'''
LSI
http://zhikaizhang.cn/2016/05/31/自然语言处理之LSA/
TODO
# 生成word-document矩阵
X = np.zeros([len(keywords), currentDocId])
for i, k in enumerate(keywords):
    for d in dictionary[k]:
        X[i,d] += 1

# 奇异值分解
U,sigma,V = linalg.svd(X, full_matrices=True)
print("U:\n", U, "\n")
print("SIGMA:\n", sigma, "\n")
print("V:\n", V, "\n")

# 得到降维(降到targetDimension维)后单词与文档的坐标表示
targetDimension = 2
U2 = U[0:, 0:targetDimension]
V2 = V[0:targetDimension, 0:]
sigma2 = np.diag(sigma[0:targetDimension])
print(U2.shape, sigma2.shape, V2.shape)

'''


'''
TODO
在语义分析问题中，存在同义词和一词多义这两个严峻的问题，LSA可以很好的解决同义词问题，却无法妥善处理一词多义问题。
PLSA则可以同时解决同义词和一词多义两个问题。
http://zhikaizhang.cn/2016/06/17/自然语言处理之PLSA/
'''



'''
TODO
LDA由PLSA发展而来，PLSA由LSA发展而来，同样用于隐含语义分析，这里先给出两篇实现LSA和PLSA的文章链接。
我们知道，PLSA也定义了一个概率图模型，假设了数据的生成过程，但是不是一个完全的生成过程：没有给出先验。因此PLSA给出的是一个最大似然估计(ML)或者最大后验估计(MAP)。
LDA拓展了PLSA，定义了先验，因此LDA给出的是一个完整的贝叶斯估计。
那么接下来怎么办呢？我们回忆一下在PLSA中是怎么做的。
PLSA中的概率图模型由于没有先验，模型比LDA简单一些，认为文档决定topic，topic决定单词，写出了整个数据集的对数似然性，然后由于要求解的参数以求和的形式出现在了对数函数中，无法通过直接求导使用梯度下降或牛顿法来使得这个对数似然最大，因此使用了EM算法。
LDA同样可以使用EM算法求解参数，但需要在E步计算隐变量的后验概率时使用变分推断进行近似，一种更简单的方法是使用gibbs sampling。

'''

import numpy as np
import codecs
# 预处理(分词，去停用词，为每个word赋予一个编号，文档使用word编号的列表表示)
def preprocessing(filename):
    # 读取停止词文件
    file = codecs.open('stopwords.dic', 'r', 'utf-8')
    stopwords = [line.strip() for line in file]
    file.close()

    # 读数据集
    file = codecs.open('dataset.txt', 'r', 'utf-8')
    documents = [document.strip() for document in file]
    file.close()

    word2id = {}
    id2word = {}
    docs = []
    currentDocument = []
    currentWordId = 0

    for document in documents:
        # 分词
        segList = jieba.cut(document)
        for word in segList:
            word = word.lower().strip()
            # 单词长度大于1并且不包含数字并且不是停止词
            if len(word) > 1 and not re.search('[0-9]', word) and word not in stopwords:
                if word in word2id:
                    currentDocument.append(word2id[word])
                else:
                    currentDocument.append(currentWordId)
                    word2id[word] = currentWordId
                    id2word[currentWordId] = word
                    currentWordId += 1
        docs.append(currentDocument);
        currentDocument = []
    return docs, word2id, id2word


# 初始化，按照每个topic概率都相等的multinomial分布采样，等价于取随机数，并更新采样出的topic的相关计数
def randomInitialize():
    for d, doc in enumerate(docs):
        zCurrentDoc = []
        for w in doc:
            pz = np.divide(np.multiply(ndz[d, :], nzw[:, w]), nz)
            z = np.random.multinomial(1, pz / pz.sum()).argmax()
            zCurrentDoc.append(z)
            ndz[d, z] += 1
            nzw[z, w] += 1
            nz[z] += 1
        Z.append(zCurrentDoc)


# gibbs采样
def gibbsSampling():
    # 为每个文档中的每个单词重新采样topic
    for d, doc in enumerate(docs):
        for index, w in enumerate(doc):
            z = Z[d][index]
            # 将当前文档当前单词原topic相关计数减去1
            ndz[d, z] -= 1
            nzw[z, w] -= 1
            nz[z] -= 1
            # 重新计算当前文档当前单词属于每个topic的概率
            pz = np.divide(np.multiply(ndz[d, :], nzw[:, w]), nz)
            # 按照计算出的分布进行采样
            z = np.random.multinomial(1, pz / pz.sum()).argmax()
            Z[d][index] = z
            # 将当前文档当前单词新采样的topic相关计数加上1
            ndz[d, z] += 1
            nzw[z, w] += 1
            nz[z] += 1


alpha = 5
beta = 0.1
iterationNum = 50
K = 10
# 预处理
docs, word2id, id2word = preprocessing("data.txt")
Z = []
N = len(docs)
M = len(word2id)
# ndz[d,z]表示文档d中由topic z产生的单词计数加伪计数alpha
ndz = np.zeros([N, K]) + alpha
# nzw[z,w]表示topic z产生的单词w的计数加伪计数beta
nzw = np.zeros([K, M]) + beta
# nz[z]表示topic z产生的所有单词的总计数加伪计数
nz = np.zeros([K]) + M * beta
# 初始化
randomInitialize()
# gibbs sampling
for i in range(0, iterationNum):
    gibbsSampling()
# 产生每个topic的top10的词
topicwords = []
maxTopicWordsNum = 10
for z in range(0, K):
    ids = nzw[z, :].argsort()
    topicword = []
    for j in ids:
        topicword.insert(0, id2word[j])
    topicwords.append(topicword[0: min(10, len(topicword))])


'''
Conclusion:
textMatching is a method for classifying the meaning of different sentences.


'''