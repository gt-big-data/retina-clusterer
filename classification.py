import nltk
import string
import os
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
import numpy as np

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


def cross_validation(clf, X, Y, num_folds=10):
    """
    :param clf: a classifier to use for training (eg. SVM / MultinomialNaiveBayes ...)
    :param X: vectors
    :param Y: labels
    :return: accuracy as the average of 10-fold cross-validation.
    """
    X = X.todense()
    fold_size = len(X) / num_folds
    i = 0
    accs = []
    for fold in xrange(num_folds):
        test_mat = X[i*fold_size : (i+1)*fold_size]
        test_labels = Y[i*fold_size : (i+1)*fold_size]

        train_mat = X[0:i*fold_size].tolist() + X[(i+1)*fold_size::].tolist()
        train_labels = Y[0:i*fold_size] + Y[(i+1)*fold_size::]
        clf.fit(train_mat, train_labels)
        predicted_labels = clf.predict(test_mat)

        # finding accuracy:
        correct = 0
        for predicted, true in zip(predicted_labels, test_labels):
            if predicted == true:
                correct += 1
        acc = float(correct) / float(len(predicted_labels))
        accs.append(acc)

    return np.mean(accs)