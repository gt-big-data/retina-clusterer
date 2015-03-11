# DON'T RUN THIS BEFORE CHECKING WITH EVERY ONE

import time
from db import app
from cluster_name import cluster_name
def clusterPurge():
	app.db.clusters.remove()
	clusters = ['Politics', 'Sports', 'Technology', 'Arts', 'Justice', 'Travel', 'Dining', 'Health', 'Business', 'World', 'Theater', 'Science', 'US', 'Movies', 'Opinion'];
	clusterArticles = {};

	for cluster in clusters:
		app.createCluster(cluster, []);
		clusterArticles[cluster] = []

	articleList = app.getArticlesByTimeStamp((time.time() - 300 * 86400), 20000) # last hundred day's worth of articles

	nbArticles = 0
	for article in articleList:
		cleanCat = cluster_name(article.category)
		if cleanCat != '':
			clusterArticles[cleanCat].append(article.id)
			nbArticles += 1

	for cluster in clusters:
		app.insertToCluster(clusterArticles[cluster], cluster)
	print len(clusters), "clusters, ", nbArticles, " articles added"

clusterPurge()