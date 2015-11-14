from dbco import db

def article_tweets(articleID, num_days):
    article = db.qdoc.find_one({"_id" : articleID})
    topic = article["topic"]
    if topic:
        keywords = article["keywords"]
        article_timestamp = article["timestamp"]
        day_in_ms = 86400000
        query = {"words" : {"$in" : keywords}, "$and" : [{"timestamp" : {"$gte" : article_timestamp - num_days*day_in_ms}}, {"timestamp" : {"$lte" : article_timestamp + num_days*day_in_ms}}]}
        aggregate_query = [{"$match" : query}, {"$project" : {"intersect" : {"$size": {"$setIntersection" : ["$words", keywords]}}, "text" : 1, "author" : 1, "timestamp" : 1, "hashtags" : 1}}, {"$match" : {"intersect" : {"$gte" : 2}}}]
        tweets = db.tweet.aggregate(aggregate_query)
        for tweet in tweets:
            tweet_id = tweet["_id"]
            query = {"_id" : topic}
            update = {"$addToSet" : {"related_tweets" : [tweet_id]}}
            db.topic.update(query, update)

def find_related_tweets(articles, time_interval):
    for a in articles:
        article_tweets(a["_id"], time_interval)