import os
import json
from StringIO import StringIO
"""
loads the text files that have been crawled.
"""

LABELS_PATH = 'labels.txt'

def get_articles():
    """
    :param dir_path: the directory that contains the articles
    :return: a list of 2-tuples of labeled training data: (article_json, label)
    """
    articles = []
    with open(LABELS_PATH, 'r') as f:
        lines = f.readlines()
        for line in lines:
            splits = line.split()
            filepath, label = splits[0], ' '.join(splits[1:])  # handling labels have spaces within them.
            with open(filepath, 'r') as sub_file:
                article_text = json.load(StringIO(sub_file.read()))
                articles.append((article_text, label))

    return articles

