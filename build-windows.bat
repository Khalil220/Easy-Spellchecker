@echo off
setlocal EnableDelayedExpansion

set "PROJECT_ROOT=%~dp0"
pushd "%PROJECT_ROOT%"

set "PYTHON=python"
%PYTHON% -V >nul 2>&1 || (
	echo [FATAL] Python is required on PATH.
	goto :teardown
)

set "VENV_DIR=.venv-win"
set "VENV_PY=%PROJECT_ROOT%%VENV_DIR%\Scripts\python.exe"
if not exist "%VENV_PY%" (
	%PYTHON% -m venv "%VENV_DIR%" || goto :teardown
)

call "%VENV_PY%" -m pip install --upgrade pip setuptools wheel || goto :teardown
call "%VENV_PY%" -m pip install -r requirements.txt || goto :teardown
call "%VENV_PY%" -m pip install -e . || goto :teardown
call "%VENV_PY%" -m pip install nuitka || goto :teardown

set "OUT_DIR=build\windows"
if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"
set "PACKAGE_SWITCH=--include-package=easyspell --include-package-data=easyspell --include-package-data=symspellpy"

call :build_core || goto :teardown
call :build_tray || goto :teardown

echo [INFO] Build completed. Executables located in %OUT_DIR%.

:teardown
popd
exit /b %errorlevel%

:build_core
"%VENV_PY%" -m nuitka --standalone %PACKAGE_SWITCH% --output-dir="%OUT_DIR%" src\easyspell\core_app.py || goto :error
call :cleanup core_app
exit /b 0
:error
exit /b 1

:build_tray
"%VENV_PY%" -m nuitka --standalone %PACKAGE_SWITCH% --include-data-file="%OUT_DIR%\core_app.exe=core_app.exe" --output-dir="%OUT_DIR%" src\easyspell\tray_service.py || goto :error
call :cleanup tray_service
exit /b 0

:cleanup
set "BASE=%~1"
if exist "%OUT_DIR%\%BASE%.dist" rmdir /s /q "%OUT_DIR%\%BASE%.dist"
if exist "%OUT_DIR%\%BASE%.build" rmdir /s /q "%OUT_DIR%\%BASE%.build"
if exist "%OUT_DIR%\%BASE%.onefile-build" rmdir /s /q "%OUT_DIR%\%BASE%.onefile-build"
if exist "%OUT_DIR%\%BASE%.onefile-lock" del /f /q "%OUT_DIR%\%BASE%.onefile-lock"
exit /b 0
