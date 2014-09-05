# f = file
def wordCounter(f):
	words_read = {}
	for w in f.read().split():
		if w not in words_read:
			words_read[w] = 1
		else:
			words_read[w] = words_read[w] + 1
	print(w, words_read)
# end