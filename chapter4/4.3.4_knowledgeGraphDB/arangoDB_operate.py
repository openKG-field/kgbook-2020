# -*- encoding: utf-8 -*-
"""
@File    : arango_imp.py
@Time    : 2021/3/19 14:00
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""

from pyArango.connection import *
import psycopg2
from hanziconv import HanziConv


CONNECT_DB_URL = "dbname"


def get_categories():
    conn = psycopg2.connect(CONNECT_DB_URL)
    cur = conn.cursor()
    cur.execute('select * from kg_categories')

    lst_category = []
    dict_category_all = {}
    for rec in cur:
        str_uri, str_label = rec[0], rec[1]
        lst_broaders = rec[3] if rec[3] else None
        lst_related = rec[4] if rec[4] else None

        dict_category_all[str_uri] = (str_label, lst_broaders, lst_related)
        lst_category.append(str_uri)

    cur.close()
    conn.close()

    return lst_category, dict_category_all


def imp_categories(lst_urls, dict_category_all):
    conn = Connection(arangoURL="http://localhost:8080", username="root",
                      password="123")
    db = conn["iecas_kg"]
    col = db["Categories"]

    # conn1 = psycopg2.connect("host=127.0.0.1 dbname=kg_name user=postgres "
    #                          "password=123")
    # cur = conn1.cursor()
    # cur.execute("select * from skos_categories where uri in %s",
    #             (tuple(lst_urls),))
    # lst_tmp = []
    for url in lst_urls:
        if url in dict_category_all:
            doc = col.createDocument()
            doc["category_uri"] = url
            doc["category_name"] = dict_category_all[url][0]
            doc["category_broader"] = dict_category_all[url][1]
            doc["category_related"] = dict_category_all[url][2]
            doc.save()
    # for url in lst_urls:
    #     if url not in lst_tmp:
    #         print(url)


def imp_edges():
    conn = Connection(arangoURL="http://localhost:19000", username="root",
                      password="123")
    db = conn["kg"]

    aql = "FOR x IN Categories RETURN x"
    aql1 = "FOR c IN Categories FILTER c.category_uri == @category_uri " \
           "LIMIT 1 RETURN c"
    queryResult = db.AQLQuery(aql, rawResults=False, batchSize=100)
    g = db.graphs["iecas_graph"]
    for x in queryResult:
        print(x["category_name"])
        if not x["category_broader"]:
            continue
        for label in x["category_broader"]:
            bindVars = {'category_uri': label}
            # y = db["Categories"].fetchFirstExample({'category_uri': label},
            #                                        rawResults=False)[0]

            queryResult1 = db.AQLQuery(aql1, rawResults=False, batchSize=1,
                                      bindVars=bindVars)
            if queryResult1 and len(queryResult1) > 0:
                y = queryResult1[0]
                # linking them
                # print(x._id, y._id)
                g.link('isSubclassOf', x, y, {'type': 'isSubclassOf'})


if __name__ == '__main__':

    # categoriesCollection = db.createCollection(name="Categories")
    # imp_categories(*get_categories())
    imp_edges()
