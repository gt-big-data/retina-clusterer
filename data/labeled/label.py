
import json
import os
from bs4 import BeautifulSoup

for filename in os.listdir('raw'):
    article = None
    article_file = os.path.join('raw', filename)
    with open(article_file) as f:
        article = json.load(f)
    html = article['html']
    soup = BeautifulSoup(html)
    nav_on = soup.find(class_='nav-on')
    if nav_on:
        print article_file, nav_on.getText()