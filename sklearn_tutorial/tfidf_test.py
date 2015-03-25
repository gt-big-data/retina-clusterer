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
trainingLabels = [x.category for x in trainingArticles]

trainingCounts = count_vect.fit_transform(trainingText)
trainingTfidf = tfidf_trans.fit_transform(trainingCounts)

vocab = count_vect.vocabulary_
vocabValue=vocab.keys()
vocabIndex=vocab.values()

tfidfArray = trainingTfidf.toarray()
article1 = tfidfArray[0]
articleCount = 0
for article in tfidfArray:
	wordIndex = 0
	myKeyword = []
	for wordTfidf in article:
		if wordTfidf > 0.1:
			thisWord = vocabValue[vocabIndex.index(wordIndex)]
			myKeyword.append(thisWord.encode('utf-8'))
		wordIndex = wordIndex + 1
	print trainingTitle[articleCount].encode('utf-8'), ": {", ", ".join(myKeyword) ,"}\n\n\n"
	articleCount = articleCount + 1
	if articleCount > 10:
		break
# print trainingCounts