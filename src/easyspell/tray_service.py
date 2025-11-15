from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import wx
import wx.adv

from easyspell import APP_NAME
from easyspell.config import HOTKEY, STARTUP_NOTIFICATION, find_icon
from easyspell.hotkeys import Hotkey, parse_hotkey
from easyspell.logging_utils import configure_logging
from easyspell.notifications import Notifier

CORE_EXECUTABLE = "core_app.exe"


class TrayService(wx.App):
	def __init__(self, log_dir: Optional[Path] = None):
		self._binary_dir = self._resolve_binary_dir()
		self._log_dir = log_dir
		self.logger = logging.getLogger(__name__)
		self.hidden_frame: Optional[wx.Frame] = None
		self.hotkey_id: Optional[int] = None
		self.tray_icon: Optional[wx.adv.TaskBarIcon] = None
		self.core_process: Optional[subprocess.Popen] = None
		self.notifier: Optional[Notifier] = None
		super().__init__(redirect=False)
		self.SetExitOnFrameDelete(False)

	def OnInit(self) -> bool:
		if not hasattr(self, "logger"):
			self.logger = logging.getLogger(__name__)
		configure_logging(self._log_dir)
		self.logger.info("Starting tray service from %s", self._binary_dir)
		self.hidden_frame = wx.Frame(None)
		self.hidden_frame.Hide()
		self.notifier = Notifier(APP_NAME, find_icon(self._binary_dir))
		self._register_hotkey()
		if not self._install_tray_icon():
			self.logger.error("Unable to install system tray icon. Exiting.")
			return False
		wx.CallAfter(lambda: self.notifier.show(STARTUP_NOTIFICATION))
		return True

	def _resolve_binary_dir(self) -> Path:
		if getattr(sys, "frozen", False):
			env_parent = os.environ.get("NUITKA_ONEFILE_PARENT")
			if env_parent:
				return Path(env_parent)
			env_exe = os.environ.get("NUITKA_ONEFILE_EXE")
			if env_exe:
				return Path(env_exe).resolve().parent
			exe = Path(sys.argv[0]).resolve()
			return exe.parent
		return Path(__file__).resolve().parent

	def _register_hotkey(self) -> None:
		try:
			binding = parse_hotkey(HOTKEY)
		except ValueError:
			self.logger.warning("Invalid hotkey %s", HOTKEY)
			return
		self.hotkey_id = wx.NewIdRef().GetId()
		if self.hidden_frame and self.hidden_frame.RegisterHotKey(self.hotkey_id, binding.modifiers, binding.keycode):
			self.hidden_frame.Bind(wx.EVT_HOTKEY, lambda evt: self.launch_core(), id=self.hotkey_id)
			self.logger.info("Registered global hotkey %s", HOTKEY)
		else:
			self.logger.warning("Failed to register hotkey %s", HOTKEY)

	def _install_tray_icon(self) -> bool:
		class ServiceIcon(wx.adv.TaskBarIcon):
			def __init__(self, outer: TrayService):
				super().__init__()
				self.outer = outer
				icon_path = find_icon(outer._binary_dir)
				if icon_path and icon_path.exists():
					icon = wx.Icon(str(icon_path))
				else:
					icon = wx.ArtProvider.GetIcon(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))
				self.SetIcon(icon, APP_NAME)
				self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, lambda evt: outer.launch_core())

			def CreatePopupMenu(self) -> wx.Menu:
				menu = wx.Menu()
				launch_item = menu.Append(wx.ID_ANY, "Launch")
				quit_item = menu.Append(wx.ID_EXIT, "Quit")
				menu.Bind(wx.EVT_MENU, lambda evt: self.outer.launch_core(), launch_item)
				menu.Bind(wx.EVT_MENU, lambda evt: self.outer.shutdown(), quit_item)
				return menu

		try:
			self.tray_icon = ServiceIcon(self)
			return True
		except Exception:
			self.logger.exception("Failed to initialise tray icon")
			return False

	def launch_core(self) -> None:
		if self.core_process and self.core_process.poll() is None:
			self.logger.info("Core already running; ignoring launch request.")
			return
		cmd = self._core_command()
		try:
			self.core_process = subprocess.Popen(cmd)
			self.logger.info("Launched core process: %s", cmd)
		except Exception:
			self.logger.exception("Failed to launch core process")

	def _core_command(self) -> list[str]:
		exe_path = (self._binary_dir / CORE_EXECUTABLE).resolve()
		if exe_path.exists():
			return [str(exe_path)]
		self.logger.warning("Packaged core executable not found at %s, falling back to python -m", exe_path)
		return [sys.executable, "-m", "easyspell.core_app"]

	def shutdown(self) -> None:
		self.logger.info("Shutting down tray service")
		if self.core_process and self.core_process.poll() is None:
			self.core_process.terminate()
			try:
				self.core_process.wait(timeout=5)
			except subprocess.TimeoutExpired:
				self.core_process.kill()
		if self.tray_icon:
			self.tray_icon.RemoveIcon()
			self.tray_icon.Destroy()
		if self.hotkey_id is not None:
			self.hidden_frame.UnregisterHotKey(self.hotkey_id)
		self.ExitMainLoop()
		self.Destroy()


def main(argv: list[str] | None = None) -> int:
	parser = argparse.ArgumentParser(description="Easy Spellchecker tray service")
	parser.add_argument("--log-dir", type=str, default=None)
	args = parser.parse_args(argv)
	log_dir = Path(args.log_dir) if args.log_dir else None
	app = TrayService(log_dir)
	return app.MainLoop()


if __name__ == "__main__":
	sys.exit(main())
