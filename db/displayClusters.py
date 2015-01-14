# -*- coding: utf-8 -*-
import time
import numpy as np
from db_article_loader import db_get_unique_categories
from classification import vectorize
from classification import cross_validation
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

print "Nb cat: ", len(unique_cat) ,"\n Succes: ", unique_cat;