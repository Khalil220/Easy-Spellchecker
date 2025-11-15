import sys
import unittest

if sys.platform.startswith("win"):
	import wx
	from easyspell.hotkeys import Hotkey, parse_hotkey
else:
	wx = None
	Hotkey = None
	parse_hotkey = None


@unittest.skipUnless(wx, "wxPython hotkey tests require Windows")
class HotkeyTests(unittest.TestCase):
	def test_combo(self):
		self.assertEqual(parse_hotkey("ctrl+alt+c"), Hotkey(wx.MOD_CONTROL | wx.MOD_ALT, ord("C")))

	def test_function_key(self):
		self.assertEqual(parse_hotkey("shift+f12"), Hotkey(wx.MOD_SHIFT, wx.WXK_F12))

	def test_invalid(self):
		with self.assertRaises(ValueError):
			parse_hotkey("invalid")


if __name__ == "__main__":
	unittest.main()
