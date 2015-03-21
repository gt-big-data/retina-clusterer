from app import *

print "Last articles added:\n"


articles = getLatestCleanArticles(10)

for article in articles:
	print article.title.encode('utf-8') , "\n-------------------------------------\n", article.keywords ,"\n\n"

# clusterList = getArticleClusterList();
# for cluster in clusterList:
# 	ret = getLatestCluster(cluster, 1);
# 	lastArticle = ret[0];
# 	print "[", lastArticle.category , "]", lastArticle.title.encode('utf-8'), "\n"