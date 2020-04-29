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
      self.rank_sum += keywords_rank.get(kw, 0.0)
    return
  def __lt__(self, other):
    if self.matched != other.matched:
      return self.matched > other.matched
    else:
      if self.rank_sum != other.rank_sum:
        return self.rank_sum > other.rank_sum
      else:
        return self.ratio > other.ratio

def search_from_keywords(synonyms_list, sentences, keywords_with_weight):
    #synonyms_list is a list of dictionaries
    global keywords_rank
    final_result = []
    for index in range(len(synonyms_list)):
        synonyms_dict = synonyms_list[index]
        keywords_list = list(synonyms_dict.keys())
        threshold = 0.5 * len(keywords_list)
        if not keywords_list:
            final_result.append(None)
            continue
        keywords_rank = keywords_with_weight[index]
        matched_sentences = PriorityQueue()
        keyword_processor = KeywordProcessor()
        keyword_processor.add_keywords_from_dict(synonyms_dict)
        for sent in sentences:
            keywords_found = set(keyword_processor.extract_keywords(sent))
            if keywords_found:
                entry_obj = Entry(list(keywords_found), sent)
                if entry_obj.matched >= threshold:
                  matched_sentences.put(entry_obj)
        if not matched_sentences.empty():
          best_sentence = matched_sentences.get()
          final_result.append(best_sentence.sentence)
        else:
            final_result.append(None)            
    return final_result


