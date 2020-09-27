#coding=utf-8


'''

Patent Abstract
use different textAbstract  classes to do abstract
the patent is "field+problem+(tech+claim)+func", and give abstracts
'''

'''
Data:
mqpat database，
fieldsIndivideBase，利用里面的四个字段组合内容中，继续抽取一个专利的abstract
制作语料：（字段组合，独立权利要求），制作几个领域的对应语料，用于后续的深度学习文本生成算法，我来准备算法；
制作语料：（test库中US和EP的专利，有对应的中文标题和英文标题，中文摘要和英文摘要，我们制作机器翻译语料），测试机器翻译算法。

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
    port = 29017
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

(conn, db, col) = v4Mongo('fieldsIndivideBase')
#(conn, db, col) = wordMongo('fieldsIndivideBase')

f= codecs.open('Abstract.txt','w',encoding='utf-8')
for data in col.find({'fieldsName':'baidu','userid':'wangnan'}).limit(200).batch_size(100):
    if 'abst' not in data:
        continue
    if data['abst'] is None or len(data['abst'])<2:
        continue
    f.write(data['abst']+'\n')
f.close()

'''
TODO
https://github.com/davidadamojr/TextRank
gensim.summarization模块实现了TextRank，

它建立在Google用于排名网页的流行PageRank算法的基础之上。TextRank的工作原理如下：
预处理文本：删除停止词并补足剩余的单词。
创建把句子作为顶点的图。
通过边缘将每个句子连接到每个其他句子。边缘的重量是两个句子的相似程度。
在图表上运行PageRank算法。
选择具有最高PageRank分数的顶点（句子）
在原始TextRank中，两个句子之间的边的权重是出现在两个句子中的单词的百分比。Gensim的TextRank使用Okapi BM25函数来查看句子的相似程度。它是Barrios等人的一篇论文的改进。

'''

def sort_words(vertex_source, edge_source, model, window=2, pagerank_config={'alpha': 0.85, }):
    """将单词按关键程度从大到小排序

    Keyword arguments:
    vertex_source   --  二维列表，子列表代表句子，子列表的元素是单词，这些单词用来构造pagerank中的节点
    edge_source     --  二维列表，子列表代表句子，子列表的元素是单词，根据单词位置关系构造pagerank中的边
    window          --  一个句子中相邻的window个单词，两两之间认为有边
    pagerank_config --  pagerank的设置
    """

    # 记录词和词的位置信息
    sorted_words = []
    word_index = {}
    index_word = {}
    _vertex_source = vertex_source
    _edge_source = edge_source
    words_number = 0
    for word_list in _vertex_source:
        for word in word_list:
            if not word in word_index:
                word_index[word] = words_number
                index_word[words_number] = word
                words_number += 1

    graph = np.zeros((words_number, words_number))

    # 图赋权
    for word_list in _edge_source:
        for w1, w2 in combine(word_list, window):
            if w1 in word_index and w2 in word_index:
                index1 = word_index[w1]
                index2 = word_index[w2]
                try:
                    similarity = model(w1, w2)
                    if similarity < 0:
                        similarity = 0
                    # print similarity
                except:
                    similarity = 0
                graph[index1][index2] = similarity
                graph[index2][index1] = similarity
    #                graph[index1][index2] = 1.0
    #                graph[index2][index1] = 1.0

    nx_graph = nx.from_numpy_matrix(graph)

    scores = nx.pagerank(nx_graph, max_iter=100, **pagerank_config)  # this is a dict
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    for index, score in sorted_scores:
        item = AttrDict(word=index_word[index], weight=score)
        sorted_words.append(item)
    return sorted_words


def filter_keywords(sort_words):
    '''
    去掉一个字个关键词
    '''
    return [ele for ele in sort_words if len(ele.word) > 3]

def sort_sentences(sentences, words, model, pagerank_config={'alpha': 0.85, }):
    """将句子按照关键程度从大到小排序

    Keyword arguments:
    sentences         --  列表，元素是句子
    words             --  二维列表，子列表和sentences中的句子对应，子列表由单词组成
    sim_func          --  计算两个句子的相似性，参数是两个由单词组成的列表
    pagerank_config   --  pagerank的设置
    """
    sorted_sentences = []
    _source = words
    sentences_num = len(_source)
    graph = np.zeros((sentences_num, sentences_num))

    for x in range(sentences_num):
        for y in range(x, sentences_num):
            similarity = get_similarity(_source[x], _source[y], model)
            graph[x, y] = similarity
            graph[y, x] = similarity
    nx_graph = nx.from_numpy_matrix(graph)
    scores = nx.pagerank(nx_graph, **pagerank_config)  # this is a dict
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    for index, score in sorted_scores:
        item = AttrDict(index=index, sentence=sentences[index], weight=score)
        sorted_sentences.append(item)

    return sorted_sentences




'''
TextTeaser将分数与每个句子相关联。该分数是从该句子中提取的特征的线性组合。TextTeaser中的特征如下：
titleFeature：文档和句子标题共有的单词数。
sentenceLength：TextTeaser的作者定义了一个常量“理想”（值为20），它表示摘要的理想长度，以表示字数。 sentenceLength计算为距此值的标准化距离。
sentencePosition：规范化的句子数（句子列表中的位置）。
keywordFrequency：词袋模型中的术语频率（删除停用词后）。
有关摘要的句子特征的更多信息，请参阅Jagadeesh等人的基于句子提取的单文档摘要。


