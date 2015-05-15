from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import time
from ..db import app
from ..db.app import Article
from ..classification import vectorize
from ..cluster_name import cluster_name
from collections import defaultdict
from sklearn.naive_bayes import MultinomialNB
from ..supervisedTest import static_classifier_test
from bson.objectid import ObjectId
from sklearn.svm import SVC

new_articles = app.getArticlesByTimeStamp((time.time() - 304 * 3600), 2500) # last four hours
print len(new_articles)
unlabeled_articles = [];
unlabeled_texts = [];

cleanCategoriesDict = defaultdict(list) #Maps a clean category to a list of articleIDs

for article in new_articles:
    cleanCategory = cluster_name(article.category)
    if article.text is not None:
        if cleanCategory != '': # a category was already detected
            cleanCategoriesDict[cleanCategory].append(article.id) #Add the article ID
            app.insertCleanArticle(Article(article.title, article.text, cleanCategory, article.clusterDate, article.id, [], article.img))
        else: # no category was matched, we will run it through the clustering afterwards
            unlabeled_articles.append(article);
            unlabeled_texts.append(article.text);

predicted_labels = static_classifier_test(unlabeled_texts)

for new_cat, article in zip(predicted_labels, unlabeled_articles):
    if getattr(article, 'id', None) != None:
        cleanCategoriesDict[new_cat].append(article.id);
        app.insertCleanArticle(Article(article.title, article.text, new_cat, article.clusterDate, article.id, [], article.img))
    else:
        print article