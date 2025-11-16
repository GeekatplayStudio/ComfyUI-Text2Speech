@echo off
echo Setting up TTS environment...

python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/ and make sure it's added to PATH.
    echo Then run this script again.
    pause
    exit /b 1
)

if not exist venv (
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

call venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

echo TTS setup complete. Run run_tts.bat to start the server.
pause