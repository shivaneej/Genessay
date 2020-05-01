from gingerit.gingerit import GingerIt
from pprint import pprint

def correctGrammar(sentence):
	parser = GingerIt()
	result = parser.parse(sentence)
	pprint(result)
	corrected_sent = result.get('result')
	return corrected_sent

