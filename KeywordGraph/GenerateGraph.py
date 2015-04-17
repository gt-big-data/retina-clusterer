from ..db import app
from ..db.app import Article
import time
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from collections import defaultdict
from igraph import *

beginTime = time.time() - 3*24*3600
endTime = beginTime + 3*24*3600
articles = app.getArticlesBetweenTimes(beginTime, endTime)

i = 0
nodes = [], edges = []
g = Graph()
for i in range(0, len(articles)-2):
	for j in range(i+1, len(articles)-1):
		commonKeywords = list(set(articles[i].keywords).intersection(articles[j].keywords))
		if 'continuing browse' in articles[i].keywords: # don't like those for now
			commonKeywords = []
		if len(commonKeywords) > 1:
			edges.append('{"source": '+ str(i) +', "target": '+str(j)+', "value": '+str(len(commonKeywords))+' }')
			g.add_edges((i, j))

coloring = g.community_spinglass()
memberships = coloring.membership

for i, membership in zip(range(0,len(articles)-1), memberships):
	nodes.append('{"id": '+str(i)+', "name": "'+articles[i].title.encode('utf-8').replace('"', '')+'", "group": '+membership+' }');

f = open('retina-clusterer/KeywordGraph/lastGraph.json','w')
fullTxt = '{\n"nodes": \n['+',\n'.join(nodes)+'\n],\n"links":\n[\n'+',\n'.join(edges)+'\n]\n}'

f.write(fullTxt)
f.close()