import os
"""
loads the text files that have been crawled.
"""

# Waiting for access to the crawled files... till then, let's work on some sample articles:

current_directory = os.getcwd()
TEXT_DIR = current_directory + '/texts/'


def get_articles(dir_path=TEXT_DIR):
    """
    :param dir_path: the directory that contains the articles
    :return: article strings as list
    """
    sample_articles = os.listdir(dir_path)
    articles = []
    for article in sample_articles:
        path = TEXT_DIR + article
        with open(path, 'r') as f:
            article_string = f.read()
            articles.append(article_string)
    return articles




