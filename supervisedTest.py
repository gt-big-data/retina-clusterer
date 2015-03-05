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
from sklearn.svm import SVC



def static_classifier_test(testText):
	count_vect = CountVectorizer(stop_words='english') #initialize the vectorizer
	tfidf_trans = TfidfTransformer() #initialize our tfidf transformer

	trainingArticles = app.getTrainingSet(40, 0) # get the latest 50 articles
	trainingText = [x.text for x in trainingArticles]
	trainingLabels = [x.categories for x in trainingArticles]

	trainingCounts = count_vect.fit_transform(trainingText)
	trainingTfidf = tfidf_trans.fit_transform(trainingCounts)

	testCounts = count_vect.transform(testText)
	testTfidf = tfidf_trans.transform(testCounts)

	clf = SVC(kernel = 'linear').fit(trainingTfidf, trainingLabels) # train classifier

	return clf.predict(testTfidf)

testArticles = app.getTrainingSet(50, 40) # get the 51->100 latest articles
testText = [x.text for x in testArticles]
testTrueLabels = [x.categories for x in testArticles]
testPredictedLabels = static_classifier_test(testText)
right = 0;
for truth, predicted in zip(testPredictedLabels, testTrueLabels):
	if truth == predicted:
		right += 1
print "Accuracy: ", str(100*float(right) / float(len(testTrueLabels))), "% (On ", str(len(testTrueLabels)), "new articles)"


