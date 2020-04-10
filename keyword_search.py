from flashtext import KeywordProcessor
import nltk
from queue import PriorityQueue

class Entry(object):
  def __init__(self, keywords, sentence):
    self.keywords = keywords
    self.sentence = sentence
    self.matched = len(keywords)
    self.ratio = self.matched/len(nltk.tokenize.word_tokenize(sentence))
    self.rank_sum = 0
    for kw in keywords:
      self.rank_sum += keywords_rank[kw]
    return
  def __lt__(self, other):
    if self.matched != other.matched:
      return self.matched > other.matched
    else:
      if self.rank_sum != other.rank_sum:
        return self.rank_sum < other.rank_sum
      else:
        return self.ratio > other.ratio


def read_dataset():
    ipFile = open('integrated.txt','r', encoding='utf-8')
    sentences = []
    for line in ipFile.readlines():
        sentences.extend(nltk.tokenize.sent_tokenize(line))
    return sentences

def search_from_keywords(synonyms_list):
    #synonyms_list is a list of dictionaries
    global keywords_rank 
    sentences = read_dataset()
    final_result = []
    for synonyms_dict in synonyms_list:
        keywords_list = list(synonyms_dict.keys())
        threshold = 0.5 * len(keywords_list)
        if not keywords_list:
            final_result.append(None)
            continue
        keywords_rank = {keywords_list[i]:i+1 for i in range(len(keywords_list))}
        matched_sentences = PriorityQueue()
        keyword_processor = KeywordProcessor()
        keyword_processor.add_keywords_from_dict(synonyms_dict)
        for sent in sentences:
            keywords_found = set(keyword_processor.extract_keywords(sent))
            if keywords_found:
                entry_obj = Entry(list(keywords_found), sent)
                if entry_obj.matched < threshold:
                    continue
                matched_sentences.put(entry_obj)
        best_sentence = matched_sentences.get()
        if not best_sentence:
            final_result.append(None)
        else:
            final_result.append(best_sentence.sentence)
    return final_result


# test = [{"studying": ["boning (up)", "chewing over", "cogitating", "conning", "considering", "contemplating", "debating", "deliberating", "entertaining", "eyeing", "kicking around", "learning", "meditating", "memorizing", "mulling (over)", "perpending", "pondering", "poring (over)", "questioning", "revolving", "ruminating", "thinking (about or over)", "turning", "weighing", "wrestling (with)"]}, {"diagnosed": ["diagnoses", "diagnosis", "diagnostic", "misdiagnosed", "diagnostics", "overdiagnosed", "diagnostical", "diagramed", "dismissed", "disclosed", "diagnostician", "disposed", "diagnostically", "misdiagnoses", "diagnosticians", "underdiagnosed", "misdiagnose", "overdiagnoses", "diagrammed", "overdiagnose"], "fever": ["affection", "ail", "ailment", "bug", "complaint", "complication", "condition", "disease", "disorder", "distemper", "distemperature", "ill", "illness", "indisposition", "infirmity", "malady", "sickness", "trouble", "unhealthiness", "unsoundness"]}, {"certificate": ["blank", "certification", "document", "form", "instrument", "paper"], "enclosed": ["anchored", "bolted", "bound", "caged", "caught", "chained", "confined", "fastened", "fettered", "immured", "imprisoned", "kidnapped", "leashed", "manacled", "penned", "restrained", "shackled", "tied", "unfree"]}, {"grant": ["allocation", "allotment", "annuity", "appropriation", "entitlement", "subsidy", "subvention"], "leave": ["allowance", "authorization", "clearance", "concurrence", "consent", "granting", "green light", "license", "permission", "sanction", "sufferance", "warrant"]}, {}]
# print(search_from_keywords(test))

