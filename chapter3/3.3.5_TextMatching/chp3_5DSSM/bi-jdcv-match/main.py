# -*- coding:utf-8 -*-
'''
@author: zhanghaichao
@license: (C) Copyright liepin
@contact: zhanghaichao@liepin.com
@file: main.py
@time: 2020/4/1 16:37
@desc:
'''
import datetime
import tensorflow as tf
from tensorflow.keras import optimizers, losses
from tensorboard import notebook
from data.load_data import Word2Vec, Word2Vec_bd
from data.load_data import DataProcessor
from models.jdcv_lstm import JDCV_LSTM, Evaluate
from log import log

logger = log('./log.log')

if __name__ == '__main__':

    # 加载word2vec预训练模型
    #     word2vec = Word2Vec_bd(vector_dir='./data/sgns.baidubaike.bigram-char')
    word2vec = Word2Vec_bd(vector_dir='./data/jd_cv_workexp_0407_vec.txt')
    word_index, index_word, embedding_matrix = word2vec.load_w2v(first_line=False, total_word=227546, dim=100)

    #     # 加载glove预训练模型
    #     glove = GloVe()
    #     word_index, index_word, word_vector, embedding_matrix = glove.load_glove()

    # 加载数据
    padding_len = 256
    data_processor = DataProcessor(word_index=word_index)
    y_train, cvs_train, jds_train = data_processor.load_data(
        '/data1/jupyter/zhanghaichao/jd-cv-text-matching/jd-cv-data/train_data_seg.txt', padding_len=padding_len)
    x_train = [cvs_train, jds_train]
    y_dev, cvs_dev, jds_dev = data_processor.load_data(
        '/data1/jupyter/zhanghaichao/jd-cv-text-matching/jd-cv-data/dev_data_seg.txt', padding_len=padding_len)
    x_dev = [cvs_dev, jds_dev]

    # 模型训练
    logger.info('模型训练...')
    logdir = "./data/keras_model/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(logdir, histogram_freq=1)
    batchsz = 64
    epochs = 100
    lr = 1e-4
    lstm_units = 64
    first_dense_units = 64
    sec_dense_units = 32
    embedding_dim = 100
    model = JDCV_LSTM(lstm_units=lstm_units,
                      first_dense_units=first_dense_units,
                      sec_dense_units=sec_dense_units,
                      embedding_matrix=embedding_matrix,
                      embedding_dim=embedding_dim,
                      max_seq_len=padding_len)

    model.compile(optimizer=optimizers.Adam(learning_rate=lr),
                  loss=losses.BinaryCrossentropy(),
                  metrics=['acc'])
    history = model.fit(x=x_train,
                        y=y_train,
                        batch_size=batchsz,
                        epochs=epochs,
                        validation_data=(x_dev, y_dev), callbacks=[tensorboard_callback])
    model.summary()
    logger.info('模型训练完成')

    # 评估一下模型效果
    logger.info('模型评估')
    evaluate = Evaluate()
    evaluate.metrics_plot(history=history, metric='acc', save_path='./acc_own_w2v.png')
    #     notebook.list()
    #     notebook.start("--logdir ./data/keras_model")

    # 查看一下预测结果
    logger.info('查看一下预测的结果')
    x_valid = [cvs_dev[:2], jds_dev[:2]]
    y_valid = y_dev[:2]
    y_predict = model.predict_on_batch(x=x_valid)
    for cv, jd, y_, y in zip(cvs_dev[:2], jds_dev[:2], y_predict, y_valid):
        logger.info('cv:' + "".join([index_word.get(index, '<UNK>') for index in cv]))
        logger.info('jd:' + "".join([index_word.get(index, '<UNK>') for index in jd]))
        logger.info('predict label:{}'.format(y_))
        logger.info('real label:{}'.format(y))
