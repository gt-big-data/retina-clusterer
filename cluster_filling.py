import time
from db_article_loader import db_get_populated_articles
from classification import vectorize
from cluster_name import cluster_name
from app import insertToCluster
from collections import defaultdict

# This function should be ran every 4 hours in the future (!)
all_articles = db_get_populated_articles()
cleanCategoriesDict = defaultdict(list) #Maps a clean category to a list of articleIDs
for article in all_articles:
    cleanCategory = cluster_name(article[2])
    cleanCategoriesDict[cleanCategory].append(article[3]) #Add the article ID
    
for cleanCategory in cleanCategoriesDict.keys():
    articleIDs = cleanCategoriesDict[cleanCategory]
    insertToCluster(articleIDs, cleanCategory)
