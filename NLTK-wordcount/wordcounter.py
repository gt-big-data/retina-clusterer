import nltk
from collections import defaultdict
# f = file
def wordCounter(f):

	words_read = defaultdict(int);
	for line in f:
		for sentence in nltk.sent_tokenize(line):
			for word in nltk.word_tokenize(sentence):
				words_read[word] += 1;
	words_read = sorted(words_read.items(), key=lambda x: -x[1]);
	print(words_read)
