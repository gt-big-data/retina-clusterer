from db import app

art = app.db.cleanarticles.find({ "$query": { "img":  {'$exists': False} }, "$orderby": { 'download_time' : -1 } }).limit(2000)
i = 0
for article in art:
	i += 1
	oldArt = app.db.articles.find_one({"_id": article['_id']})
	img = ''
	if oldArt is not None:
		if len(oldArt['images']) > 0:
			img = oldArt['images'][0]
		app.db.cleanarticles.update({ "_id": article['_id'] },{"$set": {"img": img}})
	print i