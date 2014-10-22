#This script tries to 

# -*- coding: utf-8 -*-
import time
from db_article_loader import db_get_articles
from classification import vectorize
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from article_loader import get_articles, get_test_data


labeled_data = get_articles(1);
labeled_articles = [x[0]['text'] for x in labeled_data]
labeled_labels = [x[1] for x in labeled_data]
labels = set([x[1] for x in labeled_data]);

labeled_tfidf, vectorizer = vectorize(labeled_articles);

clf = MultinomialNB().fit(labeled_tfidf, labeled_labels)

ts = time.time(); ts = ts - 100*24*60*60;
docs_new = db_get_articles(ts);

new_tfidf = vectorizer.transform([x[1] for x in docs_new])

predicted = clf.predict(new_tfidf)
success = 0; total = 0;
for doc, category in zip(docs_new, predicted):
	total = total+1;
	if doc[2] != None:
		if doc[2][0].lower() == category.lower():
			success = success+1;
print str(success)+' / '+str(total);
