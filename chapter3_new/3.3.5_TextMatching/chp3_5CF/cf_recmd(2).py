#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : books_method
# @File : cf_recmd.py
# @Time    : 2020/6/18 16:55
# @Author  : Zhaohy
import json

class cf_recmd():

    field_weight = 1
    func_weight = 1
    tech_weight = 1
    good_weight = 1

    #初始化所有备选协同召回矩阵
    def __init__(self):
        self.field_similar = json.load(open('fieldWords_similar.json', 'r'))

        self.func_similar = json.load(open('funcWords_similar.json', 'r'))

        self.tech_similar = json.load(open('techWords_similar.json', 'r'))

        self.good_similar = json.load(open('goodsList_similar.json', 'r'))

    #矩阵加和时提供不同的权重
    def weight_modify(self,weights):
        '''
        :param weights: list of float [ field, func, tech, good]
        :return:
        '''
        self.field_weight,self.func_weight,self.tech_weight,self.good_weight = weights


    #按照公开号 推荐召回，召回数量top
    def recmd_top(self,pubid,top):
        cur_field_dict = self.field_similar[pubid]
        cur_tech_dict = self.tech_similar[pubid]
        cur_func_dict = self.func_similar[pubid]
        cur_good_dict = self.good_similar[pubid]


        def top_recmd(dict,top,weight):
            count = 0
            cur = []
            for k,v in sorted(cur_field_dict.items(),key=lambda k:k[1],reverse=True):
                count += 1
                cur.append((k,float(v)*float(weight)))
                if count > top :
                    break
            return cur

        field_arr = top_recmd(cur_field_dict,top,self.field_weight)
        tech_arr = top_recmd(cur_tech_dict,top,self.tech_weight)
        func_arr = top_recmd(cur_func_dict,top,self.func_weight)
        good_arr = top_recmd(cur_good_dict,top,self.good_weight)

        mea_dict = {}

        arr = field_arr + tech_arr + func_arr + good_arr
        for (p,v) in arr :
            if p not in mea_dict :
                mea_dict[p] = v
            else:
                mea_dict[p] = mea_dict[p] + v


        count = 0

        recmd_list = []
        for k,v in sorted(mea_dict.items(),key=lambda k:k[1],reverse=True):
            count += 1
            recmd_list.append(k)

            if count > top :
                break

        return recmd_list


if __name__ == '__main__':
    cf = cf_recmd()
    pubid = 'CN205752064U'
    recmd_list = cf.recmd_top(pubid,20)
    print(recmd_list)


