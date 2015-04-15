import app
from app import Article
import time
from collections import defaultdict

startFrom = 60
daysAgo = startFrom
totalSum = 0
day2nb = {}
while daysAgo > 0:
	nb = app.getNbArticlesInXDays(daysAgo)
	if daysAgo != startFrom:
		day2nb[daysAgo] = totalSum-nb
	totalSum = nb
	daysAgo = daysAgo - 1
for day, nb in day2nb.iteritems():
    print nb, " articles added ", day, "days ago"