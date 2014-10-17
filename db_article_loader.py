import time
from db import app
from StringIO import StringIO

def db_get_articles(ts=1):
	"""
	Connects to the database, pulls up articles puts them in a list where:
	articles[i][0] = Title of article
	articles[i][1] = Text in article
	articles[i][2] = Category list
	"""
	articles = app.getArticlesByTimeStamp(ts);

	articles_returned = [];
	for article in articles['articleArray']:
		articles_returned.append((article['title'], article['text'], article['categories']));
	return articles_returned