#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : books_method
# @File : config.py
# @Time    : 2020/7/6 15:30
# @Author  : Zhaohy

params = {
    'booster': 'gbtree',
    'objective': 'multi:softmax',
    'num_class':2,
    'gamma': 0.1,
    'max_depth': 5,
    'lambda': 3,
    'subsample': 0.7,
    'colsample_bytree': 0.7,
    'min_child_weight': 3,
    'eta': 0.1,
    'seed': 1000,
}