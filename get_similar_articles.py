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


def getSimilarArticles(article, numOfDays = 10, numOfNeighbors):
	articles = app.getTrainingSet(50, 0)
	neigh = KNeighborsClassifier()
	trainingText = [x.text for x in articles]
	rainingLabels = [x.categories for x in trainingArticles]

	trainingCounts = count_vect.fit_transform(trainingText)
	trainingTfidf = tfidf_trans.fit_transform(trainingCounts)

	targetCounts = count_vect.transform([article.text])
	targetTfidf = tfidf_trans.transform(targetCounts)

	neigh.fit(trainingTfidf,rainingLabels)
	neigh.kneighbors(n_neighbors=numOfNeighbors, return_distance=False)


trainingArticles = app.getTrainingSet(50, 0)