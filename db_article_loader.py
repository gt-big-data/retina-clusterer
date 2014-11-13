import time
from db import app
from StringIO import StringIO

def db_get_populated_articles(ts=1, limit=10000):
	"""
	Connects to the database, pulls up the recent version of articles puts them in a list where:
	articles[i][0] = Title of article
	articles[i][1] = Text in article
	articles[i][2] = Category list
	"""
	count= 0
	articles = app.getPopulatedArticlesByTimeStamp(ts,limit);
	articles_returned = [];
	for article in articles['articleArray']:
		if (count < 1):
			print article
			count = count+ 1
		articles_returned.append((article['title'], article['text'], article['categories'], article['_id']))
	return articles_returned

def db_get_populated_articles_count(ts=1):
	"""
	Counts the number of useful articles (most recent version, populated articles)
	"""
	return app.getPopulatedArticlesCount(ts)


def db_get_unique_categories(ts=1):
	"""
	Returns a list of unique categories in the DB
	"""
	listCat = set([]);
	articles = app.getPopulatedArticlesByTimeStamp(ts,1000)
	for article in articles['articleArray']:
		listCat.add(article['categories'][0]);

	return listCat;