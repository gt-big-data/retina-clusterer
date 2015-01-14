# -*- coding: utf-8 -*-
from app import *

clusterList = getArticleClusterList();
print 'Number of clusters: '+str(len(clusterList))+'\n'
for cluster in clusterList:
	myCount = getClusterArticleCount(cluster);
	print cluster+' ( '+str(myCount)+' )\n'