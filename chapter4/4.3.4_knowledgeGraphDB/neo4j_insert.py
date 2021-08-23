# -*- encoding: utf-8 -*-
"""
@File    : neo4j_insert.py
@Time    : 2021/3/19 14:00
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""


# from py2neo import Graph,Node,Relationship   #,NodeSelector
# from py2neo import authenticate
#
# authenticate("localhost:7474", "neo4j", "123456")
# Import-Module 'D:\Program Files\neo4j-community-3.5.6\bin\Neo4j-Management.psd1'
def split_point(word):
    
    if word == u'，' or word == u'。' or word ==u'；' or word ==u'！' or word == u'？':
        return True
    return False



def insert_function(relation):
    '''
    Neo4j数据插入
    '''

    link = Graph("http://localhost:7474/db/data/")  # , username="neo4j", password="123456")
    graph = link
    graph.delete_all()

    for i in relation:
        i=i.split('_')
        if i[2] == 'error':
            continue
        print ('......',i[0],i[1],i[2])
        u = Node(i[3], name=i[0])
        # 和分类节点的关系
        v = Node(i[4], name=i[1])
        u_node = graph.find_one(
            property_key='name',
            property_value=i[0],
            label=i[3]
            #property_key=,

        )
        if u_node ==None:
            u_node = u
            graph.create(u_node)

        v_node = graph.find_one(
            property_key='name',
            property_value=i[1],
            label=i[4],
            #property_key="entity1",
            #property_key=i[1]
        )
        if v_node ==None:
            v_node = v
            graph.create(v_node)
        if i[2]=='error':
            print ('....?',u_node,v_node)


        relationship = Relationship(u_node, i[2], v_node)
        graph.create(relationship)

#run()