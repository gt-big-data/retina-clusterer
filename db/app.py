from datetime import datetime, date, timedelta
from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from collections import namedtuple
import time, json, sys

from article import *
from dbco import *

def getArticlesByTimeStamp(timeStamp, limit=1000):
    timeObj = datetime.utcfromtimestamp(timeStamp)
    articles = db.qdoc.find({'$and': [{"content": {'$ne': ''}}, {"title": {'$ne': ''}}, {"timestamp": {"$gte":  timeStamp}}]}).limit(limit);
    return buildArticleArray(articles)

def getArticlesInLastNDays(n=10, limit=1000):
    return getArticlesByTimeStamp(time.time() - n*24*3600, limit)

def getNbArticlesInXDays(days=60):
    return db.qdoc.find({'timestamp': {'$gte': (time.time() - days*24*3600)}}).count()

def getArticlesBetweenTimes(time1, time2):
    articles = db.qdoc.find({'$and': [{'timestamp': {'$gte': time1}}, {'timestamp': {'$lte': time2}}]})
    return buildArticleArray(articles)

def getCrawlerVersion():
    doc = db.articles.find_one({"_id" : "version"})
    return doc["number"]

def getArticleClusterList():
    clusters = db.clusters.distinct('clusterName')
    clusterNameArray = []
    for cluster in clusters:
        clusterNameArray.append(cluster)
    return clusterNameArray

def getLatestCluster(clusterName, limit = 50, skip=0):
    if limit == 0: # If limit is 0, get ALL articles.
        limit = db.cleanarticles.find({'category': clusterName}).count()
    articles = db.cleanarticles.find({ "$query": { "category":  clusterName }, "$orderby": { 'download_time' : -1 } }).skip(skip).limit(limit)
    clean_articles = []
    for article in articles:
        clean_articles.append(Article(article['_id'], article['title'], '', 0, '', '', article['text']))
    return clean_articles

def getTrainingSet(limit = 50, skip=0):
    clusterList = getArticleClusterList()
    trainingSet = []
    for cluster in clusterList:
        articles = getLatestCluster(cluster, limit, skip)
        for article in articles:
            if article.content is not None:
                trainingSet.append(article)
    return trainingSet

def getArticlesNoKeywords(limit=30):
    articles = db.qdoc.find({ "$query": { "keywords":  [] }, "$orderby": { 'timestamp' : -1 } }).limit(limit)
    return buildArticleArray(articles)

def updateKeywords(articleID, keywords):
    db.qdoc.update({ "_id": articleID },{"$set": {"keywords": keywords}})

def articlesWithKeywordsCount():
    return db.qdoc.find({'keywords': {'$ne': []}}).count()