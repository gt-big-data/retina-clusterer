# -*- coding: utf-8 -*-
import time
import numpy as np
from db import app
from classification import vectorize
from classification import cross_validation
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from article_loader import get_articles, get_test_data

timestamp = time.time(); timestamp = timestamp - 100*24*60*60;
test_data = app.getArticlesCount(timestamp, 1000);

test_articles = [x.text for x in test_data];
test_labels = [x.category for x in test_data];

test_tfidf, vectorizer = vectorize(test_articles);

clf = MultinomialNB();

print "Succes: ", cross_validation(clf, test_tfidf, test_labels, 5);