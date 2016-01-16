from dbco import *
import random

rand = int(1000*random.random())

art = list(db.qdoc.find().sort('timestamp', -1).skip(300+rand).limit(1))[0]

doc = nlp(unicode(art['content']))

print "SpaCy length: ", len(list(doc.ents))

print "Old length: ", len(art['entities'])

for ent in doc.ents:
	print " ".join([e.orth_ for e in ent])