from gingerit.gingerit import GingerIt

def correctGrammar(sentence):
	parser = GingerIt()
	result = parser.parse(sentence)
	corrected_sent = result.get('result')
	return corrected_sent

