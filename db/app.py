from pymongo import MongoClient
from bson.objectid import ObjectId
import time
import hashlib
import md5
from datetime import datetime, timedelta

## ~~~FOR USE IN LOCALHOST ONLY~~~ :D ##
# client = MongoClient('mongodb://localhost:27017/')
# db = client['BigData']

client = MongoClient('mongodb://146.148.59.202:27017/')
db = client['big_data']

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

def getCluster(clusterName):
    cluster = db.clusters.find({ "clusterName": clusterName })

    if cluster.count() <= 0:
        return {
            "error": "Error: No " + clusterName + " cluster found."
        }

    articles = []
    for articleId in cluster[0][u'articles']:
        article = db.articles.find_one({ "_id": articleId })
        # There must be a more effective way to get all the articles
        # without making the cursor go over the db multiple times...
        articles.append(article)

    return {
        "clusterName": cluster[0][u'clusterName'],
        "articles": articles,
        "_id": cluster[0][u'_id'],
        "features": cluster[0][u'features'],
    }


def createCluster(clusterName, objectID):
    # objectID is an array
    db.clusters.insert( { "clusterName": clusterName, "_id": hashlib.md5(clusterName).hexdigest(), "articles": objectID } )

def deleteCluster(clusterName):
    db.clusters.remove( { "clusterName": clusterName })

def insertToCluster(articleIDs, clusterName): # articleIDs is an array
    db.clusters.update( { "clusterName": clusterName }, { "$push": { "articles": {'$each': articleIDs} } } )

def deleteFromCluster(articleIDs, clusterName):
    db.clusters.update( { "clusterName": clusterName }, { "$pull": { "articles": {'$in': articleIDs} } } )

def getClusterArticleCount(clusterName):
    cluster = db.clusters.find_one({ "clusterName": clusterName })
    if not cluster:
        return -1

    if 'articles' not in cluster:
        return 0
    return cluster["articles"];