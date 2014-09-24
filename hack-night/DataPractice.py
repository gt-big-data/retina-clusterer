#Brian Woodbury: Big Data Club 8/29/2014

class Word:
    def __init__(self, word):
        self.word = word
        self.count = 1

    def increaseCount(self):
        self.count += 1

    def show(self):
        return self.word

#initialize text
text = input("Input some text here")
text = text.lower().replace('.','').replace(',','').replace('\"','')
while text.find("  ") != -1:
    text = text.replace("  ", " ")

#takes each word and puts it into a list
words = [""]
index = 0
for i in xrange(0, len(text)):
    if text[i] != ' ':
        words[index] += text[i]
    else:
        index += 1
        words += [""]

#sorts alphabetically
words.sort()

#counts the frequency of each word
data = [Word(words[0])]
for i in xrange(1, len(words)):
    if words[i] == data[len(data) - 1].show():
        data[len(data) - 1].increaseCount()
    else:
        data += [Word(words[i])]

#sorts by frequency (least => most)
sortedData = [Word("")]
n = 1
while len(sortedData) <= len(data):
    for i in xrange(0, len(data)):
        if data[i].count == n:
            sortedData += [data[i]]
    n += 1
del(sortedData[0])

#prints result
file = open("newfile.txt", "w")
file.write("hello world in the new file\n")
for i in xrange(0, len(sortedData)):
    file.write(sortedData[i].show())
    file.write(" count: ")
    file.write(str(sortedData[i].count))
    file.write("\n")
file.close()