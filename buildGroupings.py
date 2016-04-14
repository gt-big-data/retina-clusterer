from dbco import *
import time
import numpy as np

def largestTopics(days, limit):
    limit = int(limit); days = int(days)
    startTime = time.time() - days * 24 * 3600
    endTime = time.time()
    match = {"$match" : {"timestamp" : {"$gt" : startTime, "$lt" : endTime}, 'topic': {'$exists': True}}}
    group = {"$group" : {"_id" : "$topic", "count" : {"$sum" : 1}}}
    sort = {"$sort" : {"count" : -1}}
    limit = {"$limit" : limit}
    topicCounts = list(db.qdoc.aggregate([match, group, sort, limit]))

    return topicCounts
def buildGroupings(topic=0):
	if topic == 0:
		topic = largestTopics(3,2)[1]['_id']
	arts = list(db.qdoc.find({'topic': topic}).sort('timestamp', 1))
	print "Number of articles: ", len(arts)
	timestamps = [a['timestamp'] for a in arts]
	diffs = np.diff(timestamps)
	mean = np.mean(diffs)
	std = np.std(diffs)

	buckets = {}
	oldTime = 0; i = -1
	for a in arts:
		print len(buckets[i])
		if (a['timestamp']-oldTime > (mean) and (i==-1 or len(buckets[i])>=5)) or (len(buckets[i]) >= 20):
			i += 1; buckets[i] = []
		buckets[i].append(a)
		oldTime = a['timestamp']
	print "Number of buckets: ", len(buckets)

	return buckets

if __name__ == '__main__':
	buckets = buildGroupings()
	for b in buckets:
		buck = buckets[b]
		text = "\n".join([a['content'] for a in buck])