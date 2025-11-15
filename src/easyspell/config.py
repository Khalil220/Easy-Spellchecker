from dataclasses import dataclass
from pathlib import Path
from typing import Optional


APP_NAME = "Easy Spellchecker"
APP_VERSION = "1.0.0"
HOTKEY = "ctrl+alt+c"
STARTUP_NOTIFICATION = (
	"Easy Spellchecker is running in the background. Use Ctrl+Alt+C or the tray icon to open it."
)


def find_icon(base: Optional[Path] = None) -> Optional[Path]:
	candidates = []
	if base:
		candidates.append(base / "Icons" / "Alert.ico")
	package_icon = Path(__file__).resolve().parent / "assets" / "Alert.ico"
	candidates.append(package_icon)
	for candidate in candidates:
		if candidate.exists():
			return candidate
	return None
