# -*- encoding: utf-8 -*-
"""
@File    : weighted_Search.py
@Time    : 2021/3/19 14:00
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""
from text_similarity import  *
def weight_search(sentence):
    word,weight,datas = text_similar(sentence)

    doc_weight = {}
    for i in range(len(weight)-1 ):
        # sentence 将会是最后一条数据
        cur_weight = 0
        for j in range(len(word)):
            if word[j] in sentence :
                cur_weight = cur_weight + max(weight[i][j],0.01)
                #考虑到tfidf对于部分数据的过滤，保留最小相似度
        doc_weight[i] = cur_weight

    similar_result = []
    for i in doc_weight:
        similar_result.append({'doc':datas[i],'weight':doc_weight[i]})
    similar_result.sort(key=lambda k:k['weight'],reverse=True)
    return similar_result

def main():
    sentence = '高频$$宽带$$线性$$稳定$$低噪声$$可靠$$负反馈$$性能$$任意组合$$集成$$厚膜$$薄膜生产$$任意$$组合$$生产$$反馈$$直流$$低频$$范围'.split('$$')
    result = weight_search(sentence)
    top3 = result[:3]
    for i in top3:
        print(i)


if __name__ == '__main__':
    main()

