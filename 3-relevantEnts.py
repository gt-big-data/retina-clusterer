from dbco import *
from datetime import datetime, timedelta

earliest = datetime.utcnow() - timedelta(hours=1)

match = {'$match': {'timestamp': {'$gte': earliest}}}
unwind = {'$unwind': '$entities'}
matchNeNull = {'$match': {'entities.wdid': {'$ne': None}}}
group = {'$group': {'_id': '$entities.wdid', 'count': {'$sum': 1}}}
sort = {'$sort': {'count': -1}}
limit = {'$limit': 50}
lookup = {'$lookup': {'from': 'entities', 'localField': '_id', 'foreignField': '_id', 'as': 'pop'}}
project1 = {'$project': {'_id': 1, 'count': 1, 'aliases': {'$arrayElemAt': ['$pop.aliases', 0]}, 'title': '$pop.title'}}
project2 = {'$project': {'_id': 1, 'count': 1, 'title': 1, 'aliases': {'$ifNull': ['$aliases', []]}, 'myNames': {'$concatArrays': [{'$ifNull': ['$aliases', []]}, '$title']}}}
unwindNames = {'$unwind': '$myNames'}
groupFinal = {'$group': {'_id': 0, 'finalArray': {'$push': '$myNames'}}}

names = list(db.qdoc.aggregate([match, unwind, matchNeNull, group, sort, limit, lookup, project1, project2, unwindNames, groupFinal]))[0]['finalArray']

db.relevant_ents.insert({'entities': names, 'datetime': datetime.utcnow()})