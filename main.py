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
from sentence_completion import complete_sentences
import re

app = Flask(__name__)  # static_url_path='', static_folder='static')
cors = CORS(app)
NAMED_ENTITY_TAGS = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']

@app.route('/health', methods=['GET']) #to check the API health
def health():
    _response = Response("API Up & Running!")
    _response.headers["Access-Control-Allow-Origin"] = "*"
    return _response, 200


@app.route('/') #render main html page
def render():
    return render_template('index.html')

@app.route('/letter', methods=['POST']) #process user input
def generate_letter():
    _input = request.get_json().get('message')
    keyphrases = nltk.sent_tokenize(_input)
    print(keyphrases)
    named_entities = extract_named_entities(_input) 
    keywords = keywordExtraction(keyphrases, ['NOUN','VERB','NUM'], 4, True)
    synonyms = []
    for keywords_list in keywords:
        synonyms.append(get_synonyms(keywords_list))
    sentences = search_from_keywords(synonyms)
    for index in range(len(sentences)):
        sentence = sentences[index]
        keyword_processor = KeywordProcessor()
        keyword_dict = {'~' :  NAMED_ENTITY_TAGS}
        keyword_processor.add_keywords_from_dict(keyword_dict)
        sentences[index] = keyword_processor.replace_keywords(sentence)
    predicted_options = complete_sentences(sentences, keywords, named_entities)
    print(predicted_options)
    joined_sentences = ' '.join(sentences)
    for answer in list(predicted_options.values()):
        joined_sentences = re.sub('~', answer, joined_sentences, 1)
    _output = {}
    _output['keywords'] = keywords
    _output['options'] = named_entities
    _output['synonyms'] = synonyms
    _output['sentences'] = joined_sentences   
    return json.dumps(_output), 200


def app_error(e):
    return jsonify({"message": str(e)}), 400


if __name__ == '__main__':
    app.register_error_handler(Exception, app_error)
    app.run(host='localhost', port=8080, debug=True)