from article_loader import get_articles
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
"""
Load articles into memory and run sci-kit learn's nmf topic modeling algorithm on them:
"""

articles = get_articles()

# tfidf vectorizing:
vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=2000,
                             stop_words='english')