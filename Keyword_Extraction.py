# -*- coding: utf-8 -*-
import time
from db import app
import numpy as np

from StringIO import StringIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

count_vect1 = CountVectorizer(stop_words='english', ngram_range=(1,1))
count_vect2 = CountVectorizer(stop_words='english', ngram_range=(2,2))

tfidf_trans1 = TfidfTransformer()
tfidf_trans2 = TfidfTransformer()

trainingArticles = app.getTrainingSet(50, 0)
trainingTitle = [x.title for x in trainingArticles]
trainingText = [x.text for x in trainingArticles]
trainingLabels = [x.category for x in trainingArticles]

trainingCounts1 = count_vect1.fit_transform(trainingText)
trainingCounts2 = count_vect2.fit_transform(trainingText)
trainingTfidf1 = tfidf_trans1.fit_transform(trainingCounts1)
trainingTfidf2 = tfidf_trans2.fit_transform(trainingCounts2)

vocab1 = count_vect1.vocabulary_
vocabValue1=vocab1.keys()
vocabIndex1=vocab1.values()
vocab2 = count_vect2.vocabulary_
vocabValue2=vocab2.keys()
vocabIndex2=vocab2.values()


tfidfArray1 = trainingTfidf1.toarray()
tfidfArray2 = trainingTfidf2.toarray()

articleCount = 0

while articleCount < 10:
	article1 = tfidfArray1[articleCount]
	article2 = tfidfArray2[articleCount]
	wordIndex1 = 0
	myKeyword1 = []
	for wordTfidf1 in article1:
		if wordTfidf1 > 0.1:
			thisWord = vocabValue1[vocabIndex1.index(wordIndex1)]
			myKeyword1.append(thisWord.encode('utf-8'))
		wordIndex1 = wordIndex1 + 1
	print trainingTitle[articleCount].encode('utf-8'), ": {", ", ".join(myKeyword1) ,"}\n"
	wordIndex2 = 0
	myKeyword2 = []
	for wordTfidf2 in article2:
		if wordTfidf2 > 0.1:
			thisWord = vocabValue2[vocabIndex2.index(wordIndex2)]
			myKeyword2.append(thisWord.encode('utf-8'))
		wordIndex2 = wordIndex2 + 1
	print "{", ", ".join(myKeyword2) ,"}\n\n\n\n"
	
	articleCount = articleCount + 1
	#if articleCount > 10:
	#	break
# print trainingCounts1