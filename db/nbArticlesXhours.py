import time
from app import getArticlesByTimeStamp

while(True):
	ts = time.time();
	ts = ts - int(raw_input('Number of articles in the last X hours?'))*60*60;
	articles = getArticlesByTimeStamp(ts);
	print len(articles), ' articles';