@echo off
echo Setting up TTS environment...

REM Check for Python in ComfyUI root python_embeded directory
if exist "..\..\..\python_embeded\python.exe" (
    set PYTHON_EXE=..\..\..\python_embeded\python.exe
    goto :python_found
)

REM Check for Python in ComfyUI python_embeded directory (higher in tree)
if exist "..\..\python_embeded\python.exe" (
    set PYTHON_EXE=..\..\python_embeded\python.exe
    goto :python_found
)

REM Check for Python in ComfyUI python_embeded directory
if exist "..\python_embeded\python.exe" (
    set PYTHON_EXE=..\python_embeded\python.exe
    goto :python_found
)

REM Check for Python in ComfyUI directory
if exist "..\python.exe" (
    set PYTHON_EXE=..\python.exe
    goto :python_found
)

REM Check for Python in PATH
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_EXE=python
    goto :python_found
)

echo Python is not found in ComfyUI python_embeded, ComfyUI directory, or PATH.
echo Please ensure ComfyUI has an embedded Python installation or install Python system-wide.
pause
exit /b 1

:python_found
echo Using Python: %PYTHON_EXE%

REM Set PIP_EXE based on Python location
if "%PYTHON_EXE%" == "..\..\..\python_embeded\python.exe" (
    set PIP_EXE=..\..\..\python_embeded\Scripts\pip.exe
    set USE_VENV=false
) else if "%PYTHON_EXE%" == "..\..\python_embeded\python.exe" (
    set PIP_EXE=..\..\python_embeded\Scripts\pip.exe
    set USE_VENV=false
) else if "%PYTHON_EXE%" == "..\python_embeded\python.exe" (
    set PIP_EXE=..\python_embeded\Scripts\pip.exe
    set USE_VENV=false
) else (
    set PIP_EXE=pip
    set USE_VENV=true
)

if "%USE_VENV%" == "true" (
    if not exist venv (
        %PYTHON_EXE% -m venv venv
    ) else (
        echo Virtual environment already exists.
    )
    call venv\Scripts\activate
)

%PIP_EXE% install --upgrade pip
%PIP_EXE% install -r requirements.txt

echo TTS setup complete. Run run_tts.bat to start the server.
pause