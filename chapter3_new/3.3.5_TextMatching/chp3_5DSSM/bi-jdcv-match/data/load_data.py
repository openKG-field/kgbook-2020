# -*- coding:utf-8 -*-
'''
@author: zhanghaichao
@license: (C) Copyright liepin
@contact: zhanghaichao@liepin.com
@file: load_data.py
@time: 2020/4/1 14:07
@desc:
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import numpy as np
import tensorflow as tf
from gensim.models import KeyedVectors
from scipy.sparse import csr_matrix

logger = logging.getLogger(__name__)


class Word2Vec_bd(object):
    def __init__(self, vector_dir='./data/sgns.baidubaike.bigram-char'):
        self.vector_dir = vector_dir
        self.word_index = {"<UNK>": 0, "<PAD>": 1}
        self.index_word = {0: "<UNK>", 1: "<PAD>"}
        self.embedding_matrix = None

    def load_w2v(self,first_line = True,total_word=None,dim=None):
        logger.info('加载word2vec预训练向量...')
        if not first_line:
            self.embedding_matrix = np.zeros((total_word + 2, dim))
        i = 0
        with open(self.vector_dir, encoding='utf8', errors='ignore') as f:
            for line in f:
                if first_line:
                    first_line = False
                    values = line.rstrip().split(" ")
                    word_count = int(values[0])
                    dim = int(values[1])
                    self.embedding_matrix = np.zeros((word_count + 2, dim))
                    continue
                values = line.rstrip().split(" ")
                word = values[0]
                weight = np.asarray(values[1:], dtype='float32')
                if weight.shape[0] != dim:
                    continue
                self.word_index[word] = i + 2
                self.index_word[i + 2] = word
                self.embedding_matrix[i + 2] = weight
                i += 1
        logger.info('加载word2vec预训练向量完成')
        return self.word_index, self.index_word, self.embedding_matrix


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
        logger.info('加载word2vec预训练向量...')
        self.w2v_model = KeyedVectors.load_word2vec_format(fname=self.vector_dir, binary=True, encoding='utf8')
        word_list = [word for word, value in self.w2v_model.wv.vocab.items()]
        self.embedding_matrix = np.zeros((len(word_list) + 2, self.w2v_model.vector_size))
        for i, word in enumerate(word_list):
            self.word_index[word] = i + 2
            self.index_word[i + 2] = word
            self.embedding_matrix[i + 2] = self.w2v_model.wv[word]
        logger.info('加载word2vec预训练向量完成')
        return self.word_index, self.index_word, self.embedding_matrix


class DataProcessor(object):
    '''
    数据处理的基本类，讲分词后的数据转化为numpy形式，并做一些预处理
    '''

    def __init__(self, word_index, UNK=0, PAD=1):
        self.word_index = word_index
        self.UNK = UNK
        self.PAD = PAD

    def _read_txt(self, data_dir, delimiter='\t', is_have_label=True):
        labels = []
        cvs = []
        jds = []
        with open(data_dir, 'r', encoding='utf8') as f:
            for line in f.readlines():
                items = line.strip().split('\t')
                if len(items) != 3:
                    continue
                labels.append(int(items[0]))
                cvs.append([self.word_index.get(word, self.UNK) for word in items[1].split(' ')])
                jds.append([self.word_index.get(word, self.UNK) for word in items[2].split(' ')])

        return labels, cvs, jds

    def load_data(self, data_dir=None, padding_len=256):
        logger.info('加载数据集...')
        if data_dir:
            labels, cvs, jds = self._read_txt(data_dir)
            cvs = tf.keras.preprocessing.sequence.pad_sequences(cvs, maxlen=padding_len, truncating='post',padding='post',
                                                                value=self.PAD)
            jds = tf.keras.preprocessing.sequence.pad_sequences(jds, maxlen=padding_len, truncating='post',padding='post',
                                                                value=self.PAD)
            labels = np.asarray(labels, dtype=np.int32)
            cvs = np.asarray(cvs, dtype=np.int32)
            jds = np.asarray(jds, dtype=np.int32)

            logger.info('加载数据集完成')
            return labels, cvs, jds
        else:
            raise Exception('data dir is None!')