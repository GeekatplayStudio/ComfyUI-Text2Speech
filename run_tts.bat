@echo off
echo Starting TTS server...

if exist venv (
    call venv\Scripts\activate
    set PYTHON_CMD=python
) else (
    REM Check for embedded Python
    if exist "..\..\..\python_embeded\python.exe" (
        set PYTHON_CMD="..\..\..\python_embeded\python.exe"
    ) else if exist "..\..\python_embeded\python.exe" (
        set PYTHON_CMD="..\..\python_embeded\python.exe"
    ) else if exist "..\python_embeded\python.exe" (
        set PYTHON_CMD="..\python_embeded\python.exe"
    ) else (
        set PYTHON_CMD=python
    )
)

%PYTHON_CMD% tts_server.py