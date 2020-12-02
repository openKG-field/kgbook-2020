# -*- coding:utf-8 -*-
'''
@author: zhanghaichao
@license: (C) Copyright liepin
@contact: zhanghaichao@liepin.com
@file: log.py
@time: 2020/4/7 15:40
@desc:
'''
import os
import logging
def log(log_path):
    dir_name=os.path.dirname(log_path)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh=logging.StreamHandler()
    sh.setFormatter(FORMAT)

    ch=logging.FileHandler(log_path)
    ch.setFormatter(FORMAT)
    logger=logging.getLogger()
    logger.addHandler(ch)
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)
    return logger
