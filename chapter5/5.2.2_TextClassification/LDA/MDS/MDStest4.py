# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import pandas as pd
import nltk
from bs4 import BeautifulSoup
import re
import os
import codecs
from sklearn import feature_extraction
#import mpld3
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import pylab
pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']
pylab.mpl.rcParams['axes.unicode_minus'] = False
# import jieba
# import jieba.posseg as pseg
# jieba.load_userdict('mergeWord.txt')
#
# f = codecs.open('remodifynew.txt','r',encoding = 'utf-8')
# ff = codecs.open('remodifynew1.txt','w',encoding = 'utf-8')
# theme = []
#
# for line in f.readlines():
#     result = jieba.posseg.cut(line)
#     for word, flag in result:
#       theme.append(result.word)
# for w in theme:
#   print (w)
# print (len(theme))
# print("\n" + "="*40)
from lineModifyTool import lineModify


synopses = []
titles = []
ChineseTest = open('ChineseTech1.txt')
#====================================================================================
count = 0
for line in ChineseTest:
    line = lineModify(line)
    head = line[:2]
    body = line[2:]
    if head == '#*':
        titles.append(body.decode('utf-8'))
    if head == '#!':
        synopses.append(body.decode('utf-8'))
    if count == 100:
        break
titles = titles[:100]
synopses = synopses[:100]
#========================================================================================
# synopses_imdb = open('XmltestAbst.txt').read().split('\n BREAKS HERE') #synopses_list_imdb.txt
#  
# synopses_imdb = synopses_imdb[:100]
# print (synopses_imdb)
#  
#  
#  
# synopses_clean_imdb = []
#  
# for text in synopses_imdb:
#     text = BeautifulSoup(text, 'html.parser').getText()
#     #strips html formatting and converts to unicode
#     synopses_clean_imdb.append(text)
#  
# synopses_imdb = synopses_clean_imdb
#    
# synopses = []
# synopses_wiki = synopses_imdb
# # 
#  
# for i in range(len(synopses_wiki)):
#     item = synopses_wiki[i] + synopses_imdb[i]
#     synopses.append(item)
# print ('sy   = ',len(synopses))
# #generates index for each item in the corpora (in this case it's just rank) and I'll use this for scoring later
# ranks = []
# titles = open('Xmltest.txt').read().split('\n')
# titles = titles[:100]
#  
# #print ('title = ',titles)
# print ('title   = ',len(titles)) 
# for i in range(0,len(titles)):
#     ranks.append(i)
# print ('ranks   = ',len(ranks))
# #load nltk's English stopwords as variable called 'stopwords'
#========================================================================================================
#stopwords = nltk.corpus.stopwords.words('english')

# load nltk's SnowballStemmer as variabled 'stemmer'
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

# here I define a tokenizer and stemmer which returns the set of stems in the text that it is passed

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


totalvocab_stemmed = []
totalvocab_tokenized = []
for i in synopses:
    allwords_stemmed = tokenize_and_stem(i)
    totalvocab_stemmed.extend(allwords_stemmed)

    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer(max_df=0.9, max_features=2000,
                                 min_df=0.01, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

#%time
tfidf_matrix = tfidf_vectorizer.fit_transform(synopses)

print(tfidf_matrix.shape)
terms = tfidf_vectorizer.get_feature_names()


from sklearn.metrics.pairwise import cosine_similarity
dist = 1 - cosine_similarity(tfidf_matrix)
from sklearn.cluster import KMeans

num_clusters = 10

km = KMeans(n_clusters=num_clusters)

#%time
km.fit(tfidf_matrix)

clusters = km.labels_.tolist()
from sklearn.externals import joblib

#joblib.dump(km,  'doc_cluster.pkl')
km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()


print("多维向量分析MDS结果:")
print()

import os  # for os.path.basename
import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn.manifold import MDS
MDS()

# two components as we're plotting points in a two-dimensional plane
# "precomputed" because we provide a distance matrix
# we will also specify `random_state` so the plot is reproducible.
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

pos = mds.fit_transform(dist)  # shape (n_components, n_samples)

xs, ys = pos[:, 0], pos[:, 1]

#strip any proper nouns (NNP) or plural proper nouns (NNPS) from a text
from nltk.tag import pos_tag

def strip_proppers_POS(text):
    tagged = pos_tag(text.split()) #use NLTK's part of speech tagger
    non_propernouns = [word for word,pos in tagged if pos != 'NNP' and pos != 'NNPS']
    return non_propernouns

#set up colors per clusters using a dict
cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}

#set up cluster names using a dict
cluster_names = {0: 'Microelectromechanical system, artificial',
                 1: 'CNN, Network, device',
                 2: 'face recognition,  ELECTRICAL DEVICES',
                 3: 'automating shipping, interface',
                 4: 'multimedia, apparatus'}
#%matplotlib

# create data frame that has the result of the MDS plus the cluster numbers and titles
print ('xs   = ',len(xs))
print ('ys   = ',len(ys))
print ('cluster   = ',len(clusters))
df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=titles))



# group by cluster
groups = df.groupby('label')
print (groups)

# set up plot
fig, ax = plt.subplots(figsize=(17, 9))  # set size
ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling

# iterate through groups to layer the plot
# note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
for name, group in groups:
    print ('group = ',group)
    print ('name = ',name)
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, label=cluster_names[name], color=cluster_colors[name],
            mec='none')
    ax.set_aspect('auto')
    ax.tick_params( \
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom='off',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        labelbottom='off')
    ax.tick_params( \
        axis='y',  # changes apply to the y-axis
        which='both',  # both major and minor ticks are affected
        left='off',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        labelleft='off')

ax.legend(numpoints=1)  # show legend with only 1 point

# add label in x,y position with the label as the film title
for i in range(len(df)):
    ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=4) #size=8

plt.show()  # show the plot

# uncomment the below to save the plot if need be
# plt.savefig('clusters_small_noaxes.png', dpi=200)
plt.close()
#
from scipy.cluster.hierarchy import ward, dendrogram

linkage_matrix = ward(dist) #define the linkage_matrix using ward clustering pre-computed distances

fig, ax = plt.subplots(figsize=(100, 50)) # set size
ax = dendrogram(linkage_matrix, orientation="right", labels=titles);

plt.tick_params(\
    axis= 'x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')

plt.tight_layout() #show plot with tight layout

#uncomment below to save figure
plt.savefig('ward_clusters.png', dpi=200) #save figure as ward_clusters
plt.close()
