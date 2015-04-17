import nltk
from db import app

def getNameEntities(text):
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    nameEntity = []
    for sentence in chunked_sentences:
        for part in sentence:
            if type(part) is nltk.Tree:
                listPN = part.leaves()
                entity = ""
                for tuplePN in listPN:
                    entity += " "
                    entity += tuplePN[0]
                entity = entity[1:]
                nameEntity.append(entity)
    nameEntity = list(set(nameEntity))
    return nameEntity

articles = app.getLatestCleanArticles(5)
articleNumber = 2
print articles[articleNumber][0], "\n\n", getNameEntities(articles[articleNumber][1])
