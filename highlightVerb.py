#!/usr/bin/env python
# -*- coding: utf-8 -*-

from buildGroupings import *
import sys, random, time, operator
from dbco import *
from collections import Counter
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

pronouns = ['i', 'you', 'he', 'she', 'it', 'we', 'you', 'they', 'me', 'you', 'him', 'her', 'it', 'us', 'them']
fakeSubjects = ['this', 'that']

topic = largestTopics(3,5)[0]['_id']
print db.qdoc.find({'topic': topic}).count()

art = list(db.qdoc.find({'topic': topic}).sort('timestamp', 1))

verbLines = {}
ts = [a['timestamp'] for a in art]

bucketSize = int((max(ts)-min(ts))/33.0)

tsMods = [(a['timestamp']-(a['timestamp']%bucketSize)) for a in art]
minBucket = min(tsMods); maxBucket = max(tsMods);

numBuckets = int((maxBucket-minBucket)/bucketSize)+1

sentenceCount = {int(minBucket+bu*bucketSize): 0 for bu in range(numBuckets)}
for a in art:
	doc = nlp(unicode(a['content']))
	tsMod = a['timestamp']-(a['timestamp']%bucketSize)
	sentCount = 0
	for s in doc.sents:
		sentTxt = " ".join([w.orth_ for w in s])
		subj = ''; dobj = '';
		verb = s.root.lemma_
		if s.root.orth_ == "'s":
			verb = 'be'
		if verb not in ['say', 'tell']: #
			sentCount += 1
			if verb not in verbLines:
				verbLines[verb] = [{'tsMod': (minBucket+bu*bucketSize), 'sentences': []} for bu in range(numBuckets)]
			for slot in verbLines[verb]:
				if slot['tsMod'] == tsMod:
					slot['sentences'].append(sentTxt)
					break
	sentenceCount[tsMod] += sentCount
verbCounts = {}
for verb in verbLines:
	verbCounts[verb] = sum([len(t['sentences']) for t in verbLines[verb]])

verbCounts = sorted(verbCounts.items(), key=operator.itemgetter(1), reverse=True)[:50]
sortedSentenceCount = sorted(sentenceCount.items(), key=operator.itemgetter(0), reverse=False)

verbVect = {}

for verb, count in verbCounts:
	verbVect[verb] = []
	for t in verbLines[verb]:
		tsMod = t['tsMod']
		t['perc'] = int(100.0*float(len(t['sentences']))/(0.1+sentenceCount[tsMod]))
		verbVect[verb].append(len(t['sentences']))

print "SENTENCES".ljust(15), " ".join([str(sc).ljust(3) for tsMod, sc in sortedSentenceCount])

for verb, count in verbCounts:
	# print verb.ljust(15), " ".join([str(t['perc']).ljust(3) for t in verbLines[verb]])
	print "-----------------------------------------"
	print verb
	mean = np.mean(verbVect[verb])
	std = np.std(verbVect[verb])
	for t in verbLines[verb]:
		t['score'] = int((len(t['sentences'])-mean)/std)
		if t['score'] >= 2:
			print "\n".join(t['sentences']).encode('utf-8')+'\n'