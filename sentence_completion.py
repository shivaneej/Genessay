import numpy as np
from copy import copy, deepcopy
from itertools import *
import re
from numpy import array
import nltk
import csv
import nltk
import spacy
import time
import pandas as pd

unigrams = 'dataset/unigrams.csv'
bigrams = 'dataset/bigrams.csv'
trigrams = 'dataset/trigrams.csv'

class Matrix:
    def __init__(self, filename):
        #optimised
        self.filename = filename
        self.mat = []     
        self.row_index = {}  
        dataframe = pd.read_csv(filename, chunksize = 10**8)
        df_list = [] 
        for df in dataframe: 
            index = 0
            for name in df[' ']:
                self.row_index[name] = index
                index += 1
            df_list += [df.copy()] 
        df_final = pd.concat(df_list)
        self.rownames = df_final[' '].to_list()
        dataframe = df_final.drop([' '], axis = 1)
        self.mat = dataframe.to_numpy()
        self.colnames = list(df.columns)

    def get_word_index(self, word):
        return self.row_index.get(word, -1)

    def get_value(self, i1, i2):
        return self.mat[i1, i2]
          
def generation(options_list):
    nlp = spacy.load('en_core_web_sm')
    dependency_list = []
    pos_list = []
    for options in options_list:
        no_br_text_options = []
        for sent in options: 
            t = sent.replace("[","")
            t = t.replace("]","")
            no_br_text_options.append(t) 
        loc_dep_list = []
        loc_pos_list = []
        for x in range(len(no_br_text_options)): 
            doc = nlp(no_br_text_options[x])
            st = ""
            #pos
            for w in doc:
                st += str(w.text+"_"+w.tag_+" ")
                loc_pos_list.append(st)
            #dependency string generation
            dep_string = ""
            for token in doc:
                if token.dep_=="ROOT":
                    dep_string += str("NULL_"+token.text+" ") 
                elif token.dep_=="pobj":
                    dep_string += str(token.text+"_"+token.head.text+" ") 
                elif token.dep_!="punct":
                    dep_string += str(token.head.text+"_"+token.text+" ") 
                if dep_string != '':
                    loc_dep_list.append(dep_string)
        dependency_list.append(loc_dep_list)
        pos_list.append(loc_pos_list)  
    return dependency_list, pos_list

def pmi(m, positive=False, discounting=False):
    # maplist = [[inner for inner in outer.tolist()] for outer in m.mat]
    # print(maplist)
    # p = maplist/ np.sum(maplist, axis=None)
    p = m.mat/ np.sum(m.mat, axis=None)
	
    # PMI with positive option:
    colprobs = np.sum(p, axis=0)
    np_pmi_log = np.vectorize((lambda x : pmi_log(x, positive=positive)))
    p = array([np_pmi_log(row / (np.sum(row)*colprobs)) for row in p])
    if discounting:
        colsums = np.sum(m.mat, axis=0)
        fmatrix = m.mat / (m.mat + 1)
        dmatrix = array([pmi_discount(row, colsums) for row in m.mat])        
        p *= fmatrix * dmatrix
    reweighted = copy(m)
    reweighted.mat = p
    return reweighted    

    
def pmi_log(x, positive=False):
    if (x <= 0.0): 
        return 0.0
    else:
        x = np.log2(x)
        if (positive and x < 0.0):
            x = 0.0
        return x

def pmi_discount(row, colsums):
    mincontext = np.minimum(np.sum(row), colsums)
    return mincontext / (mincontext + 1)

def get_stopwords(sentence):
    pos_to_remove = ('dt','prp','prp$','cc','nnp','nnps') #pos to remove
    stopwords = []
    tokens = sentence.strip().split(" ")
    for token in tokens:
        words = token.split("_")
        tokens = nltk.word_tokenize(words[0])
        t = tokens[0].lower().strip()
        tokens = nltk.word_tokenize(words[1])
        pos = tokens[0].lower().strip()
        if (pos in pos_to_remove):
            stopwords.append(t) 
    return stopwords
    
def get_dependencies(option, sentence): #relation with blank 
    reln_with_blank = set()
    tokens = sentence.strip().split(" ")
    for token in tokens:
        words = token.split("_")
        tokens = nltk.word_tokenize(words[0])
        first_word = tokens[0].lower().strip()
        tokens = nltk.word_tokenize(words[1])
        second_word = tokens[0].lower().strip()
        if(first_word == option or second_word == option):
            if(first_word != option and first_word != "null"):
                reln_with_blank.add(first_word)
            if(second_word != option and second_word != "null"):
                reln_with_blank.add(second_word)
    return list(reln_with_blank)

def get_option_score(p, options, features, named_entities): #pmi score for option
    option_score = 0.0
    for option in options:
        for feature in features:   
            option_entity = named_entities.get(option)
            t = time.time()    
            feature_word_index = p.get_word_index(feature)
            option_index = p.get_word_index(option)
            print("Searching time", time.time() - t)
            if (feature_word_index != -1 and option_index != -1):
                pmi = p.get_value(feature_word_index, option_index)
                option_score += pmi              
    return option_score