'''





'''
https://github.com/DerwenAI/pytextrank

PyTextRank是原始TextRank算法的python实现，具有一些增强功能，例如使用词形结构而不是词干，结合词性标注和命名实体解析，从文章中提取关键短语并基于它们提取摘要句子。
除了文章的摘要，PyTextRank还从文章中提取了有意义的关键短语。PyTextRank分四个阶段工作，每个阶段将输出提供给下一个：
在第一阶段，对文档中的每个句子执行词性标注和词形还原。
在第二阶段，关键短语与其计数一起被提取，并被标准化。
通过近似句子和关键短语之间的jaccard距离来计算每个句子的分数。
根据最重要的句子和关键短语总结文档。

'''





'''
https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume22/erkan04a-html/erkan04a.html

抽象文本抽样
一种神经网络方法
Google的Textsum是一种最先进的开源抽象文本概要架构。 它可以根据前两个句子创建新闻文章的头条。
以Textsum形式的Gigaword数据集（前两个句子，头条）训练了400万对之后，这已经展示出了良好的结果。
 在训练期间，它根据文章的前两句优化了概要的可能性。 编码层和语言模块是同时训练。 为了生成概要，它搜索所有可能概要的地方，以找到给定文章的最可能的单词序列。
ROUGE-N指标
对于LexRank，Luhn和LSA方法，我们使用Sumy 摘要库来实现这些算法。我们使用ROUGE-1指标来比较所讨论的技术。
Rouge-N是模型和黄金摘要（gold summary）之间的单词N-gram度量。
具体而言，它是在模型和黄金摘要中出现的N-gram短语的计数与在黄金摘要中出现的所有N-gram短语的计数的比率。
解释它的另一种方法是作为召回值来衡量模型摘要中出现的黄金摘要中有多少N-gram。
通常对于摘要评估，只使用ROUGE-1和ROUGE-2（有时候ROUGE-3，如果我们有很长的黄金摘要和模型）指标，理由是当我们增加N时，我们增加了需要在黄金摘要和模型中完全匹配的单词短语的N-gram的长度。
例如，考虑两个语义相似的短语“apples bananas”和“bananas apples”。如果我们使用ROUGE-1，我们只考虑单词，这两个短语都是相同的。但是如果我们使用ROUGE-2，我们使用双字短语，因此“apples bananas”成为一个与“bananas apples” 不同的单一实体，导致“未命中”和较低的评价分数。
BLEU指标
BLEU指标是一种经过修改的精度形式，广泛用于机器翻译评估。
精度是黄金和模型转换/摘要中共同出现的单词数与模型摘要中单词数的比率。与ROUGE不同，BLEU通过采用加权平均值直接考虑可变长度短语 - 一元分词，二元分词，三元分词等。
实际指标只是修改精度，以避免模型的翻译/摘要包含重复的相关信息时的问题
对于一元分词和二元分词的权重[0.6,0.4]，该比率变为0.6 *（7/9）+ 0.4 *（4/8）= 0.667。

'''



