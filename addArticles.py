import pymongo
from cluster_name import cluster_name

class AddArticles():

    def __init__(self):
        self.m = pymongo.MongoClient("146.148.59.202", 27017)
        self.db = self.m.big_data

    def findAndAddArticles(self, category, clusterName):
        query = {"v" : "0.0.6", "categories" : {"$in" : [category]}}
        cursor = self.db.articles.find(query)
        ids = []
        for doc in cursor:
            objectid = doc["_id"]
            ids.append(objectid)
        newQuery = {"clusterName" : clusterName}
        self.db.clusters.update(newQuery, {"$addToSet" : {"articles" : {"$each" : ids}}})

a = AddArticles()
categories = ["showbiz", "movies", "arts", "justice", "dining", "health", "technology", "business"]
for c in categories:
    clustername = cluster_name(c)
    a.findAndAddArticles(c, clustername)