#This script tries to 

# -*- coding: utf-8 -*-
import time
from db_article_loader import db_get_populated_articles
from classification import vectorize
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

timestamp = time.time(); timestamp = timestamp - 100*24*60*60;
train_data = db_get_populated_articles(timestamp, 1000);
train_articles = [x[1] for x in train_data];
train_labels = [x[2][0] for x in train_data]


train_tfidf, vectorizer = vectorize(train_articles);

clf = MultinomialNB().fit(train_tfidf, train_labels)

test_data = train_data;
test_articles = [x[1] for x in test_data];

new_tfidf = vectorizer.transform(test_articles)

predicted = clf.predict(new_tfidf)
success = 0; total = 0;
for doc, category in zip(test_data, predicted):
	total = total+1;
	if doc[2] != None:
		if doc[2][0].lower() == category.lower():
			success = success+1;
print str(success)+' / '+str(total);
