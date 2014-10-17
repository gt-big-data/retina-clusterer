#This script tries to 

# -*- coding: utf-8 -*-
import time
from db_article_loader import db_get_articles
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from article_loader import get_articles, get_test_data


labeled_data = get_articles(0);
labeled_articles = [x[0]['text'] for x in labeled_data]
labeled_labels = [x[1] for x in labeled_data]
labels = set([x[1] for x in labeled_data]);

count_vect = CountVectorizer()
labeled_counts = count_vect.fit_transform(labeled_articles)

tfidf = TfidfTransformer()
labeled_tfidf = tfidf.fit_transform(labeled_counts)

clf = MultinomialNB().fit(labeled_tfidf, labeled_labels)

ts = time.time(); ts = ts - 100*24*60*60;
docs_new = db_get_articles(ts);

new_articles = count_vect.transform([x[1] for x in docs_new])
new_tfidf = tfidf.transform(new_articles)

predicted = clf.predict(new_tfidf)
success = 0; total = 0;
for doc, category in zip(docs_new, predicted):
	total = total+1;
	if doc[2] != None:
		# print doc[2][0].lower()+' and '+category.lower();
		if doc[2][0].lower() == category.lower():
			success = success+1;
print str(success)+' / '+str(total);
