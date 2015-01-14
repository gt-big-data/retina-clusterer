from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import time
from db import app
from db_article_loader import db_get_populated_articles
from classification import vectorize
from cluster_name import cluster_name
from collections import defaultdict
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB

from bson.objectid import ObjectId

# This function should be ran every 4 hours in the future (!)
new_articles = db_get_populated_articles(ts = time.time() - 4 * 3600) # last four hours
training_set = db_get_populated_articles(ts = time.time() - 3 * 86400) # last 3 days
training_articles = []
training_labels = []

for article in training_set:
    cleanCat = cluster_name(article[2][0]);
    if cleanCat != '':
        training_articles.append(article[1]);
        training_labels.append(cleanCat);

training_tfidf, vectorizer = vectorize(training_articles);
clf = DecisionTreeClassifier(max_depth=4) # clf = MultinomialNB();
clf.fit(training_tfidf.toarray(), training_labels)

unlabeled_articles = [];
unlabeled_texts = [];


cleanCategoriesDict = defaultdict(list) #Maps a clean category to a list of articleIDs

for article in new_articles:
    cleanCategory = cluster_name(article[2][0])
    if cleanCategory != '': # a category was already detected
        cleanCategoriesDict[cleanCategory].append(article.id) #Add the article ID
    else: # no category was matched, we will run it through the clustering afterwards
        unlabeled_articles.append(article);
        unlabeled_texts.append(article.text);

unlabeled_tfidf = vectorizer.transform(unlabeled_texts);

predicted_labels = clf.predict(unlabeled_tfidf.toarray());

for new_cat, article in zip(predicted_labels, unlabeled_articles):
    if getattr(article, 'id', None) != None:
        cleanCategoriesDict[new_cat].append(article.id);
    else:
        print article

# append to the database    
for cleanCategory in cleanCategoriesDict.keys():
    articleIDs = cleanCategoriesDict[cleanCategory]
    if not all(type(_id) == ObjectId for _id in articleIDs):
        print articleIDs
    else:
        app.insertToCluster(articleIDs, cleanCategory)