from flask import Flask, jsonify, request, Response, render_template
import nltk
from nltk.tokenize import sent_tokenize
from keyword_extraction import keywordExtraction
from named_entity_recognition import extract_named_entities


app = Flask(__name__)  # static_url_path='', static_folder='static')

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
    _input = request.form["message"]
    keyphrases = nltk.sent_tokenize(_input)
    named_entities = extract_named_entities(_input) 
    keywords = keywordExtraction(keyphrases, ['NOUN','VERB','NUM'], 4, True)
    print(keywords)
    print(named_entities)
    return str(keywords) + "\n" + str(named_entities), 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    return True

def app_error(e):
    return jsonify({"message": str(e)}), 400


if __name__ == '__main__':
    app.register_error_handler(Exception, app_error)
    app.run(host='localhost', port=8080, debug=True)