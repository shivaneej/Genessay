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

def makeMatrix(matrixDict, uniqueNGrams):
    for rowname in matrixDict.keys():
        row = matrixDict.get(rowname)
        cols = row.keys()
        for ngram in uniqueNGrams:
            if ngram not in cols:
                row[ngram] = 0
        matrixDict[rowname] = row

def saveMatrix(filename, matrixDict, uniqueNGrams):
    csvfile = open(filename, 'w',newline='')
    row = [" "]
    row.extend(list(uniqueNGrams))
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(row)
    for rowname in uniqueNGrams:
        row = [rowname]
        row.extend([matrixDict[rowname].get(col) for col in uniqueNGrams])
        filewriter.writerow(row)

def wordContext(listNGrams, uniqueNGrams, matrixDict):
    n = len(listNGrams)
    uniqueNGrams |= set(listNGrams)
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


def updateMatrices(data_dir):
    DATASET_FILE = data_dir + DATASET_FILENAME
    for i in range(N):
        sample_file = open(DATASET_FILE, 'r', encoding='utf-8')
        data = sample_file.read()
        samples = list(data.split("\n\n"))
        matrixDict = {}
        uniqueNGrams = set()
        for sample in samples:
            listNgrams = extractNGrams(sample, i + 1)
            matrixDict = wordContext(listNgrams, uniqueNGrams, matrixDict)
        makeMatrix(matrixDict, uniqueNGrams)
        saveMatrix(data_dir + '/' + OP_FILE_NAMES[i], matrixDict, uniqueNGrams)


DATASET_FILENAME = '/og.txt'
OP_FILE_NAMES = ['unigrams.csv', 'bigrams.csv', 'trigrams.csv']
N = len(OP_FILE_NAMES)