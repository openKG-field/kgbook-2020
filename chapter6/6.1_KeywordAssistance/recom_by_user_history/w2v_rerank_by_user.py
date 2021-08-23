# -*- encoding: utf-8 -*-
"""
@File    : w2v_rerank_by_used.py
@Time    : 2021/1/25 11:29
@Author  : Zhaohy
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""

from gensim.models import word2vec

currDir = './..'
model_cn=word2vec.Word2Vec.load(currDir + "/wc.model")

model_en = word2vec.Word2Vec.load(currDir + '/Word2vecEnglish.model')
import json



def suggestion_by_user(words,N,recom_limit=50,userid=None,history_limit=20,language=1):
    '''
    @words : 输入的待推荐词  list
    @ N : top N 相似
    @ recom_limit : 每一个词相关的推荐词最大量
    @ userid : 用户id
    @ history_limit : 用户历史热词最大截取量
    @ language :  推荐语言主题 1 = CN , else = EN

    整体获取用户历史行为中，对于推荐词的点击记录
    利用点击记录将整体推荐结果重新混排，保证用户行为词保持长期考前
    为保证推荐词的新颖性与流动性，用户点击记录中截取最大【20】个词，整体推荐词总长度为【50】

    '''

    if language == 1 :
        model = model_cn
    else:
        model = model_en
    his_words = {}
    if userid != None :
        data = json.load(open('/home/pydep/pytask/w2v/func_w2v/user_history_click.json','r'))
        if userid in data :
            his_words = data[userid]

    recom_list = []
    for i in words :
        #if True :
        try :
            similar_words = model.most_similar(i,'',N)


            re_rank = {}
            if i in his_words :
                re_rank = his_words[i]
            sub_dict = {}
            count = 0
            '''
            re_rank = {'a':15,'b':3} value = click_times
            
            '''
            tem = []
            his_count = 0
            for j in similar_words :
                word = j[0]
                if word in re_rank and his_count < history_limit:
                    sub_dict[word] = re_rank[word]
                    his_count += 1
                else:
                    sub_dict[word] = count
                    count -= 1
            recom_count = 0
            for k,v in sorted(sub_dict.iteritems(),key=lambda k:k[1],reverse=True):
                print(k,v)
                tem.append(k)
                recom_count += 1
                if recom_count >= recom_limit : break

            recom_list.append(tem)
        except:
            recom_list.append([])
    return recom_list


words = [u'移动',u'移动支付',u'支付',u'什么']

result = suggestion_by_user(words=words,N=100,userid='admin')

for i in result :
    print(i)

