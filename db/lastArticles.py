from app import *

print "Last articles added to each cluster:"

clusterList = getArticleClusterList();
for cluster in clusterList:
	ret = getLatestCluster(cluster, 1);
	lastArticle = ret[0];
	print "[", lastArticle.categories , "]", lastArticle.title.encode('utf-8'), "\n"