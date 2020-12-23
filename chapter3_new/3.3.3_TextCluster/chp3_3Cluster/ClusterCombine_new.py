#coding=utf-8
from sklearn import datasets
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
from pymongo import MongoClient
import codecs
from sklearn.cluster import KMeans
import xmlrpc.client

from numpy import *

'''
distance calculation
1欧式距离

2.明氏距离
其中，t为一个正整数。
曼哈顿距离：

马氏距离：
其中， 表示样本协方差阵的逆阵，T在运算里表示矩阵的转置。

'''
def Eucli_distance(vecA,vecB):
    return sqrt(sum(power(vecA - vecB, 2)))

def Eucli_distance_vec(vecA,vecB):

    s = 0
    i = 0
    while i < len(vecA):
        s = s+ power(vecA[i]-vecB[i],2)
    return sqrt(s)

def manhattan_distance(vecA,vecB):
    dis = 0
    for i in range(len(vecA)):
        dis += abs(vecA[i]-vecB[i])
    return dis

def chebyshev_distance(vecA,vecB):
    if len(vecA) <3 : return -1 #使用切比雪夫距离 维度推荐至少大于2
    dis = -1
    for i in range(len(vecA)):
        cur = abs(vecA[i] - vecB[i])
        if cur > dis :
            dis = cur
    return dis

def Minkowski_distance(vecA,vecB):
    if len(vecA) == 1 :
        return manhattan_distance(vecA,vecB)
    elif len(vecA) == 2 :
        return Eucli_distance(vecA.vecB)
    elif len(vecA) > 3 :
        return chebyshev_distance(vecA,vecB)
    else:
        return -1 # 向量长度为0

def Mahalanobis_distance(vecAList,vecBList):
    '''
    :param vecAList:
    :param vecBList:
    :return:
    '''
    # 马氏距离与样本总量相关且样本量应该大于数据维度，与当前整体计算逻辑不符合
    pass

'''
word embedding获取词向量
'''
import xmlrpc.client
proxy = xmlrpc.client.ServerProxy("http://103.105.201.54:30004")

def similar(wordList):
    result = []
    simArray=[]
    count = 0
    topnn = 20  # int(sys.argv[3])
    typeCode = 1
    wordList = list(set(wordList))
    print ('the length is',len(wordList))
    for i in wordList:
        simList = proxy.wordArray(i)
        if type(simList) is not list:
            continue
        else:
            count += 1
            simArray.append(simList)
            result.append(i)
    #print ('count value = ',count)
    return simArray, result

'''
Algorithm:
#  Kmeans,DBSCAN,AGNES,具体算法如下所示。

'''
'''
K-meaans
'''
class kmeans():
    def word_label(cluster, center):

        result = {}
        for i in cluster:
            # 每一个类别，求距离圆心最近的点作为标记
            cur_cen = center[i]
            min_dis = 100000000
            word_lab = ''
            disMap = {}
            wordList = []
            for m in cluster[i]:
                word = m['word']
                vec = m['vec']
                dis = Eucli_distance(cur_cen, vec)
                disMap[m['word']] = dis
                # if dis < min_dis :
                #     min_dis = dis
                #     word_lab = word

            for key, value in sorted(disMap.items(), key=lambda k: k[1], reverse=True):  # (k, v): (v, k)
                # word_lab = k[:2]
                wordList.append(key)
            word_lab = '\t'.join(wordList[0:4])

            # 取得最小距离的词 并存入返回结果中
            result[i] = word_lab
        return result

    def word_cluster(wordsList, vecList, k):
        o = open('result-DL-sat-field.txt', 'w',encoding='utf8')
        clf = KMeans(n_clusters=k, random_state=9)
        y_pred = clf.fit(vecList)
        cluster = {}
        for i in range(len(y_pred.labels_)):
            ind = y_pred.labels_[i]
            if ind in cluster:
                cluster[ind].append({'word': wordsList[i], 'vec': vecList[i]})
            else:
                cluster[ind] = [{'word': wordsList[i], 'vec': vecList[i]}]

        center = y_pred.cluster_centers_
        word_lab = kmeans.word_label(cluster, center)

        for i in word_lab:
            o.write('cluster ' + str(i) + ' center_word ' + word_lab[i] + '\n\n')
            for m in cluster[i]:
                o.write(m['word'] + '\t')
            o.write('\n\n')

