import glob
import os
import nltk

# read in the files into a list

nltk_handles = []

proper_nouns = []

# nltk.download()

os.chdir("texts")
for filename in glob.glob("*.txt"):
    tokens = nltk.wordpunct_tokenize(open(filename, 'r').read())
    nltk_handles.append(tokens)

    words_pos = nltk.pos_tag(tokens)
    nouns = [t for t in words_pos if t[1].startswith('NNP')]

    print(nltk.FreqDist([noun[0] for noun in nouns]))
