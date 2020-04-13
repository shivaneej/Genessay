from flask import Flask, jsonify, request, Response, render_template
import nltk
from nltk.tokenize import sent_tokenize
from keyword_extraction import keywordExtraction
from named_entity_recognition import extract_named_entities
from synonyms_extraction import get_synonyms
import json
from keyword_search import search_from_keywords
from flask_cors import CORS


app = Flask(__name__)  # static_url_path='', static_folder='static')
cors = CORS(app)

@app.route('/health', methods=['GET']) #to check the API health
def health():
    _response = Response("API Up & Running!")
    _response.headers["Access-Control-Allow-Origin"] = "*"
    return _response, 200


@app.route('/') #render main html page
def render():
    return render_template('index.html')

@app.route('/letter', methods=['POST']) #process user input
def recieve_transcripts():
    _input = request.get_json().get('message')
    keyphrases = nltk.sent_tokenize(_input)
    named_entities = extract_named_entities(_input) 
    keywords = keywordExtraction(keyphrases, ['NOUN','VERB','NUM'], 4, True)
    synonyms = []
    for keywords_list in keywords:
        synonyms.append(get_synonyms(keywords_list))
    sentences = search_from_keywords(synonyms)
    _output = {}
    _output['keywords'] = keywords
    _output['options'] = named_entities
    _output['synonyms'] = synonyms
    _output['sentences'] = ' '.join(sentences)
    return json.dumps(_output), 200


def app_error(e):
    return jsonify({"message": str(e)}), 400


if __name__ == '__main__':
    app.register_error_handler(Exception, app_error)
    app.run(host='localhost', port=8080, debug=True)