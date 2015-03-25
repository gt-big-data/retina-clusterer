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
	myTfidf1 = []
	for wordTfidf1 in article1:
		if wordTfidf1 > 0.15:
			thisWord = vocabValue1[vocabIndex1.index(wordIndex1)]
			myKeyword1.append(thisWord.encode('utf-8'))
			myTfidf1.append(wordTfidf1)
			#print (thisWord, " ", wordTfidf1)
		wordIndex1 = wordIndex1 + 1
	#print trainingTitle[articleCount].encode('utf-8'), ": {", ", ".join(myKeyword1) ,"}\n"
	wordIndex2 = 0
	myKeyword2 = []
	myTfidf2 = []
	for wordTfidf2 in article2:
		if wordTfidf2 > 0.15:
			thisWord = vocabValue2[vocabIndex2.index(wordIndex2)]
			myKeyword2.append(thisWord.encode('utf-8', errors='replace'))
			myTfidf2.append(wordTfidf2)
		wordIndex2 = wordIndex2 + 1
	splitBigrams = []
	for bigram in myKeyword2:
		wordSplit = bigram.split()
		splitBigrams.append(wordSplit[0])
		splitBigrams.append(wordSplit[1])
	for word in splitBigrams:
		if word in myKeyword1:
			index = myKeyword1.index(word)
			myKeyword1.pop(index)
			myTfidf1.pop(index)
	for bigram in myKeyword2:
		myKeyword1.append(bigram)
	for tfidf in myTfidf2:
		myTfidf1.append(tfidf)
	keyWordTfidf = zip(myTfidf1, myKeyword1)
	keyWordTfidf.sort(reverse=True)
	keyWordSorted = [keyword for tfidf, keyword in keyWordTfidf]
	print trainingTitle[articleCount]
	print keyWordSorted
	print "\n"
	articleCount = articleCount + 1