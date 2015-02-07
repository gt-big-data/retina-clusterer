import time
from db import app
import numpy as np
import os
import supervisedTest
from StringIO import StringIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB



def test_one_article():
	test_article = raw_input('Article to be tested:')
	__test_files([test_article])

def test_all_articles():
	all_files = os.listdir('Test_Articles')
	#print all_files
	all_files.remove('ReadMe.txt')
	__test_files(all_files)


def __test_files(filenames):
	articles = []
	true_categories =[]
	for filename in filenames:
		f = open(os.path.join('Test_Articles', filename), "r")
		test_file = f.readlines()
		for line in test_file:
			if "Category" in line:
				true_categories.append(line.split(':')[1])
				break

		start = 0
		count = 0
		for line in test_file:
			if "Article" in line:
				start = count+1
				break
			count = count + 1
		articles.append(" ".join(test_file[start:-1]))
	__test_articles(filenames, articles, true_categories)

def __test_articles(filenames, articles, labels):
	print 'training...'
	testPredictedLabel = supervisedTest.static_classifier_test(articles)
	if len(filenames) != len(articles) or len(filenames) != len(articles):
		print "number of file names and articles and labels don't match"
	for i in range(0,len(filenames)):
		print '-------------------------------'
		print 'File name:', filenames[i]
		print 'True category: ', labels[i]
		print 'Predict category: ', testPredictedLabel[i]