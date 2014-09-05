import os
import operator

os.chdir('/Users/kevin/Documents/hack-night-1-clusterer/texts')
filenames = os.listdir('/Users/kevin/Documents/hack-night-1-clusterer/texts')
for file in filenames:
    f = open(file)

    lines = f.readlines()
    wordList = {}

    for line in lines:
        words = line.split()
        for word in words:
            try:
                wordList[word] += 1
            except KeyError:
                wordList[word] = 1


    sorted_list = sorted(wordList.iteritems(), key=operator.itemgetter(1))
    sorted_list.reverse()
    print(sorted_list)
            
            
    

