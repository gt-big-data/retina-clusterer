import time
from db_article_loader import db_get_populated_articles
from classification import vectorize

# This function should be ran every 4 hours in the future (!)
all_articles = getPopulatedArticlesByTimeStamp()
test_data = [];