
# Hamming Codes

class Encoding(object):
	def __init__(s, code):
		s.code = code

	def __str__(s):
		strCode = "".join(map(lambda x: str(x), s.code))
		strEncode = "".join(map(lambda x: str(x), s.encode))		
		return "Encoding(" + strCode + " -> " + strEncode + ")" 