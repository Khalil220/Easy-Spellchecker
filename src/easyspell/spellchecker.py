from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from typing import Iterable, List

from symspellpy import SymSpell, Verbosity


@dataclass(frozen=True)
class Suggestion:
	term: str
	distance: int
	frequency: int


class SymSpellChecker:
	def __init__(self, max_edit_distance: int = 2, prefix_length: int = 7):
		self._symspell = SymSpell(max_dictionary_edit_distance=max_edit_distance, prefix_length=prefix_length)
		self._load_default_dictionaries()

	def _load_default_dictionaries(self) -> None:
		frequency = resources.files("symspellpy").joinpath("frequency_dictionary_en_82_765.txt")
		bigram = resources.files("symspellpy").joinpath("frequency_bigramdictionary_en_243_342.txt")
		self._symspell.load_dictionary(str(frequency), term_index=0, count_index=1)
		self._symspell.load_bigram_dictionary(str(bigram), term_index=0, count_index=2)

	def suggestions(self, text: str, max_results: int = 5) -> List[Suggestion]:
		term = (text or "").strip()
		if not term:
			return []
		lookup: Iterable = (
			self._symspell.lookup_compound(term)
			if " " in term
			else self._symspell.lookup(term, verbosity=Verbosity.CLOSEST, transfer_casing=True)
		)
		results = [Suggestion(item.term, item.distance, item.count) for item in lookup]
		return results[:max_results]

	def best(self, text: str) -> str:
		suggestions = self.suggestions(text, max_results=1)
		return suggestions[0].term if suggestions else text
