from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import wx

from easyspell.logging_utils import configure_logging
from easyspell.spellchecker import SymSpellChecker
from easyspell.gui.main_frame import MainFrame


def run(argv: list[str] | None = None) -> int:
	parser = argparse.ArgumentParser(description="Easy Spellchecker GUI")
	parser.add_argument("--log-dir", type=str, default=None, help="Custom log directory")
	args = parser.parse_args(argv)

	log_path = configure_logging(Path(args.log_dir) if args.log_dir else None)
	logging.getLogger(__name__).info("Core GUI logging to %s", log_path)

	app = wx.App()
	checker = SymSpellChecker()

	def on_exit():
		app.ExitMainLoop()

	frame = MainFrame(checker, on_exit)
	frame.Show()
	app.MainLoop()
	return 0


if __name__ == "__main__":
	sys.exit(run())
