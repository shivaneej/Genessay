from gingerit.gingerit import GingerIt

def correctGrammar(sentence):
	parser = GingerIt()
	corrected_sent = parser.parse(sentence).get('result')
	return corrected_sent

