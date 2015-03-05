# -*- coding: utf-8 -*-
from app import *

clusterList = getArticleClusterList();
print 'Number of clusters: '+str(len(clusterList))
array = [];
for cluster in clusterList:
	myCount = getClusterArticleCount(cluster)
	array.append(cluster+': '+str(myCount))
print "| "+(" | ".join(array))+" |"+'\n'
print "Number of articles in cleanArticles: ", db.cleanArticles.count()