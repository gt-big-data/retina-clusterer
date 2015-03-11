from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import time
from db import app
from db.app import Article
from classification import vectorize
from cluster_name import cluster_name
from collections import defaultdict
from sklearn.naive_bayes import MultinomialNB
from supervisedTest import static_classifier_test
from bson.objectid import ObjectId

# This function should be ran every 4 hours in the future (!)
new_articles = app.getArticlesByTimeStamp(time.time() - 4 * 3600) # last four hours

unlabeled_articles = [];
unlabeled_texts = [];

cleanCategoriesDict = defaultdict(list) #Maps a clean category to a list of articleIDs

for article in new_articles:
    cleanCategory = cluster_name(article.category)
    if article.text is not None:
        if cleanCategory != '': # a category was already detected
            cleanCategoriesDict[cleanCategory].append(article.id) #Add the article ID
            app.insertCleanArticle(Article(article.title, article.text, cleanCategory, article.clusterDate, article.id, []))
        else: # no category was matched, we will run it through the clustering afterwards
            unlabeled_articles.append(article);
            unlabeled_texts.append(article.text);

predicted_labels = static_classifier_test(unlabeled_texts)

for new_cat, article in zip(predicted_labels, unlabeled_articles):
    if getattr(article, 'id', None) != None:
        cleanCategoriesDict[new_cat].append(article.id);
        app.insertCleanArticle(Article(article.title, article.text, new_cat, article.clusterDate, article.id, []))
    else:
        print article

# append to the database in clusters (old)
for cleanCategory in cleanCategoriesDict.keys():
    articleIDs = cleanCategoriesDict[cleanCategory]
    if not all(type(_id) == ObjectId for _id in articleIDs):
        print articleIDs
    else:
        app.insertToCluster(articleIDs, cleanCategory)
# append to our new table