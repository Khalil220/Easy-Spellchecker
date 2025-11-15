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
set "PACKAGE_SWITCH=--include-package=easyspell --include-package-data=easyspell --include-package-data=symspellpy --windows-disable-console"

call :build_app || goto :teardown

echo [INFO] Build completed. Executables located in %OUT_DIR%.

:teardown
popd
exit /b %errorlevel%

:build_app
"%VENV_PY%" -m nuitka --standalone %PACKAGE_SWITCH% --output-dir="%OUT_DIR%" src\easyspell\app.py || goto :error
call :cleanup app
exit /b 0
:error
exit /b 1

:cleanup
set "BASE=%~1"
if exist "%OUT_DIR%\%BASE%.build" rmdir /s /q "%OUT_DIR%\%BASE%.build"
if exist "%OUT_DIR%\%BASE%.dist\core_app.exe" del /f /q "%OUT_DIR%\%BASE%.dist\core_app.exe"
exit /b 0
