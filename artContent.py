from bson.objectid import ObjectId
from dbco import *
import sys

if len(sys.argv) > 1:
	idT = sys.argv[1]
	art = list(db.qdoc.find({'_id': ObjectId(idT)}).limit(1))[0]

	print art['source']
	print "--------------------------------"
	print art['content'].encode('utf-8')