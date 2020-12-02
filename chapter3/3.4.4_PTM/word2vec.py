#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from gensim.models import word2vec
import codecs
import jieba

def initTrain(filename, modelname):
    sentences = word2vec.LineSentence(filename)
    model = word2vec.Word2Vec(sentences, size=20, window=5, min_count=5, workers=4)
    model.save(modelname)

def initText(text_path):
    a = codecs.open(text_path, 'r', encoding='utf-8')
    lines = a.readlines()
    idAndword = {}
    for line in lines:
        line = line.replace("\r\n", "")
        techWord_list = []
        if 'pubid' in line:
            pubid = line.replace("pubid : ", "")
        elif 'techWord' in line:
            tmp = ""
            techWord = line.replace("techWord : ", "")
            for t in techWord:
                if t != " ":
                    tmp += t
                elif t == " ":
                    t_list = jieba.cut(tmp, HMM=True)
                    for c in t_list:
                        techWord_list.append(c)
                    tmp = ""
            if tmp != '':
                t_list = jieba.cut(tmp, HMM=True)
                for c in t_list:
                    techWord_list.append(c)
        idAndword[pubid] = techWord_list
    #print(idAndword)
    return idAndword

def modelTest(modelname, word_dict, word_list, idAndword):
    word_dict = word_dict
    idAndword = idAndword
    word_list = word_list
    score_dict = {} #每个专利相似度字典
    model = word2vec.Word2Vec.load(modelname)
    for word in word_list:    #五个类别依次遍历
        for key in idAndword:#遍历所有专利
            tmp_list = idAndword[key]#获取专利techWord
            length = len(tmp_list)#techWord个数
            if length ==0:
               continue
            similar = 0 #关联度
            for tmp in tmp_list:
                try:
                    similar += model.similarity(tmp, word)
                except KeyError:
                    if length != 1:
                        length -= 1
                        
                    else:
                        length = 1
            similar = similar/length
            score_dict[key] = similar
        score_dict = dict(sorted(score_dict.items(), key=lambda x:x[1], reverse=True))
        get_len = len(score_dict)*0.2
        id_list = []
        flag = 0
        for s in score_dict:
            if flag < get_len:
                id_list.append(s)
                flag += 1
        word_dict[word] = id_list
    tmp_list = []
    other_list = []
    similar_list=[]
    for key in word_dict:
        tmp_list += word_dict[key]
    for key in idAndword:
        if key not in tmp_list:
            other_list.append(key)
    f = codecs.open('result.txt', 'w', encoding='utf-8')
    for key in word_dict:
        f.write("主题名称：" + key + "\r\n")
        f.write("相似词：")
        try:
        	similar_list = model.similar_by_word(key)
        except KeyError:
                 print ('a keyerror')
        for k in similar_list:
            f.write(k[0] + "；")
        f.write("\r\n")
        f.write("专利列表：")
        for n in word_dict[key]:
            f.write(n + "；")
        f.write("\r\n")
    f.write("其他：")
    for other in other_list:
        f.write(other + "；")
    f.close()

if __name__ == '__main__':
    #filename = "data/base.txt"
    #modelname = "data/model.model"
    idAndword = {}
    word_dict = {'移动支付': [], '数据处理': [], '智能穿戴设备': [], '手环': []}
    word_list = ['移动支付', '数据处理', '智能穿戴设备', '手环']
    text_path = "lakala.txt"
    modelname = "wc.model"
    #initTrain(filename, modelname)

    idAndword = initText(text_path)
    modelTest(modelname, word_dict, word_list, idAndword)
    print("ok")