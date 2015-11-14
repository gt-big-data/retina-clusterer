from collections import namedtuple
import json
from dbco import * # this imports the db connexion

Article = namedtuple('Article', ['guid', 'title', 'url', 'timestamp', 'source', 'feed', 'content', 'img', 'keywords', 'topic'])
class Article(namedtuple('Article', ['guid', 'title', 'url', 'timestamp', 'source', 'feed', 'content', 'img', 'keywords', 'topic'])):
	def __new__(cls, guid='', title='', url='', timestamp=0, source='', feed='', content='No Content', img='', keywords=[], topic=0):
		return super(Article, cls).__new__(cls, guid, title, url, timestamp, source, feed, content, img, keywords, topic)

def insertArticles(db, As):
	for a in As:
		db.qdoc.update({'guid': a['guid']}, {'$set': a}, upsert=True) # if the GUID is already in the set

def buildArticleArray(articles):
	articleArray = []
	for article in articles:
		if 'title' in article and 'content' in article:
			img = ''
			if 'img' in article:
				img = article['img']
			topic = 0
			if 'topic' in article:
				topic = article['topic']
			if 'keywords' not in article:
				article['keywords'] = []
			a = Article(article['_id'], article['title'], article['url'], article['timestamp'], article['source'], article['feed'], article['content'], img, article['keywords'], topic)
			if isValid(a):
				articleArray.append(a)
	return articleArray

def isValid(a):
	if a.guid == '':
		return False
	if a.title == '':
		return False
	if a.url == '':
		return False
	if a.timestamp < 500:
		return False
	if a.source == '':
		return False
	if a.feed == '':
		return False
	if a.content == '':
		return False
	return True