#参考下面的说明补充改写textRank

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