'''
dataSet:wordsArray
'''

# wordList=[]
# with codecs.open('predict_field_new.txt','r',encoding='utf-8') as f:
#     for i in f.readlines():
#         wordList.append(i.strip())
#
# vecList, wordList = similar(wordList)
#
# print(len(wordList), wordList)
# print(len(vecList))
#
# kmeans.word_cluster(wordList, vecList, 5)


'''
semi-supervision Kmeans:
半监督K-means的初始聚类中心的选择是根据有标签数据而定的，聚类个数=类别个数，初始聚类中心=各个类样本的均值（其余步骤和标准的K-means没有差别）
标签可以是fieldsName，funcName，objectName等。
'''

class semi_supervision_Kmeans():
    # label_data = None
    # data = None
    #init_centroids = None

    def __init__(self,label_data,data):
        self.label_data = label_data
        self.data = data
        centroids = []
        label_list = np.unique(label_data[:, -1])
        for i in label_list:
            label_data_i = label_data[(label_data[:, -1]) == i]
            cent_i = np.mean(label_data_i, 0)
            centroids.append(cent_i[:-1])

        self.init_centroids = np.array(centroids)

    def fit(self,label_data,data):
        '''
        按照输入的label结果，设定初始聚类数量，并初始化聚心

        按照data 数据的情况，以kmeans手段更新聚心，最终返回聚类结果

        :return: 聚类结果
        '''

        def distence(vecA, vecB):
            return np.sqrt(sum(np.power(vecA - vecB, 2)))

        dataSet = np.vstack((self.label_data[:, :-1], self.data))
        label_list = np.unique(self.label_data[:, -1])
        k = len(label_list)
        m = np.shape(dataSet)[0]

        clusterAssment = np.zeros(m)  # 初始化样本的分配
        centroids = self.init_centroids  # 确定初始聚类中心
        clusterChanged = True
        while clusterChanged:
            clusterChanged = False
            for i in range(m):  # 将每个样本分配给最近的聚类中心
                minDist = np.inf
                minIndex = -1
                for j in range(k):
                    distJI = distence(centroids[j, :], dataSet[i, :])
                    if distJI < minDist:
                        minDist = distJI
                        minIndex = j
                if clusterAssment[i] != minIndex: clusterChanged = True
                clusterAssment[i] = minIndex

            for cent in range(k):

                ptsInClust = dataSet[np.nonzero(clusterAssment == cent)[0]]
                centroids[cent, :] = np.mean(ptsInClust, axis=0)

        cluster_result = []
        for i in range(len(dataSet)):
            cluster_result.append(list(dataSet[i]) + [clusterAssment[i]])

        return cluster_result


# label_data = pd.read_csv('watermelon3_0_En.csv',header=None,encoding="gbk",skiprows=1,skipfooter=1,index_col=0,engine="python")
# #L = data.values
# data = [['black','lightCurl','heavily','blur','dimple','soft',0.481,0.149],\
#      ['green','stiff','clear','distinct','smooth','soft',0.243,0.267]]
# semi_kmeans = semi_supervision_Kmeans()
# a = semi_kmeans(label_data,data)
# print(a.fit())


def knn(clusters,datas,n):
    '''
    @ clusters : dict of list {cluster_name : [cluster_eles_vector]   }
    @ datas : list of data of vector [data_ind[data_vector]]
    @ n : number of cluster limit 
    '''
    
    data_result = []
    
    for i in data :
        #每一个待分类数据的向量
        dis_dict = {}
        count = 0 
        for clu_name in clusters :
            clu = clusters[clu_name]
            for j in clu :
                #向量长度一致
                if len(i) == len(j):
                    dis = Eucli_distance(i,j)
                    dis_dict[(clu_name,count)] = dis 
                    count +=  1
        vote_dict = {}
        count = 0 
        for k,v in sorted(dis_dict.iteritems(),key=lambda k:k[1],reverse=False):
            (name,num) = k 
            if name in vote_dict:
                vote_dict[name] += 1 
            else:
                vote_dict[name] =  1
            count += 1 
            if count > n : break 
        
        c_name = ''
        for k,v in sorted(vote_dict.iteritems(),key=lambda k:k[1],reverse=True):
            c_name = k 
            break
        
        data_result.append(c_name)
                
                
    return data_result
    
    

