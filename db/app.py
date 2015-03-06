from pymongo import MongoClient, errors
from bson.objectid import ObjectId
import time
import hashlib
import md5
from datetime import datetime, date, timedelta
from collections import namedtuple

## ~~~FOR USE IN LOCALHOST ONLY~~~ :D ##
# client = MongoClient('mongodb://localhost:27017/')
# db = client['BigData']

client = MongoClient('mongodb://146.148.59.202:27017/')
db = client['big_data']

Article = namedtuple('Article', ['title', 'text', 'categories', 'clusterDate', 'id']) # This used with getLatestCluster(limit = 0)

def getArticlesByTimeStamp(timeStamp, limit=1000):
    timeObj = datetime.utcfromtimestamp(timeStamp);
    version = getCrawlerVersion()
    articles = db.articles.find({'$and': [{"v": version}, {"text": {'$ne': ''}}, {"title": {'$ne': ''}}, {"recent_download_date": {"$gte":  timeObj}}]}).limit(limit);
    returnObject = [];
    for article in articles:
        cat = ''
        if article['categories'] is not None:
            cat = article['categories'][0];
        returnObject.append(Article(article['title'], article['text'], cat, article['recent_download_date'], article['_id'])) # this is old categories, be careful
    return returnObject

def getArticlesInLastNDays(n=10, limit=1000):
    return getArticlesByTimeStamp(time.time() - n*24*3600, limit)

def getPopulatedCount(timeStamp):
    timeObj = datetime.utcfromtimestamp(timeStamp);
    version = getCrawlerVersion()
    count = db.articles.find({'$and': [{"v": version}, {"text": {'$ne': ''}}, {"title": {'$ne': ''}}, {"recent_download_date": {"$gte":  timeObj}}]}).count()
    return count

def getCrawlerVersion():
    # Get current version of crawler
    query = {"_id" : "version"}
    doc = db.articles.find_one(query)
    return doc["number"]

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
    db.clusters.update( { "clusterName": clusterName }, { "$addToSet": { "articles": {'$each': articleIDs} } } )

def deleteFromCluster(articleIDs, clusterName):
    db.clusters.update( { "clusterName": clusterName }, { "$pull": { "articles": {'$in': articleIDs} } } )

def getLatestCluster(clusterName, limit = 50, skip=0):
    cluster = db.clusters.find_one({ "clusterName": clusterName })
    if limit == 0: # If limit is 0, get ALL articles.
        limit = getClusterArticleCount(clusterName);
    if cluster['articles'] is None:
        return {
            "error": "Error: No " + clusterName + " cluster found."
        }
    articles = db.articles.find ( { "$query": { "_id":  { "$in": cluster["articles"] } }, "$orderby": { 'recent_download_date' : -1 } } ).skip(skip).limit(limit)

    clean_articles = [];
    for article in articles:
        clean_articles.append(Article(article['title'], article['text'], clusterName, article['recent_download_date'], article['_id']))

    return clean_articles

def getTrainingSet(limit = 50, skip=0):
    clusterList = getArticleClusterList()
    trainingSet = []

    for cluster in clusterList:
        articles = getLatestCluster(cluster, limit, skip)
        for article in articles:
            trainingSet.append(article)

    return trainingSet

def getClusterArticleCount(clusterName):
    cluster = db.clusters.find_one({ "clusterName": clusterName })
    if not cluster:
        return -1

    if 'articles' not in cluster:
        return 0
    return len(cluster["articles"]);

def getArticleCluster(articleID):
    clusterList = getArticleClusterList()
    cursor = db.clusters.find({"articles": ObjectId(articleID)}, {"clusterName": 1, "_id":0})
    for cluster in cursor:
        return cluster.get("clusterName")

def insertCleanArticle(article):
    if (article.title == '') | (article.title is None):
        return -1
    elif article.text == '':
        return -1
    else:
        try:
            db.cleanArticles.insert( { "_id": article.id, "title": article.title, "text": article.text, "download_time": article.clusterDate, "category": article.categories, "keywords": [] } )
        except:
            pass # print "0" # what happened here is there was a duplicate key
