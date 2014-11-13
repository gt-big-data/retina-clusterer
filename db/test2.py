import time
from db_article_loader import db_get_populated_articles
from db import app

print app.getClusterArticleCount('Sports')
# for article in articles['articleArray']:
# 	print str(article['download_date'])+'\n';