'''
K-means算法缺点的改进：
针对上述第(3)点，不随机选取聚类中心，而是从所有的数据点中选出密度最大的一个点作为第一个初始聚类中心点。然后选择距离该点最远的那个点作为第二个初始类簇中心点，
然后再选择距离前两个点的最短距离最大的那个点作为第三个初始类簇的中心点，以此类推，直至选出K个初始类簇中心点。
使得第一个初始聚类中心不需要随机选取，而是选取最大密度点。对于一些典型的凸形状中心密度大的类型数据第一个初始点很接近它的类中心点。
TODO:improve Kmeans
'''
def im_keans():
    return 0


'''
1.凝聚层次聚类：AGNES算法(自底向上)
首先将每个对象作为一个簇，然后合并这些原子簇为越来越大的簇，直到某个终结条件被满足
2.分裂层次聚类：DIANA算法(自顶向下)
首先将所有对象置于一个簇中，然后逐渐细分为越来越小的簇，直到达到了某个终结条件。
'''
class Agnes():

    k  = 0
    def __init__(self,k):
        self.k = k

    def fit(self,points,dis_method):
        '''

        :param points:  list of points
        :param dis_method:  min_dis,max_dis,mean_dis
        :return:
        '''

        #三种不同的距离评价方式
        def min_dis(c1,c2):
            dis = 999999999

            for i in c1 :

                for j in c2 :
                   tem = Eucli_distance(i,j)
                   if dis > tem :
                       dis = tem
            return dis

        def max_dis(c1,c2):
            dis = -1

            for i in c1 :
                for j in c2 :
                    tem = Eucli_distance(i,j)
                    if dis < tem :
                        dis = tem
            return dis

        def mean_dis(c1,c2):
            dis = 0
            count = 0
            for i in c1 :
                for j in c2 :
                    tem = Eucli_distance(i,j)
                    dis = dis + tem
                    count += 1
            if count == 0 : return 0

            return float(dis)/float(count)

        #将每一位元素默认为最小类，并以此按照同组最小簇合并
        k_cluster = points.copy()
        if len(k_cluster) < self.k :
            print('number of cluster must largger than number of input points')
            return []

        while len(k_cluster) > self.k :

            for i in range(len(k_cluster)):
                min = 999999999
                ind = -1
                for j in range(i+1,len(k_cluster)-1):

                    if dis_method == 'min_dis':

                        dis = min_dis(k_cluster[i],k_cluster[j])
                    elif dis_method == 'max_dis':
                        dis = max_dis(k_cluster[i],k_cluster[j])
                    else:
                        print (type(k_cluster[i]))
                        dis = mean_dis(k_cluster[i],k_cluster[j])

                    if dis < min :
                        min = dis
                        ind = j
                        break
                if ind == -1 : continue
                k_cluster[i] = k_cluster[i] + k_cluster[ind]
                k_cluster.pop(ind)
                print (len(k_cluster))
                if len(k_cluster) == self.k :
                    return k_cluster

# wordList=[]
# with codecs.open('predict_field_new.txt','r',encoding='utf-8') as f:
#     for i in f.readlines():
#         wordList.append(i.strip())
#
# vecList, wordList = similar(wordList)
#
# print(len(wordList), wordList)
# print(len(vecList[0]))

#
# for i in range(len(result)):
#     print(i, ' cluster = ',)
#     tem = 0
#     while tem < len(result[i]):
#         cur = result[i][tem:tem+200]
#         ind = vecList.index(cur)
#         word = wordList[ind]
#         print(word, '  ')
#         tem += 200




