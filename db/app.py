from pymongo import MongoClient, errors
from bson.objectid import ObjectId
import time
import json
import sys
from datetime import datetime, date, timedelta
from collections import namedtuple

reload(sys)
sys.setdefaultencoding('utf-8')

client = MongoClient('mongodb://146.148.59.202:27017/')
db = client['big_data']

Article = namedtuple('Article', ['title', 'text', 'category', 'clusterDate', 'id', 'keywords', 'img', 'url', 'source'])

def getArticlesByTimeStamp(timeStamp, limit=1000):
    timeObj = datetime.utcfromtimestamp(timeStamp)
    articles = db.qdoc.find({'$and': [{"content": {'$ne': ''}}, {"title": {'$ne': ''}}, {"timestamp": {"$gte":  timeStamp}}]}).limit(limit);
    returnObject = [];
    for article in articles:
        cat = ''
        if 'categories' in article:
            cat = article['categories']
        img = ''
        if article['img'] is not None:
            img = article['img']
        returnObject.append(Article(article['title'], article['content'], cat, datetime.utcfromtimestamp(article['timestamp']), article['_id'], [], img, article['url'], article['source'])) # this is old categories, be careful
    return returnObject

def getArticlesInLastNDays(n=10, limit=1000):
    return getArticlesByTimeStamp(time.time() - n*24*3600, limit)

def getNbArticlesInXDays(days=60):
    return db.qdoc.find({'timestamp': {'$gte': (time.time() - days*24*3600)}}).count()

def getArticlesBetweenTimes(time1, time2):
    articles = db.qdoc.find({'$and': [{'timestamp': {'$gte': time1}}, {'timestamp': {'$lte': time2}}]})
    clean_articles = []
    for article in articles:
        img = ''
        if 'img' in article:
            img = article['img']
        category = ''
        if 'category' in article:
            category = article['category']
        clean_articles.append(Article(article['title'], article['content'], category, article['timestamp'], article['_id'], article['keywords'], img, article['url'], article['source']))
    return clean_articles

def getCrawlerVersion():
    doc = db.articles.find_one({"_id" : "version"})
    return doc["number"]

def getArticleClusterList():
    articles = db.clusters.distinct('clusterName')
    clusterNameArray = []

    for article in articles:
        clusterNameArray.append(article)

    return clusterNameArray

def getLatestCluster(clusterName, limit = 50, skip=0):
    if limit == 0: # If limit is 0, get ALL articles.
        limit = getClusterArticleCount(clusterName);
    articles = db.cleanarticles.find({ "$query": { "category":  clusterName }, "$orderby": { 'download_time' : -1 } }).skip(skip).limit(limit)
    clean_articles = []
    for article in articles:
        img = ''
        if 'img' in article:
            img = article['img']
        clean_articles.append(Article(article['title'], article['text'], clusterName, article['download_time'], article['_id'], article['keywords'], img, '', ''))
    return clean_articles

def getTrainingSet(limit = 50, skip=0):
    clusterList = getArticleClusterList()
    trainingSet = []

    for cluster in clusterList:
        articles = getLatestCluster(cluster, limit, skip)
        for article in articles:
            if article.text is not None:
                trainingSet.append(article)

    return trainingSet

def getClusterArticleCount(clusterName):
    return db.cleanarticles.find({'category': clusterName}).count()

def insertCleanArticle(article):
    if (article.title == '') | (article.title is None):
        return -1
    elif article.text == '':
        return -1
    else:
        try:
            db.cleanarticles.insert( { "_id": article.id, "title": article.title, "text": article.text, "download_time": article.clusterDate, "category": article.category, "keywords": [], "img": article.img } )
        except:
            pass # print "0" # what happened here is there was a duplicate key

def getArticlesNoKeywords(limit=30):
    articles = db.qdoc.find({ "$query": { "keywords":  [] }, "$orderby": { 'timestamp' : -1 } }).limit(limit)
    clean_articles = []
    for article in articles:
        img = ''
        if 'img' in article:
            img = article['img']
        category = ''
        if 'category' in article:
            category = article['category']
        clean_articles.append(Article(article['title'], article['content'], category, article['timestamp'], article['_id'], [], img, article['url'], article['source']))
    return clean_articles

def getLatestCleanArticles(limit=30):
    articles = db.cleanarticles.find({ "$query": { "title": {'$ne': ''}  }, "$orderby": { 'download_time' : -1 } }).limit(limit)
    clean_articles = []
    for article in articles:
        img = ''
        if 'img' in article:
            img = article['img']
        clean_articles.append(Article(article['title'], article['text'], article['category'], article['download_time'], article['_id'], article['keywords'], img, '', ''))
    return clean_articles

def updateKeywords(articleID, keywords):
    db.qdoc.update({ "_id": articleID },{"$set": {"keywords": keywords}})

def articlesWithKeywordsCount():
    return db.qdoc.find({'keywords': {'$ne': []}}).count()

def insertCleanArticles(articles):
    jsonArticles = []
    for article in articles:
        if (article.title == '') | (article.title is None):
            return -1
        elif article.text == '':
            return -1
        else:
            data = { "_id": article.id, "title": article.title, "text": article.text, "download_time": article.clusterDate, "category": article.categories, "keywords": [], "img": article.img}
            jsonArticle = json.dumps(data)
            jsonArticles.append(jsonArticle)
    try:
        db.cleanarticles.insert(jsonArticles)
    except:
        pass