import time
from db_article_loader import db_get_articles

ts = time.time();
ts = ts - 9*24*60*60;
# ts = 1412802888;

clean_articles = db_get_articles(ts);
for article in clean_articles:
	if article[2] != None:
		print ' '.join(article[2])+'\n';