# -*- coding: utf-8 -*-
import time
from db import app
import numpy as np

from StringIO import StringIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

count_vect = CountVectorizer(stop_words='english') #initialize the vectorizer
tfidf_trans = TfidfTransformer() #initialize our tfidf transformer

trainingArticles = app.getTrainingSet(50, 0) # get the latest 50 articles
trainingTitle = [x.title for x in trainingArticles]
trainingText = [x.text for x in trainingArticles]
trainingLabels = [x.categories for x in trainingArticles]

trainingCounts = count_vect.fit_transform(trainingText)
trainingTfidf = tfidf_trans.fit_transform(trainingCounts)

vocab = count_vect.vocabulary_
vocabValue=vocab.keys()
vocabIndex=vocab.values()

print trainingTitle[0]
tfidfArray = trainingTfidf.toarray()
article1 = tfidfArray[0]
wordIndex = 0
for wordTfidf in article1:
	if wordTfidf > 0.1:
		thisWord = vocabValue[vocabIndex.index(wordIndex)]
		print thisWord, ": ", wordTfidf
	wordIndex = wordIndex + 1
# print trainingCounts