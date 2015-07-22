from dbco import *

for t in range(1,1200):
	c = db.qdoc.find({'topic': t}).count()
	if c > 30:
		arts = db.qdoc.find({'$query': {'topic': t}, '$orderby': {'timestamp': 1}})
		print t, "| ", c ," articles | length in days: ", float((arts[c-1]['timestamp']-arts[0]['timestamp'])/86400), " days"

# t = 140
# arts = db.qdoc.find({'$query': {'topic': t}, '$orderby': {'timestamp': 1}})
# for a in arts:
# 	print a['title'], " | ", a['guid']