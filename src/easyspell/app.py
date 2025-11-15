from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional

import wx
import wx.adv

from easyspell import APP_NAME
from easyspell.config import HOTKEY, STARTUP_NOTIFICATION, find_icon
from easyspell.gui.main_frame import MainFrame
from easyspell.hotkeys import parse_hotkey
from easyspell.logging_utils import configure_logging
from easyspell.notifications import Notifier
from easyspell.spellchecker import SymSpellChecker


class SpellcheckerApp(wx.App):
    def __init__(self, log_dir: Optional[Path]):
        self._log_dir = log_dir
        self.logger = logging.getLogger(__name__)
        self.hidden_frame: Optional[wx.Frame] = None
        self.hotkey_id: Optional[int] = None
        self.tray_icon: Optional[wx.adv.TaskBarIcon] = None
        self.main_frame: Optional[MainFrame] = None
        self.notifier: Optional[Notifier] = None
        self.spellchecker: Optional[SymSpellChecker] = None
        self.asset_dir = self._asset_directory()
        super().__init__(redirect=False)
        self.SetExitOnFrameDelete(False)

    def OnInit(self) -> bool:
        configure_logging(self._log_dir)
        if sys.platform == "win32":
            try:
                import ctypes

                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_NAME)
            except Exception:
                self.logger.warning("Failed to set AppUserModelID.")
        self.logger.info("Starting Easy Spellchecker")
        self._first_close_notified = False
        self.spellchecker = SymSpellChecker()
        self.hidden_frame = wx.Frame(None)
        self.hidden_frame.Hide()
        self.notifier = Notifier("", find_icon(self.asset_dir), app_id=APP_NAME)
        self.main_frame = MainFrame(self.spellchecker, self._handle_main_close)
        self.main_frame.Show()
        self.main_frame.focus_input()

        self._register_hotkey()
        if not self._create_tray_icon():
            self.logger.error("Unable to install tray icon; exiting")
            return False

        return True

    def _asset_directory(self) -> Path:
        if getattr(sys, "frozen", False):
            env_parent = os.environ.get("NUITKA_ONEFILE_PARENT")
            if env_parent:
                return Path(env_parent)
            return Path(sys.argv[0]).resolve().parent
        repo_root = Path(__file__).resolve().parents[2]
        icons_dir = repo_root / "ES"
        if icons_dir.exists():
            return repo_root
        return Path(__file__).resolve().parent

    def _register_hotkey(self) -> None:
        try:
            binding = parse_hotkey(HOTKEY)
        except ValueError:
            self.logger.warning("Invalid hotkey %s", HOTKEY)
            return
        self.hotkey_id = wx.NewIdRef().GetId()
        if self.hidden_frame and self.hidden_frame.RegisterHotKey(self.hotkey_id, binding.modifiers, binding.keycode):
            self.hidden_frame.Bind(wx.EVT_HOTKEY, lambda evt: self.show_main_window(), id=self.hotkey_id)
            self.logger.info("Registered global hotkey %s", HOTKEY)
        else:
            self.logger.warning("Failed to register hotkey %s", HOTKEY)

    def _create_tray_icon(self) -> bool:
        class TrayIcon(wx.adv.TaskBarIcon):
            def __init__(self, outer: "SpellcheckerApp"):
                super().__init__()
                self.outer = outer
                icon_path = find_icon(outer.asset_dir)
                if icon_path and icon_path.exists():
                    icon = wx.Icon(str(icon_path))
                else:
                    icon = wx.ArtProvider.GetIcon(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))
                self.SetIcon(icon, APP_NAME)
                self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, lambda evt: outer.show_main_window())

            def CreatePopupMenu(self) -> wx.Menu:
                menu = wx.Menu()
                open_item = menu.Append(wx.ID_ANY, "Open")
                exit_item = menu.Append(wx.ID_EXIT, "Quit")
                menu.Bind(wx.EVT_MENU, lambda evt: self.outer.show_main_window(), open_item)
                menu.Bind(wx.EVT_MENU, lambda evt: self.outer.shutdown(), exit_item)
                return menu

        try:
            self.tray_icon = TrayIcon(self)
            return True
        except Exception:
            self.logger.exception("Failed to create system tray icon")
            return False

    def show_main_window(self) -> None:
        if not self.main_frame:
            return
        self.main_frame.Show()
        self.main_frame.Raise()
        self.main_frame.RequestUserAttention()
        self.main_frame.focus_input()

    def hide_main_window(self) -> None:
        if self.main_frame and self.main_frame.IsShown():
            self.main_frame.Hide()

    def _handle_main_close(self, event: wx.CloseEvent) -> None:
        if event.CanVeto():
            event.Veto()
        self.hide_main_window()
        if not self._first_close_notified and self.notifier:
            self.notifier.show(STARTUP_NOTIFICATION)
            self._first_close_notified = True

    def shutdown(self) -> None:
        self.logger.info("Shutting down Easy Spellchecker")
        if self.hotkey_id and self.hidden_frame:
            self.hidden_frame.UnregisterHotKey(self.hotkey_id)
        if self.tray_icon:
            self.tray_icon.RemoveIcon()
            self.tray_icon.Destroy()
            self.tray_icon = None
        if self.main_frame:
            self.main_frame.Destroy()
            self.main_frame = None
        if self.hidden_frame:
            self.hidden_frame.Destroy()
            self.hidden_frame = None
        self.ExitMainLoop()
        self.Destroy()


def run(argv: Optional[list[str]] = None) -> int:
	parser = argparse.ArgumentParser(description="Easy Spellchecker application")
	parser.add_argument("--log-dir", type=str, default=None)
	args = parser.parse_args(argv)

	log_dir = Path(args.log_dir) if args.log_dir else None
	configure_logging(log_dir)
	logging.getLogger(__name__).info("Easy Spellchecker logging initialised")

	if sys.platform == "win32":
		try:
			import ctypes

			ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_NAME)
		except Exception:
			logging.getLogger(__name__).warning("Failed to set AppUserModelID for notifications")

	app = SpellcheckerApp(log_dir)
	return app.MainLoop()


if __name__ == "__main__":
    sys.exit(run())
