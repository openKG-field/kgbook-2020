#!/usr/bin/env python
# _*_coding:utf-8_*_
"""
@File    : MDStest4.py
@Time    : 2021/3/19 10:19
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""
from __future__ import print_function
import numpy as np
import pandas as pd
import nltk

import re

#import mpld3
import pylab
pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']
pylab.mpl.rcParams['axes.unicode_minus'] = False

from lineModifyTool import lineModify

def load_data():

    synopses = []
    titles = []
    ChineseTest = open('wurenji.txt','r',encoding='utf8')
    count = 0
    for line in ChineseTest:
        line = lineModify(line)
        head = line[:2]
        body = line[2:]
        if head == '#*':
            titles.append(body)
        if head == '#!':
            synopses.append(body)
        titles.append(line[:])
        synopses.append(line[:])
        if count == 30:
            break
    titles = titles[:30]

    synopses = synopses[:30]
    return titles,synopses


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


# totalvocab_stemmed = []
# totalvocab_tokenized = []
# for i in synopses:
#     allwords_stemmed = tokenize_and_stem(i)
#     totalvocab_stemmed.extend(allwords_stemmed)
#
#     allwords_tokenized = tokenize_only(i)
#     totalvocab_tokenized.extend(allwords_tokenized)


from sklearn.feature_extraction.text import TfidfVectorizer


def mds_ana():
    titles,synopses = load_data()
    tfidf_vectorizer = TfidfVectorizer(max_df=0.9, max_features=2000,
                                     min_df=0.01, stop_words='english',
                                     use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

    #%time

    print('synopses = ',synopses)


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

    print('#####',clusters)
    import joblib

    joblib.dump(km,  'doc_cluster.pkl')
    km = joblib.load('doc_cluster.pkl')
    clusters = km.labels_.tolist()


    print("多维向量分析MDS结果:")
    print()

    import os  # for os.path.basename
    import matplotlib.pyplot as plt
    import matplotlib as mpl

    from sklearn.manifold import MDS
    MDS()

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
        ax.text(df.loc[i]['x'], df.loc[i]['y'], df.loc[i]['title'], size=4) #size=8

    plt.show()  # show the plot

    # uncomment the below to save the plot if need be
    # plt.savefig('clusters_small_noaxes.png', dpi=200)
    plt.close()
    #
    from scipy.cluster.hierarchy import ward, dendrogram

    linkage_matrix = ward(dist) #define the linkage_matrix using ward clustering pre-computed distances

    fig, ax = plt.subplots(figsize=(20, 50)) # set size
    ax = dendrogram(linkage_matrix, orientation="right", labels=titles);

    plt.tick_params(\
        axis= 'x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')

    plt.tight_layout() #show plot with tight layout

    #uncomment below to save figure
    plt.savefig('word_clusters.png', dpi=200) #save figure as ward_clusters
    plt.close()

mds_ana()