'''
DBSCAN聚类算法，输入ε (eps) 和形成高密度区域所需要的最少点数 (minPts)
几个必要概念： 
ε-邻域：对于样本集中的xj, 它的ε-邻域为样本集中与它距离小于ε的样本所构成的集合。 
核心对象：若xj的ε-邻域中至少包含MinPts个样本，则xj为一个核心对象。 
密度直达：若xj位于xi的ε-邻域中，且xi为核心对象，则xj由xi密度直达。 
密度可达：若样本序列p1, p2, ……, pn。pi+1由pi密度直达，则p1由pn密度可达。

当T集合中存在样本时执行如下步骤： 
记录当前未访问集合P_old = P 
从T中随机选一个核心对象o,初始化一个队列Q = [o] 
P = P-o(从T中删除o) 
 2.4当Q中存在样本时执行： 
     2.4.1取出队列中的首个样本q 
     2.4.2计算q的ε-邻域中包含样本的个数，如果大于等于MinPts，则令S为q的ε-邻域与P的交集， 
             Q = Q+S, P = P-S 
 2.5 k = k + 1,生成聚类簇为Ck = P_old - P 
 2.6 T  = T - Ck 
划分为C= {C1, C2, ……, Ck}

'''

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

class DBSCAN():
    esp = 0
    minP = 0
    #初始化数据，设定esp 和 minP
    def __init__(self,esp,minP):
        self.esp=esp
        self.minP = minP

    def fit(self,points):
        '''
        :param points: list of points , each point format as vector like [1,2,3,4...]
        :return:
        '''

        noisy_points = []
        key_points_cluster =  {}
        #考虑噪音数据 与 核心点
        #循环每一个初始点
        for i in range(len(points)):

            tem_cluster = []
            cur_pt = points[i]

            for j in range(i+1,len(points)) :
                tem_pt = points[j]

                dis = Eucli_distance_vec(cur_pt,tem_pt)
                if dis < self.esp:
                    tem_cluster.append(j)

            #esp内周围点的数据判断是否为噪音点与核心点
            if len(tem_cluster)  == 0 :
                noisy_points.append(i)


            #确定核心点之后，依靠connection方法，将每一个密度可达的点加入到当前的簇中，直至加无可加，该簇修改结束
            if len(tem_cluster) > self.minP :
                key_points_cluster[i] =tem_cluster

                #connection算法， 遍历每一个可能的链接点，直至可触发的初始连接点全部使用后为止
                def connection(points,tem_cluster):

                    for_list  = tem_cluster.copy()

                    while len(for_list) > 0 :
                        tem = for_list.pop(0)
                        for t in range(len(points)) :
                            if t in for_list : continue
                            if Eucli_distance_vec(points[tem],points[t]) < self.esp :
                                for_list.append(t)
                                tem_cluster.append(t)
                    return tem_cluster
                connect_points = connection(points,tem_cluster)

                key_points_cluster[i] = connect_points

        return key_points_cluster,noisy_points



wordList=[]
with codecs.open('predict_field_new.txt','r',encoding='utf-8') as f:
    for i in f.readlines():
        wordList.append(i.strip())

vecList, wordList = similar(wordList)

print(len(wordList), wordList)
print(len(vecList))
points=vecList
dbscan = DBSCAN(5,10)
key,noisy = dbscan.fit(points)
print ('DBSCAN , ' , key, noisy)

'''
conclusion:
k-means聚类和AGNES层次聚类分析结果差不多的三类。
k-means对于大型数据集也是简单高效、时间复杂度、空间复杂度低。 最重要是数据集大时结果容易局部最优；需要预先设定K值，对最先的K个点选取很敏感；

DBSCAN对噪声不敏感；能发现任意形状的聚类。 但是聚类的结果与参数有很大的关系；DBSCAN用固定参数识别聚类，但当聚类的稀疏程度不同时，
相同的判定标准可能会破坏聚类的自然结构，即较稀的聚类会被划分为多个类或密度较大且离得较近的类会被合并成一个聚类。

'''










