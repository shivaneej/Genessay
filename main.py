from flask import Flask, jsonify, request, Response, render_template
import nltk
from nltk.tokenize import sent_tokenize
from keyword_extraction import keywordExtraction
from named_entity_recognition import extract_named_entities
from synonyms_extraction import get_synonyms
import json
from keyword_search import search_from_keywords
from flask_cors import CORS
from flashtext import KeywordProcessor
from sentence_completion import complete_sentences, Matrix, pmi
import re
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import os
from model import load
import time
from matrixGen import updateMatrices

app = Flask(__name__)  # static_url_path='', static_folder='static')
cors = CORS(app)

UPLOAD_FOLDER = './dataset'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt'])
DATASET_FILE_NAME = '/og.txt'

NAMED_ENTITY_TAGS = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']
unigram_mat = None
bigram_mat = None
trigram_mat = None
dataset_sentences = []

#change these if needed
BLANK_STRING = '_' * 5
unigrams = 'dataset/unigrams.csv'
bigrams = 'dataset/bigrams-x.csv'
trigrams = 'dataset/trigrams.csv'
dataset = 'dataset/integrated.txt'


def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/') #render main html page
def render():
    return render_template('home.html')

@app.route('/admin')
def admin_page():
   return render_template('adminpage.html')

@app.route('/letter', methods=['POST']) #process user input
def generate_letter():
    _input = request.get_json().get('message') #string
    keyphrases = nltk.sent_tokenize(_input) #list of strings
    print(keyphrases)
    named_entities = extract_named_entities(_input) 
    #keywords extraction
    keywords = keywordExtraction(keyphrases, ['NOUN','VERB','NUM'], 4, True)

    #synonyms extraction
    synonyms = []
    for keywords_list in keywords:
        synonyms.append(get_synonyms(keywords_list))

    #search sentences from dataset
    sentences = search_from_keywords(synonyms, dataset_sentences)
    num_of_sentences = len(sentences)
    print(sentences)

    #generate sentences from model
    for i in range(num_of_sentences):
        if sentences[i] == None:  
            sentences[i] = generate_text(keyphrases[i]) + "."
    
    
    #replace named entity tags
    for index in range(len(sentences)):
        sentence = sentences[index]
        keyword_processor = KeywordProcessor(case_sensitive=True)
        keyword_dict = {'~' :  NAMED_ENTITY_TAGS}
        keyword_processor.add_keywords_from_dict(keyword_dict)
        sentences[index] = keyword_processor.replace_keywords(sentence)
    
    #fill blanks using PMI
    for keywords_list in keywords:
        if not keywords_list:
            keywords[keywords.index(keywords_list)] = [' ']
            
    predicted_options = complete_sentences(sentences, keywords, named_entities, unigram_mat, bigram_mat, trigram_mat)
    print(predicted_options)
    for option in list(predicted_options.keys()):
        if predicted_options.get(option) == '':
            predicted_options[option] = BLANK_STRING
    joined_sentences = ' '.join(sentences)
    for answer in list(predicted_options.values()):
        joined_sentences = re.sub('~', answer, joined_sentences, 1)

    #return output
    _output = {}
    _output['keywords'] = keywords
    _output['options'] = named_entities
    _output['synonyms'] = synonyms
    _output['sentences'] = joined_sentences  
    print(_output)
    return json.dumps(_output), 200


def app_error(e):
    return jsonify({"message": str(e)}), 400

def generate_text(input_keywords):
    path = os.getcwd()    
    parser = ArgumentParser(formatter_class = ArgumentDefaultsHelpFormatter)
    parser.add_argument('--data-dir', type = str, default = path, help = 'data directory containing input.txt')
    parser.add_argument('--seed', type = str, default= input_keywords,help = 'seed string for sampling')
    parser.add_argument('--length', type = int, default = int(1.5*len(input_keywords)) ,help = 'length of the sample to generate') #change the '8' to change number of words
    parser.add_argument('--diversity', type = float, default = 0.01, help = 'Sampling diversity')
    args = parser.parse_args()
    model = load(args.data_dir)
    del args.data_dir
    sentence = model.sample(**vars(args))
    return sentence

def initServer():
    global unigram_mat, bigram_mat, trigram_mat, dataset_sentences
    ngrams_dict = {
        1: 'uni', 2: 'bi', 3: 'tri'
    }
    print("-"*100)
    print("starting server")
    print("-"*100)
    for i in range(1,4):
        start = time.time()
        prefix = ngrams_dict.get(i)     
        filepath = globals()[prefix+'grams']
        print("Reading",prefix + "grams", "started")
        globals()[prefix+'gram_mat'] = Matrix(filepath)
        print("Time to read",prefix + "grams", time.time() - start)
        start = time.time()
        print("Computing",prefix + "grams", "started")
        globals()[prefix+'gram_mat'] = pmi(globals()[prefix+'gram_mat'], positive=True, discounting=True)
        print("Time to compute",prefix + "grams", time.time() - start)

    ipFile = open(dataset,'r', encoding='utf-8')
    for line in ipFile.readlines():
        dataset_sentences.extend(nltk.tokenize.sent_tokenize(line))

@app.route('/uploader', methods = ['POST'])
def upload_file():
   if request.method == 'POST':  
      uploaded_file = request.files['file']
      if uploaded_file and allowed_file(uploaded_file.filename):
         dataset_file = open(UPLOAD_FOLDER + DATASET_FILE_NAME, 'r')
         file_contents = uploaded_file.read().decode("utf-8")
         file_contents = file_contents.replace('\r', ' ')
         new_samples = [content.strip() for content in file_contents.split('\n \n') if content]
         old_samples = [content for content in dataset_file.read().split('\n\n') if content]
         print(new_samples)
         total_samples = new_samples + old_samples
         total_samples = [content.strip() for content in total_samples if content]
         unique_samples = set(total_samples)
         unique_samples_list = list(unique_samples)
         with open(UPLOAD_FOLDER + DATASET_FILE_NAME, 'w') as overwritten_file:
            for sample in unique_samples_list:
               overwritten_file.write("%s\n\n" % sample)
         print("File Uploaded successfully")
         return 'file uploaded successfully', 200
      else:
         return 'not a valid file type', 422

@app.route('/update', methods=['GET'])
def update():
    updateMatrices(UPLOAD_FOLDER)
    return "", 200
   


if __name__ == '__main__':
    initServer()
    app.register_error_handler(Exception, app_error)
    app.run(host='localhost', port=8080, debug=True)
    



