import os
import operator

os.chdir('C:/Users/svana_000/git/hack-night-1-clusterer/texts')
filenames = os.listdir('C:/Users/svana_000/git/hack-night-1-clusterer/texts')
mainDict = {}
for file in filenames:
    f = open(file)
    fileName = f.name
    lines = f.readlines()
    wordDict = {}
    badWords = {}
    for line in lines:
        words = line.split()
        if words in line:
            line = line.replaceAll('a', '')
        
        for word in words:
            try:
                wordDict[word] += 1
            except KeyError:
                wordDict[word] = 1 

    sorted_list = sorted(wordDict.items(), key=operator.itemgetter(1))
    sorted_list.reverse()
    mainDict[fileName] = sorted_list
     
    print(file)
    for entry in sorted_list:
        print(entry[0] + ' : ' + str(entry[1]))
            
def replaceAll(line, dictionary):
    for i in dictionary.items():
        line = line.replace(i, '');
    return line
            
    

