import unittest

from easyspell.spellchecker import SymSpellChecker, Suggestion


class SymSpellCheckerTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.checker = SymSpellChecker()

	def test_empty_input_returns_no_suggestions(self):
		self.assertEqual(self.checker.suggestions(""), [])

	def test_typo_is_corrected(self):
		self.assertEqual(self.checker.best("speling").lower(), "spelling")

	def test_suggestions_are_dataclasses(self):
		items = self.checker.suggestions("accessability")
		self.assertTrue(items)
		self.assertIsInstance(items[0], Suggestion)


if __name__ == "__main__":
	unittest.main()
