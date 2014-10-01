from pymongo import MongoClient
from bson.objectid import ObjectId
import time
import hashlib

client = MongoClient('mongodb://localhost:27017/')
db = client['BigData']

def getCluster(clusterName):
    cluster = db.clusters.find({ "clusterName": clusterName })

    articles = []
    for articleId in cluster[0][u'articles']:
        article = db.articles.find_one({ "_id": articleId })
        articles.append(article)

    return {
        "clusterName": cluster[0][u'clusterName'],
        "articles": articles,
        "_id": cluster[0][u'_id'],
        "features": cluster[0][u'features'],
    }
