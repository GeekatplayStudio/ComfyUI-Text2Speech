@echo off
echo Starting TTS server...

if not exist venv (
    echo Virtual environment not found. Run install.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate

python tts_server.py