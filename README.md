# ComfyUI-Text2Speech

A ComfyUI custom node for text-to-speech integration with a local TTS server.

## Features

- Custom ComfyUI node `HttpTTSToAudio` for sending text to a local TTS server.
- Option to load text from a file.
- Server status check node `TTSServerStatus`.
- Local TTS server using pyttsx3 (offline TTS engine), outputs MP3 files.
- Easy setup with batch files for Windows.

## Prerequisites

- Python 3.8+ installed and added to PATH. Download from [python.org](https://www.python.org/downloads/).

## Installation

### TTS Server Setup

1. Run `install.bat` to create a virtual environment and install dependencies.
2. Run `run_tts.bat` to start the TTS server on `http://127.0.0.1:5002`.

### ComfyUI Node

1. The `__init__.py` file is already in the `custom_nodes` folder.
2. Restart ComfyUI.

## Usage

- Use the `HttpTTSToAudio` node in ComfyUI under `GeekatPlay/TTS` to generate speech from text or a text file.
- Use the `TTSServerStatus` node to check if the server is running.
- Input text, optional text file path, language, and server URL.
- Output is the path to the generated MP3 audio file.

## Workflow

Connect the audio path to audio/video processing nodes in ComfyUI for creating TTS-enhanced content.
