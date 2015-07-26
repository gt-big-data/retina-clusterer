from db import app
import numpy as np

from StringIO import StringIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.stem.porter import PorterStemmer

def getKeywords(texts):
	# Given a list of texts, will extract the keywords for each and return that!
	# NOTICE: Don't send more than 100 articles at a time, as we can't insure heterogeneity

	count_vectUni = CountVectorizer(stop_words='english', ngram_range=(1,1)) # for unigrams
	count_vectBi = CountVectorizer(stop_words='english', ngram_range=(2,2)) # for bigrams

	tfidf_trans1 = TfidfTransformer()
	tfidf_trans2 = TfidfTransformer()

	trainingArticles = app.getTrainingSet(50, 20) # get a training set to mix up the TfIdf
	trainingText = [x.content for x in trainingArticles]

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
		splitBigramTfidf = []
		numBigram = {}
		for bigram in bigrams:
			index = bigrams.index(bigram)
			wordSplit = bigram.split()
			splitBigrams.append(wordSplit[0])
			splitBigrams.append(wordSplit[1])
			splitBigramTfidf.append(bigramScores[index])
			splitBigramTfidf.append(bigramScores[index])
			if wordSplit[0] not in numBigram: #add first word in bigram
				numBigram[wordSplit[0]] = 1
			else:
				numBigram[wordSplit[0]] += 1
			if wordSplit[1] not in numBigram: #add second word in bigram
				numBigram[wordSplit[1]] = 1
			else:
				numBigram[wordSplit[1]] += 1

		unigramsAndScores = sorted(zip(wordScores, keywords), reverse=True)
		unigramSorted = [e[1] for e in unigramsAndScores]
		unigramTfidfSorted = [e[0] for e in unigramsAndScores]

		#0 bigrams - keep unigram
		#1 bigram - compare values, keep higher
		#>1 bigram - keep unigram, keep highest bigram
		#loop thru unigrams in increasing tfidf value
		for unigram in reversed(unigramSorted): #loop through backwords
			if unigram in numBigram:
				if numBigram[unigram] == 1: # unigram appears in 1 bigram
					indexUni = unigramSorted.index(unigram)
					unigramValue = unigramTfidfSorted[indexUni]
					indexSplitBi = splitBigrams.index(unigram)
					bigramValue = splitBigramTfidf[indexSplitBi]
					if unigramValue > bigramValue:
						# delete both words of bigram
						if indexSplitBi % 2 == 0: # unigram is first word in the split
							splitBigrams.pop(indexSplitBi)
							splitBigramTfidf.pop(indexSplitBi)
							# if other word is also in bigram, update bigram numbers
							if splitBigrams[indexSplitBi] in numBigram:
								numBigram[splitBigrams[indexSplitBi]] -=1
							splitBigrams.pop(indexSplitBi)
							splitBigramTfidf.pop(indexSplitBi)
						else: # unigram is second word in the split
							splitBigrams.pop(indexSplitBi)
							splitBigramTfidf.pop(indexSplitBi)
							# if the other word is also in bigram, update bigram numbers
							if splitBigrams[indexSplitBi - 1] in numBigram:
								numBigram[splitBigrams[indexSplitBi - 1]] -= 1
							splitBigrams.pop(indexSplitBi - 1)
							splitBigramTfidf.pop(indexSplitBi - 1)
					else:
						# delete unigram
						unigramSorted.pop(indexUni)
						unigramTfidfSorted.pop(indexUni)
				elif numBigram[unigram] > 1: # unigram appears in more than 1 bigram
					highestValue = 0
					for index in range(len(splitBigrams)): #find value of highest bigram
						if splitBigrams[index] == unigram and splitBigramTfidf[index] > highestValue:
							highestValue = splitBigramTfidf[index]
					index = len(splitBigrams) - 1
					while (index >= 0): # loop through index and delete bigrams
						if splitBigrams[index] == unigram and splitBigramTfidf[index] < highestValue:
							if index % 2 == 0: # unigram is first word in the split
								splitBigrams.pop(index)
								splitBigramTfidf.pop(index)
								# if other word is also in bigram, update bigram numbers
								if splitBigrams[index] in numBigram:
									numBigram[splitBigrams[index]] -= 1
								splitBigrams.pop(index)
								splitBigramTfidf.pop(index)
							else: # unigram is second word in the split
								splitBigrams.pop(index)
								splitBigramTfidf.pop(index)
								# if other word is also in bigram, update bigram numbers
								if splitBigrams[index - 1] in numBigram:
									numBigram[splitBigrams[index - 1]] -= 1
								splitBigrams.pop(index - 1)
								splitBigramTfidf.pop(index - 1)
								index = index - 1
						index = index - 1

		# Checking for plural words using stemming
		stemmed = []
		delList = []
		stemmer = PorterStemmer()
		for item in unigramSorted:
			try:
				stemmed.append(stemmer.stem(item))
			except:
				#print "Not a word, breh"
				pass
		i = 0
		for stem in stemmed:
			j = i
			while j + 1 < len(stemmed):
				if stem == stemmed[j + 1]:
					# pray for no octopus/octopi
					if len(unigramSorted[i]) < len(unigramSorted[j+1]):
						delList.append(j+1)
					else:
						delList.append(i)
				j += 1
			i += 1
		for index in delList:
			if index in unigramSorted:
				del(unigramSorted[index])
			if index in unigramTfidfSorted:
				del(unigramTfidfSorted[index])


		# Concatenate both lists
		for index in range(len(splitBigrams)):
			if (index % 2 == 0):
				word = "".join([splitBigrams[index], " ", splitBigrams[index + 1]])
				unigramSorted.append(word)
				value = splitBigramTfidf[index]
				unigramTfidfSorted.append(value)

		keywordTfidf = zip(unigramTfidfSorted, unigramSorted)
		keywordTfidf.sort(reverse=True) # sort from most relevant to least relevant
		keywordSorted = [e[1] for e in keywordTfidf]

		keywordList.append(keywordSorted)

		articleIndex = articleIndex + 1
	return keywordList


def updateLatestArticles():
	# This will get the latest 30 articles without keywords
	# Produce a keyword list, and upload to Database
	articles = app.getArticlesNoKeywords(50)

	articlesTxt = [article.content for article in articles]
	articlesId = [article.guid for article in articles]

	articlesKeywords = getKeywords(articlesTxt)

	for articleKeywords, articleId in zip(articlesKeywords, articlesId):
		app.updateKeywords(articleId, articleKeywords)

updateLatestArticles()

# for articleKeywords, articleTitle in zip(articlesKeywords, articlesTitle):
# 	print articleTitle.encode('utf-8'), "\n ---------------------------------\n", articleKeywords, "\n\n"
