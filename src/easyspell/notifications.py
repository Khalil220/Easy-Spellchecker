from __future__ import annotations

from pathlib import Path
from typing import Optional

import wx
import wx.adv


class Notifier:
	def __init__(self, title: str, icon_path: Optional[Path] = None, app_id: Optional[str] = None):
		self.title = title
		self.icon_path = icon_path
		self.app_id = app_id

	def show(self, message: str) -> None:
		if not message:
			return
		app = wx.GetApp()
		if app is None:
			return
		note = wx.adv.NotificationMessage(self.title, message)
		if self.icon_path and self.icon_path.exists():
			note.SetIcon(wx.Icon(str(self.icon_path)))
		else:
			note.SetIcon(wx.ArtProvider.GetIcon(wx.ART_INFORMATION, wx.ART_OTHER, (32, 32)))
		if self.app_id and hasattr(note, "UseTaskBarIcon"):
			note.SetTitle(self.app_id)
		note.Show()
