from buildGroupings import *
import sys, random, time, operator
from dbco import *
from collections import Counter

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
		if (a['timestamp']-oldTime > (mean) and (i==-1 or len(buckets[i])>=5)) or (len(buckets[i]) >= 20):
			i += 1; buckets[i] = []
		buckets[i].append(a)
		oldTime = a['timestamp']
	print "Number of buckets: ", len(buckets)

	return buckets

def recursiveCleaning(tok, head, arr, expecting):
	for w in tok.subtree:
		if w.dep_ in expecting and w.head == head:
			arr.append(w.i)
			for w2 in w.children:
				recursiveCleaning(w2, w, arr, ['poss', 'case', 'compound', 'adj', 'aux', 'nsubj', 'prt', 'advcl','part','dobj', 'pobj', 'conj', 'npadvmod', 'cc', 'pcomp', 'ccomp', 'mark', 'nummod', 'prep', 'amod', 'det'])

def subjCleaning(tok, head, arr, expecting):
	for w in tok.subtree:
		if w.dep_ in expecting and w.head == head:
			arr.append(w.i)
			for w2 in w.children:
				recursiveCleaning(w2, w, arr, ['compound', 'aux', 'prt', 'advcl','part','dobj', 'pobj', 'conj', 'npadvmod', 'cc', 'pcomp', 'ccomp', 'mark', 'nummod', 'prep', 'amod'])

def coreSentence(s):
	verb = s.root
	cleanSentence = [verb.i]
	for l in verb.lefts:
		subj = []
		recursiveCleaning(l, verb, subj, ['nsubj', 'aux'])
		if len(subj) > 0:
			cleanSentence.extend(subj)
	expecting = ['dobj', 'ccomp', 'xcomp']
	if verb.lemma_ in ['be']:
		expecting.extend(['acomp', 'attr'])
	for r in verb.rights:
		compl = []
		recursiveCleaning(r, verb, compl, expecting)
		cleanSentence.extend(compl)

	cleanSentence = sorted(cleanSentence)
	cleanSentence = [doc[idx].orth_ for idx in cleanSentence]
	return " ".join(cleanSentence)

pronouns = ['i', 'you', 'he', 'she', 'it', 'we', 'you', 'they', 'me', 'you', 'him', 'her', 'it', 'us', 'them']
fakeSubjects = ['this', 'that']

buckets = buildGroupings() # automatically selects the topic
for b in buckets:
	print "-------------------------------------"
	buck = buckets[b]
	doc = nlp(unicode("".join([a['content'] for a in buck])))
	sentences = {}
	print len(list(doc.sents)), " sentences | ", len(buck), " articles"
	for s in doc.sents:
		sentTxt = " ".join([w.orth_ for w in s])
		subj = ''; dobj = '';
		if s.root.lemma_ not in ['say', 'tell']:
			for w in s:
				if w.head == s.root:
					if w.dep_ == 'nsubj':
						subj = w.orth_
					elif w.dep_ == 'dobj':
						dobj = w.orth_
			if subj != '' and subj.lower() not in pronouns and subj.lower() not in fakeSubjects:
				uid = (subj+" => "+(s.root.lemma_)).lower()
				if uid not in sentences:
					sentences[uid] = []
				sentences[uid].append(sentTxt)
			if dobj != '' and dobj.lower() not in pronouns:
				uid = (s.root.lemma_+" => "+dobj).lower()
				if uid not in sentences:
					sentences[uid] = []
				sentences[uid].append(sentTxt)
	groupByUid = {k: len(sentences[k]) for k in sentences}
	groupByUid = sorted(groupByUid.items(), key=operator.itemgetter(1), reverse=True)[:10]
	print groupByUid
	print "\n".join(sentences[groupByUid[0][0]])