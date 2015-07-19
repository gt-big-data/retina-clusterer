from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import time
from ..db import app
from ..article import *
from ..classification import vectorize
from ..cluster_name import cluster_name
from collections import defaultdict
from sklearn.naive_bayes import MultinomialNB
from ..supervisedTest import static_classifier_test
from bson.objectid import ObjectId
from sklearn.svm import SVC

new_articles = app.getArticlesByTimeStamp(time.time() - 4 * 3600) # last four hours
print len(new_articles)
unlabeled_articles = [];
unlabeled_texts = [];

cleanCategoriesDict = defaultdict(list) #Maps a clean category to a list of articleIDs

for article in new_articles:
    cleanCategory = cluster_name(article.category)
    if article.text is not None:
        if cleanCategory != '': # a category was already detected
            cleanCategoriesDict[cleanCategory].append(article.id) #Add the article ID

        else: # no category was matched, we will run it through the clustering afterwards
            unlabeled_articles.append(article);
            unlabeled_texts.append(article.text);

predicted_labels = static_classifier_test(unlabeled_texts)

for new_cat, article in zip(predicted_labels, unlabeled_articles):
    if getattr(article, 'id', None) != None:
        cleanCategoriesDict[new_cat].append(article.id);
    else:
        print article