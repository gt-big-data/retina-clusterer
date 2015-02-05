from pymongo import MongoClient
from bson.objectid import ObjectId
import time
import hashlib
import md5
from datetime import datetime
from collections import namedtuple

## ~~~FOR USE IN LOCALHOST ONLY~~~ :D ##
# client = MongoClient('mongodb://localhost:27017/')
# db = client['BigData']

client = MongoClient('mongodb://146.148.59.202:27017/')
db = client['big_data']

Article = namedtuple('Article', ['title', 'text', 'categories', 'clusterDate', 'id']) # This used with getLatestCluster(limit = 0)

def getArticlesByTimeStamp(timeStamp, limit=1000):
    timeObj = datetime.utcfromtimestamp(timeStamp);
    articles = db.articles.find({'$and': [{"v": "0.0.6"}, {"text": {'$ne': ''}}, {"title": {'$ne': ''}}, {"categories": {'$ne': [], '$ne': None}}, {"recent_pub_date": {"$gte":  timeObj}}]}).limit(limit);
    returnObject = {"articleArray": []}
    for article in articles:
        returnObject['articleArray'].append(article)

    return returnObject

def getPopulatedCount(timeStamp):
    timeObj = datetime.utcfromtimestamp(timeStamp);
    count = db.articles.find({'$and': [{"v": "0.0.6"}, {"text": {'$ne': ''}}, {"title": {'$ne': ''}}, {"categories": {'$ne': [], '$ne': None}}, {"recent_pub_date": {"$gte":  timeObj}}]}).count()
    return count

# The next functions are for clusters
def getArticleClusterList():
    articles = db.clusters.distinct('clusterName')
    clusterNameArray = []

    for article in articles:
        clusterNameArray.append(article)

    return clusterNameArray

def createCluster(clusterName, objectID):
    # objectID is an array
    db.clusters.insert( { "clusterName": clusterName, "_id": hashlib.md5(clusterName).hexdigest(), "articles": objectID } )

def deleteCluster(clusterName):
    db.clusters.remove( { "clusterName": clusterName })

def insertToCluster(articleIDs, clusterName): # articleIDs is an array
    db.clusters.update( { "clusterName": clusterName }, { "$push": { "articles": {'$each': articleIDs} } } )

def deleteFromCluster(articleIDs, clusterName):
    db.clusters.update( { "clusterName": clusterName }, { "$pull": { "articles": {'$in': articleIDs} } } )


def getLatestCluster(clusterName, limit = 50):
    cluster = db.clusters.find_one({ "clusterName": clusterName })
    if limit == 0: # If limit is 0, get ALL articles.
        limit = getClusterArticleCount(clusterName);
    if cluster['articles'] is None:
        return {
            "error": "Error: No " + clusterName + " cluster found."
        }
    articles = db.articles.find ( { "$query": { "_id":  { "$in": cluster["articles"] } }, "$orderby": { 'recent_pub_date' : -1 } } ).limit(limit)

    clean_articles = [];
    for article in articles:
        clean_articles.append(Article(article['title'], article['text'], clusterName, article['recent_pub_date'], article['_id']))

    return clean_articles

def getTrainingSet(limit = 50):
    clusterList = getArticleClusterList()
    trainingSet = []

    for cluster in clusterList:
        trainingSet.append(getLatestCluster(cluster, limit))

    return trainingSet

def getClusterArticleCount(clusterName):
    cluster = db.clusters.find_one({ "clusterName": clusterName })
    if not cluster:
        return -1

    if 'articles' not in cluster:
        return 0
    return len(cluster["articles"]);
