from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import time
from db import app
from db_article_loader import db_get_populated_articles
from classification import vectorize
from cluster_name import cluster_name
from collections import defaultdict
from sklearn.tree import DecisionTreeClassifier


# This function should be ran every 4 hours in the future (!)
all_articles = db_get_populated_articles(ts = time.time() - 4 * 3600)
training_set = db_get_populated_articles(ts = time.time() - 3 * 86400)
training_articles = [];
training_labels = []

for article in training_set:
    cleanCat = cluster_name(article[2][0]);
    if cleanCat != '':
        training_articles.push(article[1]);
        training_labels.push(cleanCat);

training_tfidf, vectorizer = vectorize(training_articles);
clf = DecisionTreeClassifier(max_depth=4).fit(training_tfidf, training_labels)

unlabeled_articles = [];


cleanCategoriesDict = defaultdict(list) #Maps a clean category to a list of articleIDs
for article in all_articles:
    cleanCategory = cluster_name(article[2][0])
    if cleanCategory != '':
        cleanCategoriesDict[cleanCategory].append(article[3]) #Add the article ID
    else:
        unlabeled_articles.push(article);

unlabeled_tfidf = vectorizer.transform(unlabeled_articles);

predicted_labels = clf.predict(unlabeled_tfidf);

for new_cat, article in zip(predicted_labels, unlabeled_articles):
    cleanCategoriesDict[new_cat].append(article[3]);



    
for cleanCategory in cleanCategoriesDict.keys():
    articleIDs = cleanCategoriesDict[cleanCategory]
    app.insertToCluster(articleIDs, cleanCategory)