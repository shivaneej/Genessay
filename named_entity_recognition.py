import spacy
import re
nlp = spacy.load("en_core_web_sm")

def extract_named_entities(list_of_phrases):
    seperated_entities = []
    all_entities = {}
    for phrase in list_of_phrases:
        local_dict = {}
        text_input = nlp(phrase)
        for ent in text_input.ents:
            local_dict[ent.text.strip()] = ent.label_
            local_dict.update(extract_numerical_entities(phrase))
        all_entities.update(local_dict)
        seperated_entities.append(local_dict)
    return all_entities, seperated_entities

def extract_numerical_entities(_input):
    numerical_entities = {}
    date_syntax_main="[0-3][0-9][/|_|-][0-1][0-9][/|_|-][0-2][0-9][0-9][0-9]|[0-3][0-9][/|_|-][0-1][0-9][/|_|-][0-9][0-9]|[0-1][0-9][/|_|-][0-3][0-9][/|_|-][0-2][0-9][0-9][0-9]|[0-1][0-9][/|_|-][0-3][0-9][/|_|-][0-9][0-9]|[0-3][0-9][.][0-1][0-9][.][0-2][0-9][0-9][0-9]|[0-3][0-9][.][0-1][0-9][.][0-9][0-9]|[0-1][0-9][.][0-3][0-9][.][0-2][0-9][0-9][0-9]|[0-1][0-9][.][0-3][0-9][.][0-9][0-9]|[0-9]+[a-zA-Z]+[\s]+[January|Jan|February|Feb|March|April|May|June|July|August|Aug|September|Sept|October|Oct|November|Nov|December|Dec]*[\s]+[0-9]*|[a-zA-Z]+[0-9]+|[0-9]+[a-zA-Z]+|[0-9]+"
    ddmmyy="[0-3][0-9]/[0-1][0-9]/[0-2][0-9][0-9][0-9]|[0-3][0-9]/[0-1][0-9]/[0-9][0-9]|[0-1][0-9]/[0-3][0-9]/[0-2][0-9][0-9][0-9]|[0-1][0-9]/[0-3][0-9]/[0-9][0-9]"
    month_syntax="[0-9]+[a-zA-Z]+[\s]+[January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sept|October|Oct|November|Nov|December|Dec]*[\s]+[0-9]*"
    date_syntax="[0-3][0-9][.][0-1][0-9][.][0-2][0-9][0-9][0-9]|[0-3][0-9][.][0-1][0-9][.][0-9][0-9]|[0-1][0-9][.][0-3][0-9][.][0-2][0-9][0-9][0-9]|[0-1][0-9][.][0-3][0-9][.][0-9][0-9]"
    _list=re.findall(date_syntax_main, _input)
    for ele in _list:
        if re.search(ddmmyy, ele) or re.search(month_syntax, ele) != None or re.search(date_syntax, ele) != None:
            numerical_entities[ele] = "DATE"
        else:
            numerical_entities[ele] = "CARDINAL"
    return numerical_entities
