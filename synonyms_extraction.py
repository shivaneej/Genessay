import requests
import json
from itertools import chain 

API_KEY = "b5753e1e-5aef-4ed9-aed4-67f72ddd8286"
KEY_URL = "?key="
API_URL = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"


with open('synonyms.json') as json_file: 
    synonyms_table = json.load(json_file) 

def retrieve_synonyms(word): #retrieve synonyms using API
    main_url = API_URL + word + KEY_URL + API_KEY
    responses = requests.request("GET", main_url)
    try:
        synonyms = responses.json()[0].get('meta').get('syns')
    except AttributeError:
        synonyms = responses.json()
    return synonyms

def get_synonyms(list_of_keywords): #check synonyms in cache file
    synonyms_dict_result = {}
    for keyword in list_of_keywords:
        keyword = keyword.strip()
        print(keyword)
        synonyms_list = synonyms_table.get(keyword)
        if not synonyms_list:
            print("call for", keyword)
            synonyms_list = retrieve_synonyms(keyword)
            if not synonyms_list:
                synonyms_list.append(keyword)
        if type(synonyms_list[0]) == list:
            synonyms_list = list(chain.from_iterable(synonyms_list)) 
        synonyms_dict_result[keyword] = synonyms_list
    return synonyms_dict_result


