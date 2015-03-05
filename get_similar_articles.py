import time
from db import app
import numpy as np
from StringIO import StringIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC


def getSimilarArticles(article, numOfDays, numOfNeighbors):
	articles = app.getTrainingSet(40, 1)
	neigh = KNeighborsClassifier()
	count_vect = CountVectorizer(stop_words='english')
	tfidf_trans = TfidfTransformer()
	trainingText = [x.text for x in articles]
	rainingLabels = [x.categories for x in articles]

	trainingCounts = count_vect.fit_transform(trainingText)
	trainingTfidf = tfidf_trans.fit_transform(trainingCounts)

	targetCounts = count_vect.transform([article.text])
	targetTfidf = tfidf_trans.transform(targetCounts)

	neigh.fit(trainingTfidf,rainingLabels)
	similar_articles_tfidf = neigh.kneighbors(targetTfidf, numOfNeighbors, False)
	similar_articles = []
	for index in similar_articles_tfidf[0]:
		similar_articles.append(articles[index].title)
	return similar_articles


trainingArticles = app.getTrainingSet(1, 0)
target = trainingArticles[4]
print target.title

similar_articles = getSimilarArticles(target, 10, 4)
for article in similar_articles:
	print article