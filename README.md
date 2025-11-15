# Easy Spellchecker

Easy Spellchecker is a screen-reader-first spelling companion for Windows. It runs quietly in the system tray, listens for a global shortcut, and launches an accessible interface for checking individual words or short phrases. The application is intentionally lightweight and offline friendly so it can be relied on even without network connectivity.

## Features
- **Windows system tray service** with launch/quit menu and startup notification
- **Global hotkey** (Ctrl+Alt+C by default) to open the spell-check dialog from anywhere
- **Accessible wxPython GUI** tuned for screen readers, including mnemonic labels and list navigation
- **SymSpell based engine** for fast, high-quality suggestions without needing the cloud
- **Logging** to `%LOCALAPPDATA%\EasySpellchecker\easy_spellchecker.log` for diagnostics

## Development
1. Install Python 3.12 (64-bit recommended for wxPython wheels).
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\pip install -r requirements.txt
   .venv\Scripts\pip install -e .
   ```
3. Run the tray service while developing:
   ```bash
   .venv\Scripts\python -m easyspell.tray_service
   ```
4. Launch the core GUI directly for faster iterations:
   ```bash
   .venv\Scripts\python -m easyspell.core_app
   ```
5. Execute tests with `python -m unittest`.

## Building for Windows
Use `build-windows.bat` to generate self-contained executables (tray + core) via Nuitka. The script installs prerequisites, compiles both binaries, and stores them under `build\windows`.

## License
This project is released under the MIT License. See [LICENSE](LICENSE) for details.
