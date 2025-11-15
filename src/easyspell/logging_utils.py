from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
from typing import Optional

LOG_FILE_NAME = "easy_spellchecker.log"
MAX_BYTES = 1_000_000
BACKUP_COUNT = 3


def get_log_directory() -> Path:
	base = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
	if base:
		return Path(base) / "EasySpellchecker"
	return Path.home() / ".easy_spellchecker"


def configure_logging(custom_dir: Optional[Path] = None) -> Path:
	target_dir = custom_dir or get_log_directory()
	target_dir.mkdir(parents=True, exist_ok=True)
	log_path = target_dir / LOG_FILE_NAME

	root = logging.getLogger()
	if root.handlers:
		return log_path

	handler = RotatingFileHandler(log_path, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8")
	formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
	handler.setFormatter(formatter)
	root.addHandler(handler)
	root.setLevel(logging.INFO)
	return log_path
