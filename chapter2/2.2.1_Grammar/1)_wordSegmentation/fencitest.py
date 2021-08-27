# -*- encoding: utf-8 -*-
"""
@File    : fencitest.py
@Time    : 2021/3/19 10:19
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""

from __future__ import print_function, unicode_literals
from gensim.models import word2vec
import sys
def FMM_func(user_dict, sentence):
    """
    正向最大匹配（FMM）
    :param user_dict: 词典
    :param sentence: 句子
    """
    # 词典中最长词长度
    max_len = max([len(item) for item in user_dict])
    index = 0
    result = []
    while index < len(sentence):
        #截取index为起始的最大长度字段
        cur = sentence[index:index+max_len]
        word_idx = max_len
        while len(cur) > 0 :
            if cur in user_dict or len(cur) == 1 :
                result.append(cur)
                index = index + word_idx
                break
            else:
                cur = cur[:-1]
                word_idx = word_idx -1
    return result

#key=word,value=weight
user_dict = {'北京':2,'天安门':1}
sentence = '我爱北京天安门，天安门上太阳升。'
seg = FMM_func(user_dict,sentence)
print(seg)

