#coding=utf-8

'''
Graph_algorithms图算法
https://www.cnblogs.com/alan-blog-TsingHua/p/10924894.html
连通图与非连通图,未加权图与加权图
有向图与无向图,非循环图和循环图
Data:
mqpat database，
'''


'''
TODO:
fieldsIndivideBase,
通过5G领域的英文专利引用数据citedList，来计算技术路线和最重要的专利；
通过引用数据，发现某些技术的领先申请人群或发明人群；
通过对人工智能领域中的knowledgeGraph表内容抽取出来，我们可以看图谱技术路线。

'''
#import xmlrpclib
from pymongo import MongoClient
import codecs
import dis
#proxy = xmlrpclib.ServerProxy("http://103.105.201.54:30004")

import xmlrpc.client
proxy = xmlrpc.client.ServerProxy("http://103.105.201.54:30004")

def v4Mongo(tb):
    #host ='10.0.5.12'
    host = '103.105.201.54'
    port = 27017
    passwd = 'mq2019'
    dbName = 'mqpatv4'
    user = 'mqpatv4-rw'
    myTbNme = tb
    conn = MongoClient(host, port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[myTbNme]
    return (conn, db, collection)

def wordMongo(tb):
    #host ='10.0.5.12'
    host = '103.105.201.54'
    port = 27017
    passwd = 'mq2019'
    dbName = 'mqpat'
    user = 'mqpat-rw'
    myTbNme = tb
    conn = MongoClient(host, port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[myTbNme]
    return (conn, db, collection)

#(conn, db, col) = v4Mongo('fieldsIndivideBase')
(conn, db, col) = wordMongo('fieldsIndivideBase')


'''
我们关注三类核心的图算法：路径搜索（Pathfinding and Search）、中心性计算（Centrality Computation）和社群发现（Community Detection）。
图搜索算法（Pathfinding and Search Algorithms）探索一个图，用于一般发现或显式搜索。这些算法通过从图中找到很多路径，但并不期望这些路径是计算最优的
（例如最短的，或者拥有最小的权重和）。图搜索算法包括广度优先搜索和深度优先搜索，它们是遍历图的基础，并且通常是许多其他类型分析的第一步。
图算法中最基础的两个遍历算法：广度优先搜索（Breadth First Search，简称 BFS）和深度优先搜索（Depth First Search，简称 DFS）。
BFS 从选定的节点出发，优先访问所有一度关系的节点之后再继续访问二度关系节点，以此类推。DFS 从选定的节点出发，选择任一邻居之后，尽可能的沿着边遍历下去，知道不能前进之后再回溯。
这两个图搜索算法更多地作为底层算法支持其他图算法。例如，最短路径问题和 Closeness Centrality （在后文会有介绍）都使用了 BFS 算法；
而 DFS 可以用于模拟场景中的可能路径，因为按照 DFS 访问节点的顺序，我们总能在两个节点之间找到相应的路径。
感兴趣的话，可以猜一猜，后文介绍的算法是否使用了图搜索算法，并且分别使用了 DFS 还是 BFS。
'''

import graphx
for v in V:
    v.d = MAX
    v.pre = None
    v.isFind = False
root. isFind = True
root.d = 0
que = [root]
while que !=[]:
    nd = que.pop(0)
    for v in Adj(nd):
        if not v.isFind :
            v.d = nd.d+1
            v.pre = nd
            v.isFind = True
            que.append(v)

def dfs(G):
    time = 0
    for v in V:
        v.pre = None
        v.isFind = False
    for v in V : # note this,
        if not v.isFind:
            dfsVisit(v)
    def dfsVisit(G,u):
        time =time+1
        u.begin = time
        u.isFind = True
        for v in Adj(u):
            if not v.isFind:
                v.pre = u
                dfsVisit(G,v)
        time +=1
        u.end = time


'''
https://www.jianshu.com/p/df41c4e8f34e
1/最短路径:给出关系传播的度数（degree），可以快速给出两点之间的最短距离，可以计算两点之间成本最低的路线等等。

2/最小生成树（Minimum Spanning Tree）算法从一个给定的节点开始，查找其所有可到达的节点，以及将节点与最小可能权重连接在一起，行成的一组关系。
它以最小的权重从访问过的节点遍历到下一个未访问的节点，避免了循环。
最常用的最小生成树算法来自于 1957 年的 Prim 算法。Prim 算法与Dijkstra 的最短路径类似，所不同的是， 
Prim 算法每次寻找最小权重访问到下一个节点，而不是累计权重和。并且，Prim 算法允许边的权重为负。

3/随机游走:作为 node2vec 和 graph2vec 算法的一部分，这些算法可以用于节点向量的生成，从而作为后续深度学习模型的输入；
作为 Walktrap 和 Infomap 算法的一部分，用于社群发现。如果随机游走总是返回同一组节点，表明这些节点可能在同一个社群；


'''

#Prim
for v in V:
    v.minAdjEdge = MAX
    v.pre = None
root.minAdjEdge = 0
que = priority-queue (G.V)  # sort by minAdjEdge
while not que.isempty():
    u = que.extractMin()
    for v in Adj(u):
        if v in que and v.minAdjEdge>w(u,v):
            v.pre = u
            v.minAdjEdge = w(u,v)

#Kruskal 算法

#Dijkstra 算法
def dijkstra(G,s):
    initialize(G,s)
    paths=[]
    q = priority-queue(G.V) # sort by distance
    while not q.empty():
        u = q.extract-min()
        paths.append(u)
        for v in Adj(u):
            relax(u,v,w(u,v))






'''

中心性算法:中心性算法（Centrality Algorithms）用于识别图中特定节点的角色及其对网络的影响。中心性算法能够帮助我们识别最重要的节点，
帮助我们了解组动态，例如可信度、可访问性、事物传播的速度以及组与组之间的连接。尽管这些算法中有许多是为社会网络分析而发明的，但它们已经在许多行业和领域中得到了应用。
度量方式：
DegreeCentrality
ClosenessCentrality
BetweennessCentrality
'''



'''
PageRank:在所有的中心性算法中，PageRank 是最著名的一个。它测量节点传递影响的能力。
PageRank 不但节点的直接影响，也考虑 “邻居” 的影响力。例如，一个节点拥有一个有影响力的 “邻居”，
可能比拥有很多不太有影响力的 “邻居” 更有影响力。PageRank 统计到节点的传入关系的数量和质量，从而决定该节点的重要性。

'''






'''
https://www.cnblogs.com/tychyg/p/5277137.html
社群发现算法:社群的形成在各种类型的网络中都很常见。识别社群对于评估群体行为或突发事件至关重要。
对于一个社群来说，内部节点与内部节点的关系（边）比社群外部节点的关系更多。识别这些社群可以揭示节点的分群，

找到孤立的社群，发现整体网络结构关系。社群发现算法（Community Detection Algorithms）有助于发现社群中群体行为或者偏好，
寻找嵌套关系，或者成为其他分析的前序步骤。社群发现算法也常用于网络可视化。
社区划分问题大多基于这样一个假设：同一社区内部的节点连接较为紧密，社区之间的节点连接较为稀疏。因此，社区发现本质上就是网络中结构紧密的节点的聚类。
　　从这个角度来说，这跟聚类算法一样，社区划分问题主要有两种思路：           （1）凝聚方法(agglomerative method)：添加边
　　　　（2）分裂方法(divisive method)：移除边
1/MeasuringAlgorithm

2/ComponentsAlgorithm

3/LabelPropagation Algorithm:标签传播(Label propagation)算法是由Zhu X J于2002年提出[5]，它是一种基于图的半监督学习方法，
其基本思路是用已标记节点的标签信息去预测未标记节点的标签信息。2007年，Raghavan U N等最早提出将LPA最早应用于社区发现，该算法被简称为RAK算法[6]
思想: 每个节点赋予一个标签标志着其所在社区，每次迭代，每个节点标签根据其大多数邻近节点的标签而修改，收敛后具有相同标签的节点属于同一个社区。
算法步骤:
Step1 给每一个节点随机生成一个标签
Step2 随机生成一个所有节点的顺序，按照该顺序将每一个节点的标签修改为其大多数邻居节点的标签。
Step3 重复step2，直到每个节点的标签都不再变化，具有相同标签的节点组成了一个社区。

4/LouvainModularity Algorithm: Louvain (BGLL) 算法[8]是一个基于模块度最优化的启发式算法，算法两层迭代，外层的迭代是自下而上的凝聚法，
内层的迭代是凝聚法加上交换策略，避免了单纯凝聚方法的一个很大的缺点(两个节点一旦合并，就没法再分开)。
利用spark进行层次社团发现(louvain算法测试)

5/GN算法相当于是一棵自顶向下的层次树，划分社区就是层次分裂的过程。
　　解决的办法：
　　　　引入模块度Q，模块度是用来衡量社区划分好坏的程度的概念。除此之外，我觉得基本上整个算法的思想都反过来了，不再是从顶层分裂，
而是从底层合并聚类，直到最终形成一个大的网络。每次是根据计算合并后使得模块度Q的增量最大的社区进行合并，直到收敛。
也就是说，是基于增加边而不是删除边了。这种引入模块度Q来度量社区划分质量的思想，有点像梯度下降算法，是通过迭代计算来获得定义的目标函数的最优解的。
https://www.cnblogs.com/zichun-zeng/p/6825453.html

'''



'''
9.Canopy算法 + K-Means
9.1 Canopy算法
思想：选择计算代价较低的方法计算相似性，将相似的对象放在一个子集中，这个子集被叫做Canopy,不同Canopy之间可以是重叠的
算法步骤:
Step1 设点集为 S，预设两个距离阈值 T1和 T2（T1>T2）；
Step2 从S中任选一个点P，用低成本方法快速计算点P与所有Canopy之间的距离，将点P加入到距离在T1以内的Canopy中；如果不存在这样的Canopy，则把点P作为一个新的Canopy的中心，并与点P距离在 T2 以内的点去掉；
Step3 重复step2, 直到 S 为空为止。
该算法精度低，但是速度快，常常作为“粗”聚类，得到一个k值，再用k-means进一步聚类，不属于同一Canopy 的对象之间不进行相似性计算。

'''



'''
谱聚类算法
        首先给出一个概念——图的Laplacian 矩阵（L-矩阵）。
谱算法的实质是矩阵分解，其他的矩阵分解方法还有SVD 和 NMF 等，矩阵分解的整体思想就是把点从一个空间映射到另一个空间，在新的空间利用传统的聚类方法来聚类。


'''






'''
图算法的抽象分析能力和区块链的去中心化的分布式存贮结合可以有效提升区块链的数据同步性能。Trias的图算法通过TEE技术和Gossip协议来完成，也就是HCGraph算法。

HCGraph算法

HCGraph算法为了减少区块链中使用TEE的难度，Leviatom提出了异构共识图协议（HCGraph），引入了信任传递关系网。HCGraph 让临近的具备 TEE 运行环境的节点互相验证对方的可信度，
并将所收集到的可信节点信息在已获得其信任的其它节点见传播。这样每TEE共识节点的状态信息就能形成一个信誉关 系网，互相背书互相证明，一旦有一个节点要“撒谎”，
周围的节点都会立刻就能指正它。


'''