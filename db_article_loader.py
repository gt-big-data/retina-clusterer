import time
from db import app
from StringIO import StringIO

def db_get_populated_articles(ts=1):
	"""
	Connects to the database, pulls up articles puts them in a list where:
	articles[i][0] = Title of article
	articles[i][1] = Text in article
	articles[i][2] = Category list
	"""
	articles = app.getPopulatedArticlesByTimeStamp(ts)
	articles_returned = []
	for article in articles['articleArray']:
		articles_returned.append((article['title'], article['text'], article['categories']))
	return articles_returned

def db_get_article_count(ts=1):
	"""
	Gets the number of entries in the database
	May later be changed to count of full article entries
	Early entries are not fully populated
	"""
	articles = app.getPopulatedArticlesByTimeStamp(ts)
	return len(articles['articleArray'])

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