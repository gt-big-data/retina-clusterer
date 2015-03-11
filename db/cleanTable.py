import app
from pymongo import MongoClient

def writeArticle(uid, title, text, download_time, category = '', keywords = []):
	if (title == '') | (title is None):
		return -1
	elif text == '':
		return -1
	else:
		app.db.cleanArticles.insert( { "_id": uid, "title": title, "text": text, "download_time": download_time, "category": category, "keywords": keywords } )
def databaseFiller():
	articles = app.getTrainingSet(100, 0)
	for article in articles:
		writeArticle(article.id, article.title, article.text, article.clusterDate, article.category, [])
databaseFiller()