# -*- coding: utf-8 -*-

# 首先导入两个模块：jieba与numpy，使用numpy这一利器的目的是利用里面的数据类型array以及对于array的范数操作函数
import jieba
import numpy as np
stopWords = [] # stopwords文件需要自己根据分词目的予以更改，我这里载入的是简单的停用词语料
f1 = open('stopwords.txt', 'r')
for line in f1:
    stopWords.append(line.strip())
    lst, counter = [], []# 此处也可导入user_dict，替换这里的add_word
    jieba.add_word(u'棉花糖', freq = 40)
    jieba.add_word(u'即化', freq = 40)
    # 原文件中，将每条待聚类语料放一行
def keyWord(filename):
    with open(filename, 'r') as f:
        for line in f:
            words = jieba.cut(line.strip(), cut_all = False)
            for word in words:
                if word.encode('utf-8') not in stopWords:
                    lst.append(word)
                    global set_# 使用set，保证提取的特征词集合没有重复
                    set_ = set(lst)# 可通过对'set_'使用for循环来查看本例中的
                    'Feature Names'
def countKeyWord(filename):
    f = open('test.txt', 'r')
    for line in f:
        lst_ = []
        global count
        count = {}
        words = jieba.cut(line.strip(), cut_all = False)
        for word in words:
            if word.encode('utf-8') not in stopWords:
                lst_.append(word)
for item_2 in set_:
    if item_2 in lst_:
        count[item_2] = lst_.count(item_2)
    else:
        count[item_2] = 0
        counter.append(count.values())
        f.close()
        #numpy中提供计算范数的函数：linalg.norm()，假如待聚类文档数量为n，最后的输出值共计(n*(n-1))/2个
def similarity(counter):
    counter_new = np.array(counter)
    global result
    result = []
    for i in range(0, len(counter_new) - 1):
        for j in range(i + 1, len(counter_new)):
            numerator = sum(list(counter_new[i] * counter_new[j]))
            denominator = np.linalg.norm(counter_new[i]) * np.linalg.norm(counter_new[j])
            # 由于余弦值的取值范围为[-1, 1]，相似度计算时一般需要将计算值归一化，最后取值范围限定在[0, 1] cos_value = 0.5 + 0.5 * (numerator / denominator) result.append([u'语料' + str(i + 1), u'语料' + str(j + 1), str(cos_value)]) return result
        def main():
            keyWord('test.txt')
            countKeyWord('test.txt')
            similarity(counter)
            for item in result:
                print item[0], item[1], item[2]
if __name__ == "__main__":main()




# import numpy as np
# D=np.array([[0,411,213,219,296,397],
#             [411,0,204,203,120,152],
#             [213,204,0,73,136,245],
#             [219,203,73,0,90,191],
#             [296,120,136,90,0,109],
#             [ 397,152,245,191,109,0]])
#
# N = D.shape[0]
# T = np.zeros((N,N))
#
# D2 = D**2
# H = np.eye(N) - 1/N
# T = -0.5*np.dot(np.dot(H,D2),H)
#
# eigVal,eigVec = np.linalg.eig(T)
# X = np.dot(eigVec[:,:2],np.diag(np.sqrt(eigVal[:2])))
#
# print('original distance','new distance')
# for i in range(N):
#     for j in range(i+1,N):
#         print(np.str(D[i,j]),' ',np.str("%.4f"%np.linalg.norm(X[i]-X[j])))