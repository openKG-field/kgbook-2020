#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@File     : test.py
@Time     : 2021/3/24 15:41
@Author   : zhaohongyu
@Email    : zhaohongyu2401@yeah.net
@Software : PyCharm
"""


import  json
def test(path):

    en_words = json.load(open(path,'r',encoding='utf8'))

    for i in en_words['enPathDict']:
        print(i)


path = 'en_Path_Dict.json'
test(path)


