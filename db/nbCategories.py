# -*- coding: utf-8 -*-
from app import *

clusterList = getArticleClusterList();
print 'Number of clusters: '+str(len(clusterList))+'\n'
array = [];
for cluster in clusterList:
	myCount = getClusterArticleCount(cluster)
	array.append(cluster+': '+str(myCount))
print "|".join(array)