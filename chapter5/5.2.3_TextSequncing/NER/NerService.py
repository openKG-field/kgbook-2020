# -*- encoding: utf-8 -*-
"""
@File    : NerService.py.py
@Time    : 2021/3/19 14:00
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""
# 通过单例模式使用ner,减少加载次数

import pickle
import tensorflow as tf
import os
import sys

from .model import Model
from .utils import load_config, get_logger
from .data_utils import create_input, input_from_line
#from .utils import create_model



class NerService(object):

    __instance=None
    def __init__(self):
        pass

    def __new__(cls,*args,**kwd):
        if not cls.__instance:
            cls.__instance=object.__new__(cls,*args,**kwd)
            dir_path = os.path.dirname(__file__)+'/'
            flags = tf.app.flags
            flags.DEFINE_string("config_file", dir_path + "config_file", "File for config")
            flags.DEFINE_string("ckpt_path", dir_path + "ckpt", "Path to save model")
            flags.DEFINE_string("summary_path", dir_path + "summary", "Path to store summaries")
            flags.DEFINE_string("log_file", dir_path + "evaluate.log", "File for log")
            flags.DEFINE_string("map_file", dir_path + "maps.pkl", "file for maps")
            FLAGS = tf.app.flags.FLAGS

            with open(FLAGS.map_file, "rb") as f:
                cls.char_to_id, cls.id_to_char, cls.tag_to_id, cls.id_to_tag = pickle.load(f)
            config = load_config(FLAGS.config_file)
            logger = get_logger(FLAGS.log_file)
            # limit GPU memory
            tf_config = tf.ConfigProto()
            tf_config.gpu_options.allow_growth = True

            cls.sess = tf.Session(config=tf_config)
            cls.model = cls.create_model(cls,cls.sess, Model, FLAGS.ckpt_path, config, logger)

        return cls.__instance

    def create_model(self,session, Model_class, path, config, logger):
        # create model, reuse parameters if exists
        model = Model_class(config)
        ckpt = tf.train.get_checkpoint_state(path)

        assert ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_path), "missing model"

        logger.info("Reading model parameters from %s" % ckpt.model_checkpoint_path)
        model.saver.restore(session, ckpt.model_checkpoint_path)
        return model


    def evaluate(self,line):
        # result =self.model.evaluate_line(self.sess, create_input(line), self.id_to_tag)
        # line = input('输入文本：')
        result = self.model.evaluate_line(self.sess, input_from_line(line, self.char_to_id), self.id_to_tag)

        # print(result)
        return result