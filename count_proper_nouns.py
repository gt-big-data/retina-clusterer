# Produces a list like this:
# ==========================
# <FreqDist: 'Apple': 12, 'iCloud': 6, 'Cook': 4, 'Journal': 3, 'CNNMoney': 2, '(': 1, ')': 1, 'AAPL': 1 ...>
# <FreqDist: 'Apple': 15, 'Catcher': 6, 'China': 6, 'Dell': 5, 'Labor': 5, 'CLW': 4, 'Foxconn': 3 ...>
# <FreqDist: 'Earth': 9, 'NASA': 5, 'Asteroid': 2, 'Chelyabinsk': 2, '(': 1, ')': 1, '.)': 1, '/': 1, ...>
# <FreqDist: 'iPhone': 20, 'Apple': 13, 'C': 2, 'Cook': 2, 'Dediu': 2, 'Get': 2, 'Related': 2, ...>
# <FreqDist: 'HHS': 3, 'Obamacare': 3, 'Department': 2, 'Internet': 2, 'Thursday': 2, 'Age': 1 ...>

import glob
import os
import nltk



nltk_handles = []
proper_nouns = []

# dowload nltk packages
# nltk.download()

# read in the files into a list
os.chdir("texts")
for filename in glob.glob("*.txt"):
    tokens = nltk.wordpunct_tokenize(open(filename, 'r').read())
    nltk_handles.append(tokens)

    words_pos = nltk.pos_tag(tokens)
    nouns = [t for t in words_pos if t[1].startswith('NNP')]

    print(nltk.FreqDist([noun[0] for noun in nouns]))