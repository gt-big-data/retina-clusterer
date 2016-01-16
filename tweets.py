from dbco import db

def article_tweets(articleID, num_days):
    article = db.qdoc.find_one({"_id" : articleID})
    try:
        topic = article["topic"]
        print topic
        keywords = article["keywords"]
        article_timestamp = article["timestamp"]
    except KeyError:
        print "Article doesn't have a topic"
        return
    day_in_ms = 86400000
    query = {"words" : {"$in" : keywords},
        "$and" : [{"timestamp" : {"$gte" : article_timestamp - num_days*day_in_ms}},
        {"timestamp" : {"$lte" : article_timestamp + num_days*day_in_ms}}]}
    aggregate_query = [{"$match" : query},
        {"$project" : {"intersect" : {"$size": {"$setIntersection" : ["$words", keywords]}}, "text" : 1, "author" : 1, "timestamp" : 1, "hashtags" : 1}},
        {"$match" : {"intersect" : {"$gte" : 2}}}]
    tweets = db.tweet.aggregate(aggregate_query)
    for tweet in tweets:
        tweet_id = tweet["_id"]
        query = {"_id" : topic}
        update = {"$addToSet" : {"related_tweets" : tweet_id}}
        db.topic.update(query, update)

def find_related_tweets(articles, time_interval):
    for a in articles:
        article_tweets(a["_id"], time_interval)

def run_on_sample(gt, lt):
    articleCursor = db.qdoc.find({"$and" : [{"timestamp": {"$gte" : gt}}, {"timestamp" : {"$lte" : lt}}]})
    find_related_tweets(articleCursor, 2)

run_on_sample(1447128143, 1447138143)