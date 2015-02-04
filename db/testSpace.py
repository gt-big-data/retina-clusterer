# WARNING! DISREGARD THIS FILE!
# THIS FILE FOR TESTING PURPOSES ONLY

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
import time
import hashlib
import md5
from app import getClusterArticleCount, getArticleClusterList, client, db
from datetime import datetime, timedelta
from collections import namedtuple

Article = namedtuple('Article', ['title', 'text', 'categories', 'id'])

def getLatestCluster(clusterName, limit = 50):
    cluster = db.clusters.find_one({ "clusterName": clusterName })
    if limit == 0:
        limit = getClusterArticleCount(clusterName);
    if cluster['articles'] is None:
        return {
            "error": "Error: No " + clusterName + " cluster found."
        }
    articles = db.articles.find ( { "$query": { "_id":  { "$in": cluster["articles"] } }, "$orderby": { 'recent_pub_date' : -1 } } ).limit(limit)

    clean_articles = [];
    for article in articles:
        clean_articles.append(Article(article['title'], article['text'], article['categories'], article['_id']))

    return clean_articles

#print getLatestCluster("Sports");

def getTrainingSet(limit = 0):
    clusterList = getArticleClusterList()
    trainingSet = []
    
    for cluster in clusterList:
        trainingSet.append(getLatestCluster(cluster, limit))

    return trainingSet

print getTrainingSet(1);

# // See articleLoader file
# // see nametuble in file
# // TODO getTrainingSet() -> for loops every category with getLatestCluster(...). returns the articles
# // for cluster in clusterNames:
# // article[title], article[text], cluster's name, article[id]
