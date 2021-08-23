#coding='utf8'

'''
run test for rcnn and textcnn
'''

class Config(object):
    def __init__(self, word_embedding_dimension=100, word_num=20000,
                 epoch=2, sentence_max_size=40, cuda=False,
                 label_num=2, learning_rate=0.01, batch_size=1,
                 out_channel=100):
        self.word_embedding_dimension = word_embedding_dimension     # 词向量的维度
        self.word_num = word_num
        self.epoch = epoch                                           # 遍历样本次数
        self.sentence_max_size = sentence_max_size                   # 句子长度
        self.label_num = label_num                                   # 分类标签个数
        self.lr = learning_rate
        self.batch_size = batch_size
        self.out_channel=out_channel
        self.cuda = cuda

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--lr', type=float, default=0.1)
parser.add_argument('--batch_size', type=int, default=16)
parser.add_argument('--epoch', type=int, default=20)
parser.add_argument('--gpu', type=int, default=0)
parser.add_argument('--out_channel', type=int, default=2)
parser.add_argument('--label_num', type=int, default=2)
parser.add_argument('--seed', type=int, default=1)
args = parser.parse_args()

from textCNN.textcnn import  TextCNN
import  pandas as pd
def load_data(train_path,test_path):
    head = 'type,tfidf_cnt,tfidf&tar_cnt,tech_cnt,tech&tar_cnt,agentList_cnt,problem_cnt,problem&tar_cnt,func_cnt,func&tar_cnt,applicantFirst,target'.split(',')

    train_data_pd = pd.read_csv(train_path, sep=',', header=0, encoding='utf8')
    test_data_pd = pd.read_csv(test_path, sep=',', header=0, encoding='utf8')

    x_train = train_data_pd[head[:-2]]
    y_train = train_data_pd[head[-1]]

    print(x_train)
    x_test = test_data_pd[head[:-2]]
    y_test = test_data_pd[head[-1]]

    config = Config(len(head[-2]))

    config = Config(sentence_max_size=50,
                    batch_size=args.batch_size,
                    word_num=11000,
                    label_num=args.label_num,
                    learning_rate=args.lr,
                    cuda=args.gpu,
                    epoch=args.epoch,
                    out_channel=args.out_channel)

    #rc= RCNN(config=config)
    #rc.model_build()
    #{'Q': x_train, 'C': x_train}, y_train, [x_test, x_test], y_test, batch_size=50, epochs=100
    
    tc= TextCNN(config=config)
    tc.model_build()
    
    
    #wd.build({'lr':x_train,'dnn':x_train},y_train,[x_test,x_test],y_test,batch_size=50,epochs=100)


train_path = '.\\..\\data\\train_data.txt'
test_path =  '.\\..\\data\\test_data.txt'

load_data(train_path,test_path)