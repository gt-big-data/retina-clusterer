# -*- coding: utf-8 -*-
from dbco import *
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

token = "“"

count = db.qdoc.find({'content': {'$regex': token}}).count()

while count > 0:
	qdocUpdate = db.qdoc.initialize_unordered_bulk_op()

	art = list(db.qdoc.find({'content': {'$regex': token}}).sort('timestamp', -1).limit(100))
	for a in art:
		oldCont = a['content'].encode('utf-8')
		# print oldCont
		# print "----------------------------------"
		newContent = oldCont.replace("’", "'").replace("”", '"').replace("“", '"').replace('—', '-').replace('‘', "'")
		# print newContent
		qdocUpdate.find({'_id': a['_id']}).upsert().update({'$set': {'content': newContent}})
	qdocUpdate.execute()
	count = db.qdoc.find({'content': {'$regex': token}}).count()
	print count