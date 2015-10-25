from db import app
from bson.objectid import ObjectId
from article import *
from time import *
import time
from datetime import datetime
from dateutil import tz

from collections import Counter
from igraph import *

class JSONEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, ObjectId):
			return str(o)
		return json.JSONEncoder.default(self, o)

def generateGraphForDay(endTime):
	beginTime = endTime - 3*24*3600
	articles = app.getArticlesBetweenTimes(beginTime, endTime)

	art = db.qdoc.find({'$query': {}, '$orderby': {'topic': -1}}).limit(1)
	
	maxTopic = art[0]['topic']
	print maxTopic

	updatedTopics = []
	edgesClean = []
	g = Graph()
	g.add_vertices(len(articles))

	for i in range(0, len(articles)-2):
		for j in range(i+1, len(articles)-1):
			commonKeywords = list(set(articles[i].keywords).intersection(articles[j].keywords))
			if len(commonKeywords) > 2:
				edgesClean.append({"source": articles[i].guid, "target": articles[j].guid, "value": len(commonKeywords)})
				g.add_edges([(i, j)])

	coloring = g.community_infomap()
	memberships = coloring.membership

	memberCounts = Counter(memberships)
	bigCommList = [k for k,v in memberCounts.iteritems() if v>=3]

	oldTopics = []
	for i, membership in zip(range(0,len(articles)-1), memberships):
		oldTopics.append(articles[i].topic)

	for bigComm in bigCommList:
		oldTopicList = []
		idList = []
		for i, membership, oldTopic in zip(range(0,len(articles)-1), memberships, oldTopics):
			if membership == bigComm:
				idList.append(articles[i].guid)
				oldTopicList.append(oldTopic)

		newTopic = 0
		nonZeroTopic = [v for v in oldTopicList if v != 0]
		updatedTopics.extend(nonZeroTopic)
		if len(nonZeroTopic) == 0:
			maxTopic += 1
			newTopic = maxTopic
		else:
			counter = Counter(nonZeroTopic)
			newTopic = counter.most_common(1)[0][0]
		updatedTopics.append(newTopic)
		db.qdoc.update({"_id": {'$in': idList}}, {"$set": {"topic": newTopic}}, multi=True)
	return updatedTopics

def updateTopicKeywords(topicIds):
	keywordsAndTopics = db.qdoc.aggregate([
		{'$match': {'topic': {'$in': topicIds}}},
		{'$project': {'topic': True, 'keywords': True}},
		{'$unwind': '$keywords'},
		{'$group': {
			'_id': {'topic': '$topic', 'keyword': '$keywords'},
			'count': {'$sum': 1}}},
		{'$group': {
			'_id': '$_id.topic',
			'keywords': {
				'$push' : {'keyword': '$_id.keyword', 'count': '$count'}},
		}},
		{'$unwind': '$keywords'},
		{'$sort': {'_id': -1, 'keywords.count': -1}},
		{'$group': {
			'_id': '$_id',
			'keywords': {'$push' : {'keyword': '$keywords.keyword', 'count': '$keywords.count'}},
			'totalKeywords': {'$sum': '$keywords.count'}}},
	], allowDiskUse=True)

	topicUpdate = db.topic.initialize_unordered_bulk_op()
	for topic in keywordsAndTopics:
		topicUpdate.find({'_id': topic['_id']}).upsert().update({
			'$set': {
				'keywords': topic['keywords'][:10],
				'totalKeywords': topic['totalKeywords'],
			},
		})
	topicUpdate.execute()

if __name__ == '__main__':
	# days = 15
	# for d in range(0,days):
	# 	t = time.time()-(days-d)*86400
	# 	updatedTopics = generateGraphForDay(t)
	# 	updateTopicKeywords(updatedTopics)
	updatedTopics = generateGraphForDay(time.time())
	updateTopicKeywords(updatedTopics)
