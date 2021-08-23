"""
@File    : jieba_dicttest.py
@Time    : 2021/3/19 10:19
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""
#from __future__ import print_function, unicode_literals
import sys
import os
sys.path.append("../")

from lineModifyTool import lineModify
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')



sentence = "1. 一种变形机器的虚拟现实算法。"

#基于jieba的词性标注
jieba.load_userdict('D:\\NLPdeepLearning\\zhy\\Dell\\jiebaDW\\mergeWord.txt')       
import jieba.posseg as pseg
def readDict(path):
    usingDict = {}
    file = open(path,'r')
    for line in file:
        line = lineModify(line)
        words = line.split()
        for word in words:
            usingDict[word] = 1
    return usingDict

words = jieba.cut(sentence)
print('/'.join(words))
print("="*40)

result = pseg.cut(sentence)
for w in result:
  if w.flag == 'v' and w.word in usingDict.keys():
    print w.word, "/", w.flag, ", "
print("\n" + "="*40)


#基于ltp模型的分词和命名实体识别
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser
segmentor = Segmentor()# 初始化实例
user_dict = "D:\\NLPdeepLearning\\zhy\\Dell\\jiebaDW\\mergeWord.txt"
segmentor.load_with_lexicon('D:\\Python_Packages\\ltp_data\\cws.model',user_dict) # 加载模型
word = segmentor.segment(sentence)  # 分词
def ner(words, postags):
    recognizer = NamedEntityRecognizer() # 初始化实例
    recognizer.load('D:\\Python_Packages\\ltp_data\\ner.model')  # 加载模型
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    for word, ntag in zip(words, netags):
        print word.decode("utf-8") + '/' + ntag
    recognizer.release()  # 释放模型
    return netags

for w in result:
    print(w.word, "/", w.flag, ", ")#, end=' ')

print("\n" + "="*40)
#
#
