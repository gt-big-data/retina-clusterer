import os
import glob
import operator
import nltk
from nltk.corpus import stopwords


def vectorize(article_dict):
    types = []
    [types.extend(article_dict[i].keys()) for i in article_dict]
    type_set = set(types)
    vector = {type: 0 for type in type_set}
    vectorized_articles = {}
    for article in article_dict:
        article_vector = vector.copy()
        for type in article_dict[article]:
            article_vector[type] = article_dict[article][type]
        vectorized_articles[article] = article_vector
    return vectorized_articles


os.chdir("texts")
filelisting = glob.glob("*.txt")
article_dict = {}
for filename in filelisting:
    f = open(filename)
    fileName = f.name
    wordDict = {}
    badWords = set(stopwords.words('english'))
    for line in f.readlines():
        words = line.split()
        for word in words:
            if word not in badWords:
                try:
                    wordDict[word] += 1
                except KeyError:
                    wordDict[word] = 1
    article_dict[fileName] = wordDict

X = vectorize(article_dict)
import pdb; pdb.set_trace()





