from autocorrect import Speller
class speller(Speller):
	def __init__(self):
		Speller.__init__(self)
	def check(self,word=""):
		checker=self(word)
		return checker