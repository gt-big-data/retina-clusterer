import time
from db import app
from StringIO import StringIO
from collections import namedtuple

Article = namedtuple('Article', ['title', 'text', 'categories', 'id'])

def db_get_populated_articles(ts=1, limit=10000):
	"""
	Connects to the database, pulls up the recent version of articles puts them in a list where:
	articles[i][0] = Title of article articles[i].title
	articles[i][1] = Text in article articles[i].text
	articles[i][2] = Category list articles[i].categories
	articles[i][3] = MongoDB ID articles[i].id
	"""
	articles = app.getArticlesByTimeStamp(ts,limit);
	articles_returned = [];
	for article in articles['articleArray']:
		articles_returned.append(Article(article['title'], article['text'], article['categories'], article['_id']))
	return articles_returned

def db_get_populated_articles_count(ts=1):
	"""
	Counts the number of useful articles (most recent version, populated articles)
	"""
	return app.getArticlesCount(ts)