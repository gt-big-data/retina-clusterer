import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB


categories = ['soc.religion.christian', 'alt.atheism', 'talk.religion.misc', 'talk.politics.mideast', 'rec.motorcycles'];

twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42);

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)


tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

docs_new = ['God is and Jesus are religion', 'I love my bike, it\'s got a great engine', 'Lebanon and Syria ... Peace and love', 'My bike is a god from Lebanon']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
	print('%r => %s' % (doc, twenty_train.target_names[category]))



# raw_input('Press enter to go to the accuracy testing:')

# test_data = fetch_20newsgroups(subset='test',categories=categories, shuffle=True, random_state=42);
# count_vect2 = CountVectorizer()
# test_count = count_vect2.fit_transform(test_data.data);

# tfidf_transformer2 = TfidfTransformer()
# test_tfidf = tfidf_transformer2.fit_transform(test_count);

# clf = MultinomialNB().fit(test_tfidf, test_data.target)

# predicted = clf.predict(test_tfidf);
# dd = np.mean(predicted == test_data.target);
# print(dd);

raw_input('Press enter to exit...')