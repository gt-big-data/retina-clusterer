# -*- coding: utf-8 -*-
import time
import numpy as np
from db_article_loader import db_get_populated_articles
from classification import vectorize
from classification import cross_validation
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA
from sklearn import svm

#Testing various classifiers with the data

classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    SVC(gamma=2, C=1),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    AdaBoostClassifier(),
    GaussianNB(),
    LDA(),
    MultinomialNB()]

timestamp = time.time(); timestamp = timestamp - 100*24*60*60;
test_data = db_get_populated_articles(timestamp, 1000);

test_articles = [x[1] for x in test_data];
test_labels = [x[2][0] for x in test_data];

test_tfidf, vectorizer = vectorize(test_articles);


#x of 4 runs best with 61.4%
for x in range(1, 8):
    clf = DecisionTreeClassifier(max_depth=x)
    print "Success: ", cross_validation(clf, test_tfidf, test_labels, 10);


'''
for classifier in classifiers:
    print classifier
    clf = classifier
    print "Success: ", cross_validation(clf, test_tfidf, test_labels, 10);
'''