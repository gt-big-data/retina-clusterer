from db import app
from db.app import Article
import time
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from collections import defaultdict


startFrom = 60
daysAgo = startFrom
totalSum = 0
day2nb = {}
# while daysAgo > 0:
# 	nb = app.getNbArticlesInXDays(daysAgo)
# 	if daysAgo != startFrom:
# 		day2nb[daysAgo] = totalSum-nb
# 	totalSum = nb
# 	daysAgo = daysAgo - 1
# for day, nb in day2nb.iteritems():
#     print nb, " articles added ", day, "days ago"

beginTime = 1425941931#time.time() - 18*24*3600
endTime = beginTime + 3*24*3600
articles = app.getArticlesBetweenTimes(beginTime, endTime)

i = 0
edges = [];
for i in range(0, len(articles)-2):
	for j in range(i+1, len(articles)-1):
		commonKeywords = list(set(articles[i].keywords).intersection(articles[j].keywords))
		if 'continuing browse' in articles[i].keywords: # don't like those for now
			commonKeywords = []
		if len(commonKeywords) != 0:
			edges.append('{"source": 628, "target": 291, "value": 2 }')
f = open('knn_test.txt','w')
f.write('\n'.join(edges))
f.close()
	# print articles[i].title.encode('utf-8')