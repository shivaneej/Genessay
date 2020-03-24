import csv
import re
from nltk.util import ngrams
import numpy as np

def extractNGrams(sentence,n):
  sentence = sentence.lower()
  sentence = re.sub(r'[^a-zA-Z0-9\s]', ' ', sentence)
  tokens = [token for token in sentence.split(" ") if token != ""]
  output = list(ngrams(tokens,n))
  NGrams = ['_'.join(t.strip() for t in tup) for tup in output]
  return NGrams

def makeMatrix():
    for rowname in matrixDict.keys():
        row = matrixDict.get(rowname)
        cols = row.keys()
        for ngram in uniqueNGrams:
            if ngram not in cols:
                row[ngram] = 0
        matrixDict[rowname] = row



def saveMatrix(filename):
    # print(uniqueNGrams)
    csvfile = open(filename, 'w',newline='')
    row = [" "]
    row.extend(list(uniqueNGrams))
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(row)
    for rowname in uniqueNGrams:
        row = [rowname]
        row.extend([matrixDict[rowname].get(col) for col in uniqueNGrams])
        filewriter.writerow(row)

def wordContext(listNGrams, uniqueNGrams):
    n = len(listNGrams)
    uniqueNGrams |= set(listNgrams)
    for i in range(n-1):
        current = listNGrams[i] 
        nextWord = listNGrams[i+1]
        row = matrixDict.get(current, {})
        cell = row.get(nextWord,0)
        row[nextWord] = cell + 1
        matrixDict[current] = row
        row = matrixDict.get(nextWord, {})
        cell = row.get(current,0)
        row[current] = cell + 1
        matrixDict[nextWord] = row
    return matrixDict


leaveSamples=open('Keywords - Leave Samples.csv')

csvReader = csv.reader(leaveSamples)
matrixDict = {}
uniqueNGrams = set()
for row in csvReader:
    sent = row[0]
    listNgrams = extractNGrams(sent,1)
    matrixDict = wordContext(listNgrams, uniqueNGrams)
makeMatrix()
saveMatrix("unigrams.csv")

