# -*- encoding: utf-8 -*-
"""
@File    : competitorLocate(1).py
@Time    : 2021/3/19 10:19
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""
'''
method

step 1：
    get goods of object company

step 2:
    search above goods find all patents

step 3:
    collect all companies of above patents

step 4:
    make sure which is the competitor of object company by calculation

'''


def load_data(path):
    count = 0
    # pubid	applicantList	title	abstract	claims	description	fieldWords	techWords	funcWords	goodsList
    data = {}
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            line = line.strip().split('\t')
            count += 1
            if count == 1: continue
            data[line[0]] = {'applicants': line[1].split('$$'), 'goods': line[-1].split('$$')}
    return data


def get_company(company_name, data):
    relate_company = []
    for pubid in data:
        companies = data[pubid]['applicants']
        for com in companies:
            if company_name in com:
                relate_company.append(com)

    return list(set(relate_company))


def get_relate_goods(relate_com, data):
    relate_goods = []
    for pubid in data:
        companies = data[pubid]['applicants']
        goods = data[pubid]['goods']
        if len(set(relate_com) & set(companies)) > 0:
            relate_goods = relate_goods + goods
    return list(set(relate_goods))

def competitor_company(relate_com,relate_good,data):

    competitors = {}

    for pubid in data:
        companies = data[pubid]['applicants']
        goods = data[pubid]['goods']
        inter_good = len(set(relate_good) & set(goods))
        if inter_good > 0:
            base = set(companies) - set(relate_com)
            if len(base) > 0 :
                for com in base :
                    if com not in competitors:
                        competitors[com] = inter_good
                    else:
                        competitors[com] += inter_good

    return competitors

def main():
    path = 'test.txt'
    data = load_data(path)
    target_compnay = '清华'
    relate_com = get_company(target_compnay, data)
    print(relate_com)
    relate_good = get_relate_goods(relate_com, data)
    print('goods = ', relate_good)
    competitor = competitor_company(relate_com,relate_good,data)
    print('competitor = ' ,competitor)
    
    
    
if __name__ == '__main__':
    main()