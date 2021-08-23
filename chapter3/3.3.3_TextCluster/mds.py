#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@File     : mds.py
@Time     : 2021/3/25 19:49
@Author   : zhaohongyu
@Email    : zhaohongyu2401@yeah.net
@Software : PyCharm
"""


import nltk
import re
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
stemmer = SnowballStemmer("english")
import pandas as pd
def load_data_for_mds(path):
    data_set = []
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            line = line.strip()

            if '-1' in line:
                line.remove('-1')
            data_set.append(line[:])

    return data_set


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


def mds(labels, words):
    clusters = labels
    if type(words) != list:
        words = load_data_for_mds(words)
    tfidf_vectorizer = TfidfVectorizer(max_df=0.9, max_features=2000,
                                       min_df=0.01, stop_words='english',
                                       use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 3),analyzer='char')

    print('words = ', words)
    tfidf_matrix = tfidf_vectorizer.fit_transform(words)

    from sklearn.metrics.pairwise import cosine_similarity
    dist = 1 - cosine_similarity(tfidf_matrix)

    import matplotlib.pyplot as plt

    from sklearn.manifold import MDS
    # MDS()
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(dist)  # shape (n_components, n_samples)

    xs, ys = pos[:, 0], pos[:, 1]

    from nltk.tag import pos_tag

    # set up colors per clusters using a dict
    cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}

    # set up cluster names using a dict
    cluster_names = {0: 'Microelectromechanical system, artificial',
                     1: 'CNN, Network, device',
                     2: 'face recognition,  ELECTRICAL DEVICES',
                     3: 'automating shipping, interface',
                     4: 'multimedia, apparatus'}
    # %matplotlib

    # create data frame that has the result of the MDS plus the cluster numbers and titles
    print('xs   = ', len(xs))
    print('ys   = ', len(ys))
    print('cluster   = ', len(clusters))
    df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=words))

    groups = df.groupby('label')
    print(groups)

    # set up plot
    fig, ax = plt.subplots(figsize=(17, 9))  # set size
    ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling

    # iterate through groups to layer the plot
    # note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
    for name, group in groups:
        print('group = ', group)
        print('name = ', name)
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, label=cluster_names[name],
                color=cluster_colors[name],
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
        ax.text(df.loc[i]['x'], df.loc[i]['y'], df.loc[i]['title'], size=4)  # size=8

    plt.show()  # show the plot

    plt.close()
