#encoding=utf-8
import os
from nltk.parse import stanford
import nltk
from nltk.tree import Tree
import jieba 
#jieba.load_userdict('unionDict.txt')
import time
from nltk.tokenize.stanford import StanfordTokenizer
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import jieba.posseg as pseg
os.environ['STANFORD_PARSER'] = 'D:\stanford\stanford-parser-full-2017-06-09\jars\stanford-parser.jar'
os.environ['STANFORD_MODELS'] = 'D:\stanford\stanford-parser-full-2017-06-09\jars\stanford-parser-3.8.0-models.jar'
# os.environ['STANFORD_PARSER'] = 'stanford-parser.jar'
# os.environ['STANFORD_MODELS'] = 'stanford-parser-3.8.0-models.jar'

rule2 = ['NNNN', 'NNNP','NPNN','NPNP','VVNN','JJNN','VANN','VVNP','JJNP','VANP']

rule3 = ['NNNNNN','NNNNNP','NNNPNP','NNNPNN','NPNPNP','NPNNNN','NPNNNP','NPNPNN', \
         'NNVVNN','NNVVNP','NPVVNP','NPVVNN',\
         'NNVANN','NNVANP','NPVANP','NPVVNN',\
         'NNJJNN','NNJJNP','NPJJNP','NPVVNN',\
         'VVNNNN','VVNNNP','VVNPNP','VVNPNN',\
         'JJNNNN','JJNNNP','JJNPNP','JJNPNN',\
         'VANNNN','VANNNP','VANPNP','VANPNN']

#text = "I saw a dog chasing a cat."

begin = time.time()
#patFile = open('PatResultAInew1.txt','r')
dict = {}
parser = stanford.StanfordParser( model_path="chinesePCFG.ser.gz" )
text = ['对车型训练数据进行学习从而生成车型模型， 判别的准确率上得以提升。',\
        '提高数据采集的效率， 本发明可以基于人工智能机器学习的方式']
test = '(S1(S(NP He)(VP(VP killed(NP theman)(PP with(NP aknife))) and(VP murdered(NP him)(PP with(NP a dagger)))).))'
n = parser._make_tree(test)
print (n)
for line in text:
    words = jieba.cut(line)
    content = ' '.join(words)
     
    #print (content)
     
    #tem = nltk.sent_tokenize(content)
    sentences = parser.raw_parse_sents([content],verbose=True) # nltk.sent_tokenize(text), verbose=True
    #print( type( sentences ) )
    paser_tree = None
    #sentences.draw()
    wordList = []
    flagList = []
    tem = ''
    for line in sentences:
        for sentence in line:
            #print'tpye = ',( type( sentence ) )
            print (sentence)
            parser_tree = sentence
            parser_tree.draw()
            for s in sentence.subtrees(lambda t:t.height()==2):
                if len(s.leaves())<1:
                    continue
                flag = s.label()
                word = s.leaves()[0]
                wordList.append(word)
                flagList.append(flag)
                # print (word)
                # print (flag)
                

end = time.time()

print (end-begin)     
#print parser_tree['VP']



