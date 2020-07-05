<div align="center">
	<h1>Genessay :page_with_curl:</h1>
    <img src="static/icons/logo.png">
    <p>Compose application letters with ease!</p>
    <br>
</div>

<p>
    Genessay is a content generation web application which can help in composing application letters. If you're stuck and cannot frame sentences, enter the points you want included in your letter and Genessay will generate the text for you!
</p>

## Requirements
Genessay uses various Natural Language Processing (NLP) methods and Recurrent Neural Networks (RNN) to generate the text.
1. Python 64-bit
2. See dependencies list in [requirements.txt](requirements.txt)

## How to run
1. Clone the repository <br>
`git clone https://github.com/shivaneej/Genessay.git`
2. Create a Virtual Environment<br>
`python -m virtualenv name`
3. Activate the virtual environment<br>
`name\Scripts\activate`
4. Install requirements<br>
`pip install -r requirements.txt`
5. Download [spaCy](https://spacy.io/) en-core-web-sm language model<br>
`python -m spacy download en_core_web_sm`
6. Download punkt module from NLTK<br>
`nltk.download('punkt')`
7. Start the server<br>
`python main.py`<br>
The server will run on `http://localhost:8080`

## Contributors
* [Shivanee Jaiswal](https://github.com/shivaneej)
* [Rishik Kabra](https://github.com/CHECKMATErk)
* [Rohan Solsi](https://github.com/rohansolsi)
* [Vicky Daiya](https://github.com/vickydaiya)
