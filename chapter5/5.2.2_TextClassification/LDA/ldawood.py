#encoding=utf-8
import codecs
from gensim import corpora
from gensim.models import LdaModel
import sys
from pymongo import MongoClient



reload(sys)
sys.setdefaultencoding("utf-8")

dbName = 'test'
user = 'lyj-rw'
passwd = '123456'
host = '172.10.30.41'  
port = 27017

def temMongo():
    global dbName,user,passwd,host,port
    tbName = 'temDataBean'
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[tbName]
    return (conn,db,collection) 

def trainLDAModel(k,savePath,readPath,userid):

    train=[]
    tem = []
    pubid = []
#==============read data by file ===========================

#     fr = codecs.open(readPath, 'r',encoding='utf8')
#     stopwords = ['#$','#*','#@','#!','#&','实用新型']
# 
#     for line in fr.readlines():
#         head = line[:2]
#         line = line[2:]
#         if head == '#^':
#             #line = line.split()
#             pubid.append(line)    
#         if head == '#*':
#             tem = line.split()
#         if head == '#!':
#             for i in line.split():
#                 tem.append(i)
#             train.append([w for w in tem if w not in stopwords])
# #             print train
# #             break
#     print len(train)
#===============read data from database=======================
    (conn,db,temCollection) = temMongo()
    for dataContent in temCollection.find({'userid':userid}):
        if dataContent.has_key('pubid') and dataContent.has_key('title_v1') and dataContent.has_key('abst_v1') and dataContent.has_key('claims_v1'):
            if dataContent['country'] != 'CN':
                continue
            pubid.append(dataContent['pubid'])
            tem = dataContent['title_v1'] +'  ' + dataContent['abst_v1']
            train.append(tem.split())
#             print train
#             break

#===============train data and save model======================v
    dictionary = corpora.Dictionary(train)
    corpus = [dictionary.doc2bow(text) for text in train]
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=k)
    lda.save(savePath)
    
def begin():
    readPath = 'smallTest.txt'
    savePath = 'testWood.model'
    userid = 'wangyuxiu'
    k= 5
    trainLDAModel(k, savePath, readPath,userid)

begin()
# topic_list = lda.print_topics(20)
# print type(lda.print_topics(20))
# print len(lda.print_topics(20))
# 
# #index=0
# #print chardet.detect(topic_list[1])
# for topic in topic_list:
# 
#     #unicode_str = unicode(topic, encoding='utf-8')
#     #print unicode_str.encode('utf-8')
# 
#     #print topic
#     for i in topic:
#         print i, ''.decode('utf-8')
#     print()
# 
# print '给定一个新文档，输出其主题分布'
# print ' '.join(train[1])
# # test_doc = list(new_doc) #新文档进行分词
# test_doc = train[1]  # 查看训练集中第三个样本的主题分布
# doc_bow = dictionary.doc2bow(test_doc)  # 文档转换成bow
# doc_lda = lda[doc_bow]  # 得到新文档的主题分布
# # 输出新文档的主题分布
# print doc_lda
# for topic in doc_lda:
#     print "%s\t%f\n" % (lda.print_topic(topic[0]), topic[1])