def predict_blank(p, ngram_type, questions, options, dependencies, parts_of_speech, input_keywords, named_entities):
    guesses = []
    pmi_scores = []
    results = {}
    for i in range(0, len(questions)): 
        features = get_tokens(questions[i], ngram_type) 
        reduced_context = deepcopy(features)
        if (ngram_type != 'unigram'):
            features = get_ngrams(features, ngram_type)
        keywords = get_keywords(ngram_type, input_keywords[i][0]) 
        features += keywords
        if(ngram_type == 'unigram'):
            dependent_words = get_dependencies(options[0], dependencies[i][0])
            features += dependent_words
            stopwords = get_stopwords(parts_of_speech[i][0]) 
            reduced_context = filter(lambda x: x not in stopwords, reduced_context)
            features = filter(lambda x: x not in stopwords, features)
        features = list(features)
        best_guess = ""
        max_score = 0.0    
        scores = []  
        for j in range(len(options)):
            option = options[j]
            if (ngram_type == 'unigram'):
                    option_entity = named_entities.get(option)
                    ngram_score = get_option_score(p, [option_entity], features, named_entities)
            elif (ngram_type == 'bigram'):
                    ngrams_options = get_options_ngrams(option, features, named_entities)
                    ngram_score = get_option_score(p, ngrams_options, features, named_entities)     
                    ngram_score += unigram_scores[i][j]
            else:
                    ngrams_options = get_options_ngrams(option, features, named_entities)
                    ngram_score = get_option_score(p, ngrams_options, features, named_entities)   
                    ngram_score += unigram_bigram_scores[i][j]                  
            scores.append(ngram_score)
            if (ngram_score > max_score):
                    max_score = ngram_score
                    best_guess = option
            if (ngram_type == 'unigram'):
                    unigram_scores[i] = scores
            if (ngram_type == 'bigram'):
                    unigram_bigram_scores[i] = scores     
        pmi_scores.append(max_score)
        results[questions[i]] = best_guess
    return results         

def get_tokens(text, ngram_type):
    words = []
    tokens = nltk.word_tokenize(text)   
    for t in tokens:
        t = t.strip().lower()
        if (ngram_type == 'unigram'):
            if (t not in PUNCTUATION and t not in words):
                words.append(t)
        else:
            words.append(t)
    return words   

def get_ngrams(tokens, ngram_type): #generate n grams from tokens
    ngrams = []
    if (ngram_type == 'bigram'):
        words = zip(tokens, tokens[1:])
    elif (ngram_type == 'trigram'):
        words = zip(tokens, tokens[1:], tokens[2:])
    for ngram in words:
        result = ""
        for w in ngram:
            result += w.lower().strip() + "_"
        result = result[:-1]
        ngrams.append(result)
    return ngrams

def get_keywords(ngram_type, wordList): #form n gram keywords
    keywords = []
    words = wordList.split(",")
    for w in words:
        tokens = nltk.word_tokenize(w)
        if (ngram_type == 'unigram'):
            for t in tokens:
                keywords.append(t.lower().strip())
        else:
            ngrams = get_ngrams(tokens, ngram_type) 
            for n in ngrams:
                keywords.append(n)
    return keywords

def get_options_ngrams(option, ngrams, named_entities): #extract n grams containing blank
    ngrams_options = []
    option_entity = named_entities.get(option,None)
    for n in ngrams:
        if(re.findall("~", n)):
            result = re.sub("~", str(option_entity), n) 
            ngrams_options.append(result)
    return ngrams_options 


def process_text_options(sentences, options):
    final_list = []
    for sentence in sentences:
        text_options = []
        for option in options:
            text_options.append(re.sub("~", '['+str(option)+']', str(sentence)))
        final_list.append(text_options)
    return final_list

def split_blanks(sentences, keywords_list):
    splitted_sentences = []
    new_keywords_list = []
    num_sentences = len(sentences)
    for i in range(num_sentences):
        sentence = sentences[i]
        keywords = keywords_list[i]
        if(sentence[0] == "~"):
            sentence = " " + sent
        splitted_list = sentence.split("~")
        count = len(splitted_list)
        for j in range(count):
            if sentence[0] != "~" and j != count - 1:
                splitted_sentences.append((splitted_list[j] + "~" + splitted_list[j + 1]).strip())
                new_keywords_list.append(keywords)
    return splitted_sentences, new_keywords_list

PUNCTUATION = (';', ':', ',', '.', '!', '?','(',')',"'", '~')
unigram_scores = {}
unigram_bigram_scores = {}
def complete_sentences(sentences_to_fill, keywords_list, named_entities, unigram_mat, bigram_mat, trigram_mat):
    #sentences_to_fill is a list of strings
    #keywords_list is list of list of one string
    #named_entities is a dictionary
    print(named_entities)
    sentences_to_fill = [sentence for sentence in sentences_to_fill if '~' in sentence]
    sentences_to_fill, keywords_list = split_blanks(sentences_to_fill, keywords_list)
    options = list(named_entities.keys())
    text_options = process_text_options(sentences_to_fill, options)
    dependencies, parts_of_speech = generation(text_options)
    print(sentences_to_fill)
    print(keywords_list)
    predict_blank(unigram_mat, 'unigram', sentences_to_fill, options, dependencies, parts_of_speech, keywords, named_entities)
    predict_blank(bigram_mat, 'bigram', sentences_to_fill, options, dependencies, parts_of_speech, keywords, named_entities)
    return predict_blank(trigram_mat, 'trigram', sentences_to_fill, options, dependencies, parts_of_speech, keywords, named_entities)



# print(complete_sentences(['My name is ~ working in ~'], [['studying']], {'Rohan Solsi': 'PERSON', 'KJSCE': 'ORG', '1611005': 'CARDINAL', 'Tuesday': 'DATE', 'typhoid': 'NORP'}))

# print(complete_sentences(['I am ~ studying in ~.', 'My roll no.', 'I, ~, was not able to come college from ~ as i was suffering from typhoid fever and liver infection.', 'Respectfully, I am here to inform you that, I am suffering from fever since last night.', 'I request you to accept this medical application.'], [['studying'], ['come', 'college']], {'Rohan Solsi': 'PERSON', 'KJSCE': 'ORG', 'Tuesday': 'DATE', 'typhoid': 'NORP'} ))