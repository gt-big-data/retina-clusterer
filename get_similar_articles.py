import time
from db import app
import numpy as np
from StringIO import StringIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.neighbors import KNeighborsClassifier


def getSimilarArticles(article, numOfDays, numOfNeighbors):
    articles = app.getTrainingSet(100, 1)
    neigh = KNeighborsClassifier()
    count_vect = CountVectorizer(stop_words='english')
    tfidf_trans = TfidfTransformer()
    trainingTitle = [x.title for x in articles]
    trainingLabels = [x.categories for x in articles]
    targetTitleCounts = count_vect.fit_transform([article.title])
    targetCounts = count_vect.transform([article.text])
    trainingCounts = count_vect.transform(trainingTitle)

    neigh.fit(trainingCounts, trainingLabels)
    similar_articles_index = neigh.kneighbors(targetCounts, numOfNeighbors, False)
    similar_articles = []
    for index in similar_articles_index[0]:
        similar_articles.append(articles[index].title)
    return similar_articles


trainingArticles = app.getTrainingSet(1, 0)
target = trainingArticles[7]
print 'Target article title:'

print target.title
print '--------------------------------------'
similar_articles = getSimilarArticles(target, 10, 10)
print "Similar articles' title:"
for article in similar_articles:
    print article