import requests
import json
from itertools import chain 
import inflect

APP_ID = '8d3198d0'
APP_KEY = 'c8887b3d58efa8e3b7ab67e514429e43'
API_URL = "https://od-api.oxforddictionaries.com:443/api/v2/entries/"

def lemmatize(word):
    inflectEngine = inflect.engine()
    if inflectEngine.singular_noun(word) != False:
        return inflectEngine.singular_noun(word)
    else:
        return word


def retrieve_synonyms(word): #retrieve synonyms using API
    word = word.strip()
    language = 'en'
    strictMatch = 'false'
    url = API_URL + language + '/' + word.lower() + '?strictMatch=' + strictMatch
    r = requests.get(url, headers = {'app_id' : APP_ID, 'app_key' : APP_KEY})
    try:
        final_result = set()
    #   print(r.json())
        synonym_result = r.json().get('results') #list
        for result in synonym_result:
            lexEntries = result.get('lexicalEntries') #list
            for lex_entry in lexEntries:
                entries = lex_entry.get('entries')
                for entry in entries:
                    senses = entry.get('senses') #list
                    for sense in senses:
                        synonyms = sense.get('synonyms')
                        if synonyms:
                            for synonym in synonyms:
                                final_result.add(synonym.get('text'))
        print(final_result)
        final_result = list(final_result)
        return final_result
    except Exception as e:
        print(e)
        return None

def get_synonyms(list_of_keywords): #check synonyms in cache file
    synonyms_dict_result = {}
    for keyword in list_of_keywords:
        keyword = keyword.strip()
        # lemmatized_kw = lemmatize(keyword)
        # synonyms_list = synonyms_table.get(keyword)
        # if not synonyms_list:
        #     print("call for", keyword)
        #     synonyms_list = retrieve_synonyms(keyword)
        #     if not synonyms_list:
        #         synonyms_list = [keyword]
        synonyms_list = [keyword]
        synonyms_dict_result[keyword] = synonyms_list
    return synonyms_dict_result


with open('dataset/synonyms.json') as json_file: 
    synonyms_table = json.load(json_file) 
