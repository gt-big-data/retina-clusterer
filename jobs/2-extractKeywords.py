from ..db import app
import numpy as np

from StringIO import StringIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def getKeywords(texts):
	# Given a list of texts, will extract the keywords for each and return that!
	# NOTICE: Don't send more than 100 articles at a time, as we can't insure heterogeneity

	count_vectUni = CountVectorizer(stop_words='english', ngram_range=(1,1)) # for unigrams
	count_vectBi = CountVectorizer(stop_words='english', ngram_range=(2,2)) # for bigrams

	tfidf_trans1 = TfidfTransformer()
	tfidf_trans2 = TfidfTransformer()

	trainingArticles = app.getTrainingSet(50, 20) # get a training set to mix up the TfIdf
	trainingText = [x.text for x in trainingArticles]

	totalText = trainingText + texts # merge

	# training unigram and bigram TFIDF
	trainingTfidf1 = tfidf_trans1.fit_transform(count_vectUni.fit_transform(totalText))
	trainingTfidf2 = tfidf_trans2.fit_transform(count_vectBi.fit_transform(totalText))

	# extract vocab value and index. This helps link column to a word ( 13 = 'banana')
	vocabValue1 = count_vectUni.vocabulary_.keys()
	vocabIndex1 = count_vectUni.vocabulary_.values()
	vocabValue2 = count_vectBi.vocabulary_.keys()
	vocabIndex2 = count_vectBi.vocabulary_.values()

	tfidfArray1 = trainingTfidf1.toarray()
	tfidfArray2 = trainingTfidf2.toarray()

	keywordList = [] # prepare for output

	articleIndex = len(trainingText)
	while articleIndex < len(totalText):
		thisTfidfUni = tfidfArray1[articleIndex]
		thisTfidfBi = tfidfArray2[articleIndex]
		i = 0
		keywords = []
		wordScores = []
		for wordTfidf in thisTfidfUni:
			if wordTfidf > 0.15:
				thisWord = vocabValue1[vocabIndex1.index(i)].encode('utf-8')
				keywords.append(thisWord)
				wordScores.append(wordTfidf)
			i = i + 1
		wordIndex2 = 0
		bigrams = []
		bigramScores = []
		for wordTfidf2 in thisTfidfBi:
			if wordTfidf2 > 0.15:
				thisBigram = vocabValue2[vocabIndex2.index(wordIndex2)].encode('utf-8')
				bigrams.append(thisBigram)
				bigramScores.append(wordTfidf2)
			wordIndex2 = wordIndex2 + 1

		splitBigrams = []
		for bigram in bigrams:
			wordSplit = bigram.split()
			splitBigrams.append(wordSplit[0])
			splitBigrams.append(wordSplit[1])

		for word in splitBigrams: # we remove bigram words from potential unigrams
			if word in keywords:
				index = keywords.index(word)
				keywords.pop(index)
				wordScores.pop(index)

		# Concatenate both lists
		keywords = keywords + bigrams 
		wordScores = wordScores + bigramScores

		keyWordTfidf = zip(wordScores, keywords)
		keyWordTfidf.sort(reverse=True) # sort from most relevant to least relevant
		keyWordSorted = [keyword for score, keyword in keyWordTfidf]
		
		keywordList.append(keyWordSorted)

		articleIndex = articleIndex + 1
	return keywordList

def updateLatestArticles():
	# This will get the latest 30 articles without keywords
	# Produce a keyword list, and upload to Database
	articles = app.getArticlesNoKeywords(30)
	articlesTxt = [article.text for article in articles]
	articlesId = [article.id for article in articles]
	articlesKeywords = getKeywords(articlesTxt)
	for articleKeywords, articleId in zip(articlesKeywords, articlesId):
		app.updateKeywords(articleId, articleKeywords)


updateLatestArticles()

# articles = app.getLatestCluster('Technology', 10, 0)
# articlesTitle = [article.title for article in articles]
# articlesTxt = [article.text for article in articles]
# articlesKeywords = getKeywords(articlesTxt)

# for articleKeywords, articleTitle in zip(articlesKeywords, articlesTitle):
# 	print articleTitle.encode('utf-8'), "\n ---------------------------------\n", articleKeywords, "\n\n"