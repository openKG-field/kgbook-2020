# -*- coding:utf-8 -*-
'''
@author: zhanghaichao
@license: (C) Copyright liepin
@contact: zhanghaichao@liepin.com
@file: jdcv_lstm.py
@time: 2020/4/1 9:58
@desc:
'''

import logging
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import layers, Model, Sequential
from tensorflow.keras import losses

logger = logging.getLogger(__name__)


class JDCV_LSTM(Model):
    '''
    Use LSTM to build JDCV matching model. The model have two networks, one is jd_seq, other is cv_seq.
    Then, merge two networks by cosine index.
    '''

    def __init__(self,
                 lstm_units,
                 first_dense_units,
                 sec_dense_units,
                 embedding_matrix,
                 embedding_dim,
                 max_seq_len):
        super(JDCV_LSTM, self).__init__()
        logger.info('模型构建...')
        self.jd_seq = Sequential([
            layers.Embedding(input_shape=(max_seq_len,),
                             input_dim=len(embedding_matrix),
                             output_dim=embedding_dim,
                             weights=[embedding_matrix],
                             input_length=max_seq_len,
                             trainable=False),
            # layers.Bidirectional(layers.LSTM(units=lstm_units, dropout=0.5, return_sequences=True)),
            layers.Bidirectional(layers.LSTM(units=lstm_units, dropout=0.5)),
            layers.Dense(first_dense_units, activation='relu'),
            layers.BatchNormalization(),
            layers.Dense(sec_dense_units, activation='relu'),
            layers.BatchNormalization()
        ])
        self.cv_seq = Sequential([
            layers.Embedding(input_shape=(max_seq_len,),
                             input_dim=len(embedding_matrix),
                             output_dim=embedding_dim,
                             weights=[embedding_matrix],
                             input_length=max_seq_len,
                             trainable=False),
            # layers.Bidirectional(layers.LSTM(units=lstm_units, dropout=0.5, return_sequences=True)),
            layers.Bidirectional(layers.LSTM(units=lstm_units, dropout=0.5)),
            layers.Dense(first_dense_units, activation='relu'),
            layers.BatchNormalization(),
            layers.Dense(sec_dense_units, activation='relu'),
            layers.BatchNormalization()
        ])
        logger.info('模型构建完成')

    def jdcv_cosine(self, x, y):
        '''
        实现余弦相似度jdcv_cosine
        :param x:
        :param y:
        :param axis:
        :return:
        '''
        x_norm = tf.sqrt(tf.reduce_sum(tf.square(x)))
        y_norm = tf.sqrt(tf.reduce_sum(tf.square(y)))
        x_y = tf.reduce_sum(tf.multiply(x_norm, y_norm))
        cosine = tf.divide(x_y, tf.multiply(x_norm, y_norm))
        return cosine

    def call(self, inputs, training=None, mask=None):
        '''
        实现JDCV_LSTM的前向传播
        :param inputs: jd is inputs[0], cv is inputs[1]
        :param training:
        :param mask:
        :return:
        '''
        jd = inputs[0]
        cv = inputs[1]
        jd = self.jd_seq(jd)
        cv = self.cv_seq(cv)
        cosine = losses.cosine_similarity(cv, jd, axis=-1)
        out = tf.sigmoid(cosine)
        return out


class Evaluate(object):
    def __init__(self):
        pass

    def metrics_plot(self, history, metric, save_path):
        train_metrics = history.history[metric]
        val_metrics = history.history['val_' + metric]
        epochs = range(1, len(train_metrics) + 1)
        plt.plot(epochs, train_metrics, 'bo--')
        plt.plot(epochs, val_metrics, 'ro--')
        plt.title('Train and Validation ' + metric)
        plt.xlabel('Epochs')
        plt.ylabel(metric)
        plt.legend(['train_' + metric, 'val_' + metric])
        plt.savefig(save_path)


if __name__ == '__main__':
    pass
