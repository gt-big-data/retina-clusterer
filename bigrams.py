import glob
import os

# read in the files into a list

files = []
os.chdir("texts")
for filename in glob.glob("*.txt"):
    f = open(filename, 'r')
    files.append(f.read())

print(files)