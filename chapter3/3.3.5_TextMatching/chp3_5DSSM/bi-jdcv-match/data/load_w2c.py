# -*- coding:utf-8 -*-
'''
@author: zhanghaichao
@license: (C) Copyright liepin
@contact: zhanghaichao@liepin.com
@file: load_w2c.py
@time: 2020/4/7 16:52
@desc:
'''


class Word2Vec(object):
    '''
    加载预训练好的word2vec
    '''

    def __init__(self, vector_dir):
        self.vector_dir = vector_dir
        self.word_index = {"<UNK>": 0, "<PAD>": 1}
        self.index_word = {0: "<UNK>", 1: "<PAD>"}
        self.embedding_matrix = None

    def load_embedding_matrix(self):
        with open(self.vector_dir, 'rb') as f:
            i=0
            for line in f.readlines():
                if i<10:
                    first_line=False
                    try:
                        stt=bytes.decode(line)
                    except:
                        continue
                    print(stt)
                    i+=1
                    continue


if __name__ == '__main__':
    w2v = Word2Vec(vector_dir='./word2vec_jd_cv_workexp_0401.bin')
    w2v.load_embedding_matrix()
