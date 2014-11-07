import os
import json
from StringIO import StringIO
"""
loads the text files that have been crawled.
"""


def get_articles(which=1):
    """
    Which tells it whether you want to load full file or smaller label file
    :param dir_path: the directory that contains the articles
    :return: a list of 2-tuples of labeled training data: (article_json, label)
    """
    if(which == 1):
        LABELS_PATH = 'data/labeled/labels.txt'
    else:
        LABELS_PATH = 'data/labeled/labels_small.txt'

    articles = []
    with open(LABELS_PATH, 'r') as f:
        lines = f.readlines()
        for line in lines:
            splits = line.split()
            filepath, label = splits[0], ' '.join(splits[1:])  # handling labels have spaces within them.
            with open('data/labeled/'+filepath, 'r') as sub_file:
                article_text = json.load(StringIO(sub_file.read()))
                articles.append((article_text, label))

    return articles

def get_test_data():
    """
    :return: a list of article text
    """
    articles = []
    for filename in os.listdir('data/test'):
        with open('data/test/'+filename, 'r') as f:
            articles.append([filename, f.read()]);
    return articles