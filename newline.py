import pymongo

class NewLineDetector():

    def __init__(self):
        self.m = pymongo.MongoClient("146.148.59.202", 27017)
        self.db = self.m.big_data

    def detectNewLineChars(self):
        cursor = self.db.cleanarticles.find()
        num = 0
        art = 0
        for doc in cursor:
            text = doc["text"]
            textList = text.split(".")
            if len(textList) < 3:
                num += 1
                if (art < 67):
                    print(text)
                    art += 1
        return num

n = NewLineDetector()
x = n.detectNewLineChars()
print "Number of articles with less than 3 sentences is", x

