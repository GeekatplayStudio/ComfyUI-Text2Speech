@echo off
echo Setting up TTS environment...

REM Check for Python in ComfyUI directory
if exist "..\python.exe" (
    set PYTHON_EXE="..\python.exe"
    goto :python_found
)

REM Check for Python in PATH
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_EXE=python
    goto :python_found
)

echo Python is not found in ComfyUI directory or PATH.
echo Please ensure ComfyUI has an embedded Python installation or install Python system-wide.
pause
exit /b 1

:python_found
echo Using Python: %PYTHON_EXE%

if not exist venv (
    %PYTHON_EXE% -m venv venv
) else (
    echo Virtual environment already exists.
)

call venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

echo TTS setup complete. Run run_tts.bat to start the server.
pause