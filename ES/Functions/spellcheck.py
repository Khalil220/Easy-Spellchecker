from autocorrect import Speller
class speller(Speller):
	def __init__(self):
		super().__init__()
	def check(self,word=""):
		checker=self(word)
		return checker