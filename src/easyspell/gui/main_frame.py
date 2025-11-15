from __future__ import annotations

from typing import Callable, Optional

import wx

from easyspell.config import APP_NAME
from easyspell.spellchecker import Suggestion, SymSpellChecker


class MainFrame(wx.Frame):
	def __init__(self, spellchecker: SymSpellChecker, on_close_request: Optional[Callable[[wx.CloseEvent], None]] = None):
		super().__init__(None, title=APP_NAME, size=(480, 360))
		self.spellchecker = spellchecker
		self.on_close_request = on_close_request
		self._create_menu()
		self._build_ui()
		self.Centre()
		self.Bind(wx.EVT_CLOSE, self._handle_close_request)

	def _create_menu(self) -> None:
		menu_bar = wx.MenuBar()
		help_menu = wx.Menu()
		help_item = help_menu.Append(wx.ID_HELP, "&Quick help\tF1")
		about_item = help_menu.Append(wx.ID_ABOUT, "&About")
		menu_bar.Append(help_menu, "&Help")
		self.SetMenuBar(menu_bar)
		self.Bind(wx.EVT_MENU, lambda evt: self._show_quick_help(), help_item)
		self.Bind(wx.EVT_MENU, lambda evt: self._show_about(), about_item)
		self.Bind(wx.EVT_CHAR_HOOK, self._handle_char_hook)

	def _build_ui(self) -> None:
		panel = wx.Panel(self)
		sizer = wx.BoxSizer(wx.VERTICAL)

		instructions = wx.StaticText(panel, label="Type a word or short phrase, then press Enter or Activate Check.")
		sizer.Add(instructions, 0, wx.ALL | wx.EXPAND, 10)

		input_box = wx.BoxSizer(wx.HORIZONTAL)
		label = wx.StaticText(panel, label="&Text to check:")
		self.input = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
		self.input.Bind(wx.EVT_TEXT_ENTER, lambda evt: self._run_spellcheck())
		input_box.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		input_box.Add(self.input, 1, wx.EXPAND)
		sizer.Add(input_box, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)

		self.check_button = wx.Button(panel, label="&Check")
		self.check_button.Bind(wx.EVT_BUTTON, lambda evt: self._run_spellcheck())
		sizer.Add(self.check_button, 0, wx.ALL | wx.ALIGN_RIGHT, 10)

		self.results = wx.ListBox(panel, style=wx.LB_SINGLE)
		sizer.Add(self.results, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)

		self.status = wx.StaticText(panel, label="Ready.")
		sizer.Add(self.status, 0, wx.ALL, 10)

		panel.SetSizer(sizer)
		self.focus_input()

	def _run_spellcheck(self) -> None:
		text = self.input.GetValue()
		if not text.strip():
			self.status.SetLabel("Enter a word to check.")
			return
		suggestions = self.spellchecker.suggestions(text)
		self.results.Clear()
		if not suggestions:
			self.status.SetLabel("No suggestions found.")
			return
		for suggestion in suggestions:
			self.results.Append(self._format_suggestion(suggestion))
		self.status.SetLabel("Use arrow keys to review suggestions.")
		self.results.SetSelection(0)
		self.results.SetFocus()

	def _format_suggestion(self, suggestion: Suggestion) -> str:
		return f"{suggestion.term} (edits {suggestion.distance}, freq {suggestion.frequency})"

	def _show_quick_help(self) -> None:
		message = "Type a word, press Enter or the Check button, then review suggestions in the list."
		wx.MessageBox(message, "Quick help", parent=self)

	def _show_about(self) -> None:
		message = "Accessible Windows spell checker built with SymSpell and wxPython."
		wx.MessageBox(message, "About", parent=self)

	def focus_input(self) -> None:
		if self.input:
			self.input.SetFocus()

	def _handle_char_hook(self, event: wx.KeyEvent) -> None:
		if event.GetKeyCode() == wx.WXK_F1:
			self._show_quick_help()
		else:
			event.Skip()

	def _close(self) -> None:
		self.Close()

	def _handle_close_request(self, event: wx.CloseEvent) -> None:
		if callable(self.on_close_request):
			self.on_close_request(event)
		else:
			event.Skip()
