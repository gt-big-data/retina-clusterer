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
	articles = app.getPopulatedArticlesByTimeStamp(ts,limit);
	articles_returned = [];
	for article in articles['articleArray']:
		articles_returned.append((article['title'], article['text'], article['categories']))
	return articles_returned

def db_get_populated_articles_count(ts=1):
	"""
	Counts the number of useful articles (most recent version, populated articles)
	"""
	return app.getPopulatedArticlesCount(ts)

def db_get_all_articles_count(ts=1):
	"""
	Counts the number of articles (or entries) in the database
	"""
	return app.getAllArticlesCount(ts)

def db_get_all_articles(ts=1):
	"""
	Connects to the database, pulls up ALL entries found in the database
	If present (None if not present):
	articles[i][0] = Title of article
	articles[i][1] = Text in article
	articles[i][2] = Category list
	"""
	articles = app.getAllArticlesByTimeStamp(ts)

	articles_returned = []
	for article in articles['articleArray']:

		title = None
		text = None
		categories = None
		if ("title" in article.keys()):
			title = article['title']
		if ("text" in article.keys()):
			text = article['text']
		if ("categories" in article.keys()):
			categories = article['categories']
		
		articles_returned.append((title, text, categories))
	return articles_returned
