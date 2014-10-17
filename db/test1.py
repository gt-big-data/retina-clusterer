import time
from app import getArticlesByTimeStamp

ts = time.time();
# ts = ts - 9*24*60*60;
ts = 1412802888;

articles = getArticlesByTimeStamp(ts);
print(len(articles['articleArray']));

# for article in articles['articleArray']:
# 	print str(article['download_date'])+'\n';