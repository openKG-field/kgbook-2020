# -*- encoding: utf-8 -*-
"""
@File    : Community_Detection.py
@Time    : 2021/3/19 12:49
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""


class Node:
    name = ''
    edge = ''
    com = []
    next = []

    def __init__(self, name):
        self.name = name

    def link(self, edge, next):
        self.next = next
        self.edge = edge

    def com_set(self, com):
        self.com = com


class community_detect():
    graph = None

    def __init__(self, grpah):
        self.graph = grpah

    def Louvain(self):

        def delt_modularity_Q(communitys, n, m):
            coms = []
            if communitys.com == []:
                coms = [communitys]
            else:
                coms = communitys.com
            # result between 0.3 - 0.7 is good result
            tem = 0
            # delta_q =  1/2m ( communitys 与 n 链接的边 - 社区内点不在社区的边*n的边/m )
            com_n_edge = 0
            out_com_edge = 0
            all_node = coms + n
            n_edge = 0
            for i in coms:
                com_n_edge = com_n_edge + len(set(i.next) & set(n))
                out_com_edge = out_com_edge + len(set(i.next) - set(all_node))
            for i in n:
                n_edge = n_edge + len(i.next)
                com_n_edge = com_n_edge + len(set(i.next) & set(coms))
                out_com_edge = out_com_edge + len(set(i.next) - set(all_node))
            # print('test = ',com_n_edge,out_com_edge,n_edge,m)
            delta_q = 1 / 2 / float(m) * (float(com_n_edge) - float(out_com_edge * n_edge) / float(m))
            return delta_q

        def merge_node(nodes):
            new_name = 'com'
            new_edge = 0
            new_next = []
            new_com = []
            for i in nodes:
                new_name = new_name + '_' + i.name
                new_edge += i.edge
                new_next = new_next + i.next
                if i.com == []:
                    new_com = new_com + [i]
                else:
                    new_com = new_com + i.com
            new_next = list(set(new_next))
            new = Node(new_name)
            new.link(new_edge, new_next)
            new.com_set(new_com)
            return new

        nodes = self.graph
        m = 0
        for i in self.graph:
            m = m + len(i.next)

        count = 0
        while True:
            count += 2
            # if count > 50 : break
            left_node = []
            used_node = []
            break_flag = True
            # 便利所有节点和与之相连的节点，
            for node in nodes:

                tem = node.next
                delta = node.com
                merge_list = []
                # 当前点的链接点
                # print('next = ',tem)
                for n in set(tem) - set(delta):
                    # print(n)
                    if n.com == []:
                        tar_node = [n]
                    else:
                        tar_node = n.com
                    delta_q = delt_modularity_Q(node, tar_node, m)
                    if delta_q > 0:
                        print('merge = ', node.name, '  and  ', n.name)
                        merge_list.append(n)
                        break_flag = False

                if not break_flag:
                    merge_list.append(node)
                if len(merge_list) != 0:
                    used_node = used_node + merge_list
                    new_node = merge_node(merge_list)
                    # print(new_node.name)
                    left_node.append(new_node)

                if not break_flag:
                    break

            left_node = list(set(left_node + list(set(nodes) - set(used_node))))
            print(len(left_node))
            # print ( [i.name for i in left_node])
            if break_flag:
                break
            else:
                nodes = left_node
            if len(nodes) < 2: break

        return nodes


def load_data(path):
    '''
    利用 class Node  组成 graph
    graph = list
    e.g. :
    graph = []
    a = Node('a')
    a.link(3,[b,c,d])

    graph.append(a)

    cd = community_detect(graph)

    clusters = cd.Louvain()

    for i in clusters :
        print(i.name)  此处为当前聚类的所有原始node名称
    '''

    count = 0
    graph = []
    node_dict = {}
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            line = line.strip().split('\t')
            count += 1
            if line[3] == '-1' or count == 1 or len(line) < 4: continue
            cur = line[3].split('__')

            if line[0] in node_dict:
                node_dict[line[0]] = node_dict[line[0]] | set(cur)
            else:
                node_dict[line[0]] = set(cur)
            for i in cur:
                if i in node_dict:
                    node_dict[i] = node_dict[i] | {line[0]}
                else:
                    node_dict[i] = {line[0]}
            if count > 100: break

    print(node_dict)
    str_node = {}
    cp = []
    for i in node_dict:
        name = i
        edge = list(node_dict[i])
        tem = Node(name)
        tem.link(len(edge), edge)
        str_node[name] = tem
        cp.append(tem)
    for i in cp:
        str_list = i.next
        cur = []
        for j in str_list:
            cur_node = str_node[j]
            cur.append(cur_node)
        i.link(len(cur), cur)
        graph.append(i)

    print(len(graph))

    cd = community_detect(graph)

    clusters = cd.Louvain()
    for i in clusters:

        cur = i
        print('result = ',cur.name)






path = 'graph_data'
load_data(path)
