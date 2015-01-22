# WARNING! DISREGARD THIS FILE!
# THIS FILE FOR TESTING PURPOSES ONLY

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
import time
import hashlib
import md5
from app import getClusterArticleCount, client, db
from datetime import datetime, timedelta

def updatedGetCluster(clusterName, limit = 0):
    cluster = db.clusters.find_one({ "clusterName": clusterName })
    if limit == 0:
        limit = getClusterArticleCount(clusterName);
    if cluster['articles'] is None:
        return {
            "error": "Error: No " + clusterName + " cluster found."
        }

    articles = db.articles.find ( { "$query": { "_id":  { "$in": cluster["articles"] } }, "$orderby": { 'recent_pub_date' : -1 }, "$limit": limit } )
    count = 0
    for a in articles:
        count += 1
        print a['title']
    return count;
    # return len(dumps(articles));

print updatedGetCluster("Politics")
