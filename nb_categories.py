# -*- coding: utf-8 -*-
import time
import numpy as np
from db_article_loader import db_get_unique_categories
from classification import vectorize
from classification import cross_validation
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from article_loader import get_articles, get_test_data

timestamp = time.time(); timestamp = timestamp - 100*24*60*60;
unique_cat = db_get_unique_categories(timestamp);

print "Nb cat: ", len(unique_cat) ,"\n Succes: ", unique_cat;