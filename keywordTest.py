from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from dbco import *
import time, copy
import numpy as np

longAgo = time.time()-30*24*60*60
training = list(db.qdoc.find({'timestamp': {'$lte': longAgo}}).sort('timestamp', -1).limit(300))
trainingContent = [a['content'] for a in training]
trainLemmas = []
for cont in trainingContent:
	doc = nlp(unicode(cont))
	trainLemmas.append(" ".join([w.lemma_ for w in doc]))

art = list(db.qdoc.find().sort('timestamp', -1).limit(100)) #{'$exists': True}

testTitle = [a['title'] for a in art]
testingContent = [a['content'] for a in art]
testLemmas = []
for cont in testingContent:
	doc = nlp(unicode(cont))
	testLemmas.append(" ".join([w.lemma_ for w in doc]))

oldKeywords = [a['keywords'] for a in art]

totalText = copy.copy(testLemmas); totalText.extend(trainLemmas)

count_vect = CountVectorizer(stop_words='english'); tfidf_trans = TfidfTransformer()
tfidf = tfidf_trans.fit_transform(count_vect.fit_transform(totalText))

vocab = {v: k for k,v in count_vect.vocabulary_.items()}

for i in range(len(testingContent)):
	myTfidf = tfidf[i, :].toarray()
	bestWordI = np.argsort(myTfidf)[0][-10:][::-1]
	bestWord = [vocab[j] for j in bestWordI]
	print "-------------------------------------------"
	print testTitle[i].encode('utf-8')
	print ", ".join(oldKeywords[i])
	print ', '.join(bestWord)
	print "-------------------------------------------"