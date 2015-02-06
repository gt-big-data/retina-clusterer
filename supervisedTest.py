# -*- coding: utf-8 -*-
import time
from db import app
import numpy as np
from StringIO import StringIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB

count_vect = CountVectorizer() #initialize the vectorizer
tfidf_trans = TfidfTransformer() #initialize our tfidf transformer

trainingArticles = app.getTrainingSet(50, 0) # get the latest 50 articles
trainingText = [x.text for x in trainingArticles]
trainingLabels = [x.categories for x in trainingArticles]

trainingCounts = count_vect.fit_transform(trainingText)
trainingTfidf = tfidf_trans.fit_transform(trainingCounts)

testArticles = app.getTrainingSet(50, 50) # get the 51->100 latest articles
testText = [x.text for x in testArticles]
testTrueLabels = [x.categories for x in testArticles]

testCounts = count_vect.transform(testText)
testTfidf = tfidf_trans.transform(testCounts)

#PHASE2: Classification

clf = MultinomialNB()
# clf = DecisionTreeClassifier(max_depth=7)
# clf = KNeighborsClassifier(20)
clf.fit(trainingTfidf.toarray(), trainingLabels) # train classifier
testPredictedLabels = clf.predict(testTfidf.toarray())

right = 0;
for truth, predicted in zip(testPredictedLabels, testTrueLabels):
	if truth == predicted:
		right += 1


print "Accuracy: ", str(100*float(right) / float(len(testTrueLabels))), "% (On ", str(len(testTrueLabels)), "new articles)"