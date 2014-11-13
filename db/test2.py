import time
from app import getArticlesByTimeStamp
from db_article_loader import db_get_populated_articles

ts = time.time();
# ts = ts - 9*24*60*60;
ts = 1412802888;
articles= db_get_populated_articles()

# for article in articles['articleArray']:
# 	print str(article['download_date'])+'\n';