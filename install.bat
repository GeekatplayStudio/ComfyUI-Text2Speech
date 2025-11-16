@echo off
echo Setting up TTS environment...

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