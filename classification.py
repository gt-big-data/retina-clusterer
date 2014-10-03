import nltk
import string
import os

from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

from article_loader import get_articles
"""
Supervised Learning:
- Testing with 10 fold cross-validation:
    - splitting the training into train and test sets (9:1)
    - averaging performance across all 10 test sets (in the 10 iterations) and using the result as test_accuracy.

"""
def vectorize(article_texts):
    """
    :param article_texts: a list of article texts
    :return: (vectorized_matrix, tfidf_vectorizer)
    """
    stemmer = PorterStemmer()

    # following
    def stem_tokens(tokens, stemmer):
        stemmed = []
        for item in tokens:
            stemmed.append(stemmer.stem(item))
        return stemmed

    def tokenize(text):
        tokens = nltk.word_tokenize(text)
        stems = stem_tokens(tokens, stemmer)
        return stems

    tfidf_vectorizer = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    mat = tfidf_vectorizer.fit_transform(article_texts)

    return (mat, tfidf_vectorizer)



# Testing:
articles_labels = get_articles()
articles = [article[0]['text'] for article in articles_labels]
labels = [article[1] for article in articles_labels]
print vectorize(articles)


