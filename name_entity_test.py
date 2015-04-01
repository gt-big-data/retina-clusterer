import nltk

#with open('Test_Articles/Fairly bad pitcher traps triumph in the end.txt', 'r') as f:
with open('Test_Articles/American held by ISIS.txt', 'r') as f:
    sample = f.read()

sentences = nltk.sent_tokenize(sample.encode('utf-8')) #seperate into sentences
tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences] #seperate into words
tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences] #add part of speech to each word
chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True) #turn list into tree

nameEntity = []
for sentence in chunked_sentences:
    for part in sentence: #part is tuple or tree
        if type(part) is nltk.Tree: #name entities are only in trees
            listNNP = part.leaves()
            entity = ""
            for tupleNNP in listNNP: #turn tree into entity
                entity += " "
                entity += tupleNNP[0]
            entity = entity[1:]
            nameEntity.append(entity) #add entity to list
nameEntity = list(set(nameEntity))
print nameEntity
