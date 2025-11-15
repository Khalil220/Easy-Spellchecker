from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import wx


@dataclass(frozen=True)
class Hotkey:
	modifiers: int
	keycode: int


def parse_hotkey(binding: str) -> Hotkey:
	mod_map = {
		"ctrl": wx.MOD_CONTROL,
		"alt": wx.MOD_ALT,
		"shift": wx.MOD_SHIFT,
		"win": wx.MOD_WIN,
		"cmd": wx.MOD_META,
	}
	key: Optional[int] = None
	modifiers = 0
	for part in (binding or "").replace(" ", "").split("+"):
		token = part.lower()
		if token in mod_map:
			modifiers |= mod_map[token]
		elif len(token) == 1:
			key = ord(token.upper())
		elif token.startswith("f") and token[1:].isdigit():
			key = getattr(wx, f"WXK_F{int(token[1:])}", None)
		elif token:
			key = getattr(wx, f"WXK_{token.upper()}", None)
	if key is None:
		raise ValueError(f"Unsupported hotkey definition: {binding}")
	return Hotkey(modifiers=modifiers, keycode=key)
